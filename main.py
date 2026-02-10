import asyncio
import os
from processData import Process
import readenv 
import datarequest 
import SendData
import pandas as pd
import matplotlib.pyplot as plt



async def updateData(AOELoginGroup = None, AOEUpdateCartGroup = None, AOEPlaceOrderGroup = None, AOETransactionGroup = None):
        tasks = []
        try: 
            if AOETransactionGroup != None:
                tasks.append(AOETransactionGroup[1].processDataFrame(AOETransactionGroup[0]))
            if AOELoginGroup != None:
                tasks.append(AOELoginGroup[1].processDataFrame(AOELoginGroup[0]))
            if AOEUpdateCartGroup != None:
                tasks.append(AOEUpdateCartGroup[1].processDataFrame(AOEUpdateCartGroup[0]))
            if AOEPlaceOrderGroup != None:
                tasks.append(AOEPlaceOrderGroup[1].processDataFrame(AOEPlaceOrderGroup[0]))
            await asyncio.gather(*tasks)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    readenv.load_env()
    AOE_KEY = os.getenv("AOE_KEY")
    URL ="https://api.newrelic.com/graphql" 

    time = "43200"
    UPDATE_TIME = 3600

    AOE_process_transaction = Process("AOE Transactions")
    AOE_process_login= Process("AOE Login")
    AOE_process_update = Process("AOE Cart Updates")
    AOE_process_placeorder = Process("AOE Place Order")

    # Process AOE Transactions
    print("parsing transaction data")
    dfAOETransaction = pd.DataFrame(asyncio.run(datarequest.AOEGetTransactionThroughput(URL, AOE_KEY, time)))
    AOETransactionGroup = [dfAOETransaction, AOE_process_transaction]
    print("parsed transaction data")
    
    # Process AOE Login 
    print("parsing login data")
    dfAOELogin = asyncio.run(datarequest.AOELogin(URL, AOE_KEY, time))
    AOELoginGroup = [dfAOELogin, AOE_process_login]
    print("parsed login data")

    # Process AOE cart updates
    print("parsing update cart data")
    dfAOEUpdateCart = asyncio.run(datarequest.AOEUpdateCart(URL, AOE_KEY, time))
    AOEUpdateCartGroup = [dfAOEUpdateCart, AOE_process_update]
    print("parsed update cart data")

    # Process AOE place order
    print("parsing place order data")
    dfAOEPlaceOrder = pd.DataFrame(asyncio.run(datarequest.AOEPlaceOrder(URL, AOE_KEY, time)))
    AOEPlaceOrderGroup = [dfAOEPlaceOrder, AOE_process_placeorder]
    print("parsed place order data")


    asyncio.run(updateData(AOELoginGroup, AOEUpdateCartGroup, AOEPlaceOrderGroup, AOETransactionGroup))


    while True: 
        plt.pause(UPDATE_TIME)

        # Update AOE Transaction
        dfAOETransactionUpdate = pd.DataFrame(asyncio.run(datarequest.AOEGetTransactionThroughput(URL, AOE_KEY, str(UPDATE_TIME))))
        AOETransactionGroup[0] = pd.concat([AOETransactionGroup[0], dfAOETransactionUpdate])
        # Process and store Transaction Data
        AOE_process_transaction.storeData(dfAOETransaction, "AOETransaction")

        # Update the login data with new metrics
        dfAOELoginUpdate = pd.DataFrame(asyncio.run(datarequest.AOELogin(URL, AOE_KEY, str(UPDATE_TIME))))
        AOELoginGroup[0]= pd.concat([AOELoginGroup[0], dfAOELoginUpdate])
        # Process Data, Store
        AOE_process_login.storeData(dfAOELogin, "AOELogin")

        ## Update AOE cart updates 
        dfAOEUpdateCartUpdate = pd.DataFrame(asyncio.run(datarequest.AOEUpdateCart(URL, AOE_KEY, str(UPDATE_TIME))))
        AOEUpdateCartGroup[0] = pd.concat([AOEUpdateCartGroup[0], dfAOEUpdateCartUpdate])
        # Process Data, Store
        AOE_process_update.storeData(dfAOEUpdateCart, "AOEUpdateCart")

        ## Update AOE place order
        dfAOEPlaceOrderUpdate = pd.DataFrame(asyncio.run(datarequest.AOEPlaceOrder(URL, AOE_KEY, str(UPDATE_TIME))))
        AOEPlaceOrderGroup[0] = pd.concat([AOEPlaceOrderGroup[0], dfAOEPlaceOrderUpdate])
        # Process Data, Store
        AOE_process_placeorder.storeData(dfAOEPlaceOrder, "AOEPlaceOrder")

        asyncio.run(updateData(AOELoginGroup, AOEUpdateCartGroup, AOEPlaceOrderGroup, AOETransactionGroup))

