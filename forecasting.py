import numpy as np
from prophet import Prophet 
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.metrics import mean_squared_error


class Forecast:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots(4, 1)
        self.plot_forecast = []
        

    def format_data(self, data: dict) -> str | None:  
        pass

    def average_year(self, data: DataFrame) -> DataFrame:  
        x = np.array(data.iloc[:, 1].tolist())
        for offset in range(0, len(data), 12):
            avg = 0
            remainder = 0
            for index in range(12): 
                print("index: ", index)
                print("offset: ", offset)
                print("total: ", index + offset)
                print("size: ", len(data))
                if (index + offset >= len(data)-1):
                    remainder = 12 - index
                    break
                avg += x[index+offset]
            avg = avg/12-remainder
            for index in range(12):
                if (index + offset >= len(data)-1):
                    break
                x[index+offset] = avg
        data.iloc[:, 1] = x
        return data

    def forecast(self, df, name) -> DataFrame:
        m = Prophet()
        print(df)
        m.fit(df)
        forecast = m.predict(df)
        forecast = forecast.set_index("ds")
        self.plot_forecast.append(forecast)
        print(forecast)
        future = m.make_future_dataframe(periods=1100, freq="min", include_history=False)
        future = m.predict(future)
        future = future.set_index("ds")
        self.plot_forecast.append(future)
        return forecast

    def plot(self, test_data: DataFrame, train_data: DataFrame, test_data_forecast : DataFrame, train_data_forecast : DataFrame):
        test_data = test_data.set_index("ds")
        train_data = train_data.set_index("ds")
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()
        self.ax[0].plot(train_data_forecast.iloc[:, -1], label="{}".format(test_data_forecast.columns[-1]))
        self.ax[0].plot(test_data_forecast.iloc[:, -1], label="{}".format(train_data_forecast.columns[-1]))

        self.ax[1].plot(train_data)
        self.ax[2].plot(test_data)
        self.ax[0].legend()
        self.ax[0].grid()
        self.ax[0].autoscale_view()
        self.plot_forecast = []

    def checkAnomoly(self, train_data: DataFrame, train_data_forecast: DataFrame, test_data: DataFrame, test_data_forecast: DataFrame):
        # Calculate RMSE for train
        train_data = train_data.fillna(0)
        train_data_forecast= train_data_forecast.fillna(0)
        test_data= test_data.fillna(0)
        test_data_forecast = test_data_forecast.fillna(0)

        train_RMSE = np.sqrt(mean_squared_error(train_data['y'], train_data_forecast['yhat']))
        # Calculate RMSE For test
        test_RMSE = np.sqrt(mean_squared_error(test_data['y'], test_data_forecast['yhat']))
        test_range = (np.max(np.array(test_data['y'].values)))
        # Calculate MAPE
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
        self.ax[3].clear()
        self.ax[3].bar([*data.keys()], [*data.values()])
