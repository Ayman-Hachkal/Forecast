import asyncio
import os
from time import sleep
import readenv
from forecasting import Forecast
import datarequest 
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    readenv.load_env()
    AOE_KEY= os.getenv("AOE_KEY")
    WESTELM_KEY= os.getenv("WESTELM_KEY")
    print(WESTELM_KEY)
    URL ="https://api.newrelic.com/graphql" 


    # Process data for WE cart updates
    #dfTransaction = pd.DataFrame(asyncio.run(datarequest.weGetTransactonVolume(URL, WESTELM_KEY)))
    #dfTransaction = dfTransaction.drop(dfTransaction.columns.difference(["ds", "y"]), axis=1)
    #forecast.forecast(dfTransaction, "TransactionsThroughput")

    #dfUpdateCart = pd.DataFrame(asyncio.run(datarequest.we_request_cart(URL, WESTELM_KEY)))
    #dfUpdateCart = dfUpdateCart.drop(dfUpdateCart.columns.difference(["ds", "y"]), axis=1)
    #forecast.forecast(dfUpdateCart, "UpdateCart")

    #dfPlaceOrder = pd.DataFrame(asyncio.run(datarequest.WePlaceOrder(URL, WESTELM_KEY)))
    #dfPlaceOrder = dfPlaceOrder.drop(dfPlaceOrder.columns.difference(["ds", "y"]), axis=1)
    #forecast.forecast(dfPlaceOrder, "PlaceOrder")

    #dfAOETransaction = pd.DataFrame(asyncio.run(datarequest.AOEGetTransactionThroughput(URL, AOE_KEY)))
    #dfAOETransaction = dfAOETransaction.drop(dfAOETransaction.columns.difference(["ds", "y"]), axis=1)
    #dfAOETransaction = forecast.forecast(dfAOETransaction, "AOE Transaction Throughput ")

    forecast_AOE = Forecast()

    dfAOELogin = pd.DataFrame(asyncio.run(datarequest.AOELogin(URL, AOE_KEY)))
    dfAOELogin = dfAOELogin.drop(dfAOELogin.columns.difference(["ds", "y"]), axis=1)

    train_test_ratio = 0.8
    split = round((len(dfAOELogin) * 0.8))

    dfAOELoginTrain = dfAOELogin[:split]
    dfAOELoginTrainForecast = forecast_AOE.forecast(dfAOELoginTrain, "AOE Train Login ")

    dfAOELoginTest  = dfAOELogin[split:]
    dfAOELoginTestForecast = forecast_AOE.forecast(dfAOELoginTest, "AOE Test Login")

    #dfAOEUpdateCart = pd.DataFrame(asyncio.run(datarequest.AOEUpdateCart(URL, AOE_KEY)))
    #dfAOEUpdateCart = dfAOEUpdateCart.drop(dfAOEUpdateCart.columns.difference(["ds", "y"]), axis=1)
    #dfAOEUpdateCart = forecast.forecast(dfAOEUpdateCart, "AOE Update Cart ")

    #dfAOEPlaceOrder = pd.DataFrame(asyncio.run(datarequest.AOEPlaceOrder(URL, AOE_KEY)))
    #dfAOEPlaceOrder = dfAOEPlaceOrder.drop(dfAOEPlaceOrder.columns.difference(["ds", "y"]), axis=1)
    #dfAOEPlaceOrder = forecast.forecast(dfAOEPlaceOrder, "AOE Place order ")

    forecast_AOE.checkAnomoly(dfAOELoginTrain, dfAOELoginTrainForecast, dfAOELoginTest, dfAOELoginTestForecast)
    forecast_AOE.plot(dfAOELoginTest, dfAOELoginTrain)

    while True: 
        plt.pause(60)

        # Update the login data with new metrics
        dfAOELoginUpdate = pd.DataFrame(asyncio.run(datarequest.AOELoginOneMinute(URL, AOE_KEY)))
        print("--------------------------UPDATE DataFrame-----------------------------------")
        print(dfAOELoginUpdate)
        dfAOELogin = pd.concat([dfAOELogin, dfAOELoginUpdate])

        # split the data appropratily
        train_test_ratio = 0.8
        split = round((len(dfAOELogin) * 0.8))
        dfAOELoginTrain = dfAOELogin[:split]
        dfAOELoginTest  = dfAOELogin[split:]

        # repredict the forecast for the new data and the testing data
        dfAOELoginTrainForecast = forecast_AOE.forecast(dfAOELoginTrain, "AOE Train Login ")
        dfAOELoginTestForecast = forecast_AOE.forecast(dfAOELoginTest, "AOE Test Login")

        # Check anomalies for both, then plot
        forecast_AOE.checkAnomoly(dfAOELoginTrain, dfAOELoginTrainForecast, dfAOELoginTest, dfAOELoginTestForecast)
        forecast_AOE.plot(dfAOELoginTest, dfAOELoginTrain)

        
        
        



    
        
    


