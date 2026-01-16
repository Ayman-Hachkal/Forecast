import asyncio
import os
from processData import Process
import readenv
import datarequest 
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    readenv.load_env()
    WESTELM_KEY= os.getenv("WESTELM_KEY")
    AOE_KEY = os.getenv("AOE_KEY")
    URL ="https://api.newrelic.com/graphql" 

    time = "25200"


    # Process AOE Transactions
    AOE_process_transaction = Process()
    dfAOETransaction = pd.DataFrame(asyncio.run(datarequest.AOEGetTransactionThroughput(URL, AOE_KEY, time)))
    AOE_process_transaction.processDataFrame(dfAOETransaction)
    
    # Process AOE Login 
    AOE_process_login= Process()
    dfAOELogin = pd.DataFrame(asyncio.run(datarequest.AOELogin(URL, AOE_KEY, time)))
    AOE_process_login.processDataFrame(dfAOELogin)

    # Process AOE cart updates
    AOE_process_update = Process()
    dfAOEUpdateCart = pd.DataFrame(asyncio.run(datarequest.AOEUpdateCart(URL, AOE_KEY, time)))
    AOE_process_update.processDataFrame(dfAOEUpdateCart)

    # Process AOE place order
    AOE_process_placeorder = Process()
    dfAOEPlaceOrder = pd.DataFrame(asyncio.run(datarequest.AOEPlaceOrder(URL, AOE_KEY, time)))
    AOE_process_placeorder.processDataFrame(dfAOEPlaceOrder)

    update_time = "1"

    while True: 
        plt.pause(60)

        # Update AOE Transaction
        dfAOETransactionUpdate = pd.DataFrame(asyncio.run(datarequest.AOEGetTransactionThroughput(URL, AOE_KEY, update_time)))
        dfAOETransaction = pd.concat([dfAOETransaction, dfAOETransactionUpdate])
        # Process and store Transaction Data
        AOE_process_transaction.processDataFrame(dfAOETransaction)
        AOE_process_transaction.storeData(dfAOETransaction, "AOETransaction")

        # Update the login data with new metrics
        dfAOELoginUpdate = pd.DataFrame(asyncio.run(datarequest.AOELogin(URL, AOE_KEY, update_time)))
        dfAOELogin = pd.concat([dfAOELogin, dfAOELoginUpdate])
        # Process Data, Store
        AOE_process_login.processDataFrame(dfAOELogin)
        AOE_process_login.storeData(dfAOELogin, "AOELogin")

        # Update AOE cart updates 
        dfAOEUpdateCartUpdate = pd.DataFrame(asyncio.run(datarequest.AOEUpdateCart(URL, AOE_KEY, update_time)))
        dfAOEUpdateCart = pd.concat([dfAOEUpdateCart, dfAOEUpdateCartUpdate])
        # Process Data, Store
        AOE_process_update.processDataFrame(dfAOEUpdateCart)
        AOE_process_update.storeData(dfAOEUpdateCart, "AOEUpdateCart")

        # Update AOE place order
        dfAOEPlaceOrderUpdate = pd.DataFrame(asyncio.run(datarequest.AOEPlaceOrder(URL, AOE_KEY, update_time)))
        dfAOEPlaceOrder = pd.concat([dfAOEPlaceOrder, dfAOEPlaceOrderUpdate])
        # Process Data, Store
        AOE_process_placeorder.processDataFrame(dfAOEPlaceOrder)
        AOE_process_placeorder.storeData(dfAOEPlaceOrder, "AOEPlaceOrder")
