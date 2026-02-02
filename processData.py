import pandas as pd

from forecasting import Forecast 

class Process:
    def __init__(self, name : str):
        self.forecast = Forecast(name)

    def processDataFrame(self, df : pd.DataFrame):
        df = df.drop(df.columns.difference(["ds", "y"]), axis=1)

        split = int(len(df) * 0.8)

        dfTrain = df[:split]
        dfTrainForecast = self.forecast.forecast(dfTrain)

        dfTest = df[split:]
        dfTestForecast = self.forecast.forecast(dfTest)

        self.forecast.checkAnomoly(dfTrain, dfTrainForecast, dfTest, dfTestForecast)
        self.forecast.plot(dfTest, dfTrain, dfTestForecast, dfTrainForecast)

    def storeData(self, df : pd.DataFrame, name : str): 
        df.to_csv(f"Data/{name}data.csv")

    def readData(self, name : str): 
        df = pd.DataFrame(pd.read_csv(f"Data/{name}data.csv"))
        return df



