import numpy as np
from prophet import Prophet 
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.metrics import mean_squared_error


class Forecast:
    """
    A class to handle time-series forecasting using Facebook Prophet.
    
    Attributes:
        fig: Matplotlib figure object for plotting.
        ax: Array of Matplotlib axes for different plot components.
        plot_forecast: List to store forecast DataFrames for visualization.
    """
    def __init__(self) -> None:
        """Initializes the Forecast class with a 4x1 subplot layout."""
        self.fig, self.ax = plt.subplots(4, 1)
        self.plot_forecast = []

    def forecast(self, df) -> DataFrame:
        """
        Fits a Prophet model and predicts future values.
        
        Args:
            df (DataFrame): Input data containing 'ds' and 'y' columns.
            
        Returns:
            DataFrame: The generated forecast including predicted values.
        """
        # Initialize Prophet model
        m = Prophet()
        print(df)
        m.fit(df)
        # Generate predictions for the training data
        forecast = m.predict(df)
        forecast = forecast.set_index("ds")
        self.plot_forecast.append(forecast)
        print(forecast)
        # Create future dataframe for 1100 minutes and predict
        future = m.make_future_dataframe(periods=1100, freq="min", include_history=False)
        future = m.predict(future)
        future = future.set_index("ds")
        self.plot_forecast.append(future)
        return forecast

    def plot(self, test_data: DataFrame, train_data: DataFrame, test_data_forecast : DataFrame, train_data_forecast : DataFrame):
        """
        Visualizes the actual data vs forecasted results.
        
        Args:
            test_data (DataFrame): Actual test data.
            train_data (DataFrame): Actual training data.
            test_data_forecast (DataFrame): Predicted test data.
            train_data_forecast (DataFrame): Predicted training data.
        """
        test_data = test_data.set_index("ds")
        train_data = train_data.set_index("ds")
        
        # Clear existing axes for a fresh plot
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()
        
        # Plot training and test predictions
        self.ax[0].plot(train_data_forecast.iloc[:, -1], label="{}".format(test_data_forecast.columns[-1]))
        self.ax[0].plot(test_data_forecast.iloc[:, -1], label="{}".format(train_data_forecast.columns[-1]))

        # Plot all stored forecasts in the shared axis
        for future in self.plot_forecast:
            self.ax[0].plot(future.iloc[:, -1], label="{}".format(future.columns[-1]))

        # Plot raw train and test data
        self.ax[1].plot(train_data)
        self.ax[2].plot(test_data)
        
        self.ax[0].legend()
        self.ax[0].grid()
        self.ax[0].autoscale_view()
        self.plot_forecast = []

    def checkAnomoly(self, train_data: DataFrame, train_data_forecast: DataFrame, test_data: DataFrame, test_data_forecast: DataFrame):
        """
        Calculates and displays error metrics (RMSE, MAPE) to check for anomalies.
        
        Args:
            train_data (DataFrame): Actual training data.
            train_data_forecast (DataFrame): Predicted training data.
            test_data (DataFrame): Actual test data.
            test_data_forecast (DataFrame): Predicted test data.
        """
        # Fill missing values to avoid calculation errors
        train_data = train_data.fillna(0)
        train_data_forecast= train_data_forecast.fillna(0)
        test_data= test_data.fillna(0)
        test_data_forecast = test_data_forecast.fillna(0)

        # Calculate Root Mean Square Error (RMSE) for train and test sets
        train_RMSE = np.sqrt(mean_squared_error(train_data['y'], train_data_forecast['yhat']))
        test_RMSE = np.sqrt(mean_squared_error(test_data['y'], test_data_forecast['yhat']))
        
        # Determine the peak value in the test data for context
        test_range = (np.max(np.array(test_data['y'].values)))
        
        # Calculate Mean Absolute Percentage Error (MAPE)
        mape = np.mean(np.abs((np.array(test_data['y'].values) - np.array(test_data_forecast['yhat'].values)) / np.array(test_data['y'].notnull().values))) * 100
        print(test_range)

        data = {
            "train_RMSE"    : train_RMSE, 
            "test_RMSE"     : test_RMSE,
            "mape"          : mape,
            "range"         : test_range
        }

        print("Train RMSE: ", train_RMSE)
        print("Test RMSE: ", test_RMSE)
        print("Test MAPE: ", mape)
        
        # Visualize metrics in a bar chart
        self.ax[3].clear()
        self.ax[3].bar([*data.keys()], [*data.values()])
