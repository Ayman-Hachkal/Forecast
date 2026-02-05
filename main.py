import asyncio
import os
from processData import Process
import readenv 
import datarequest 
import SendData
import pandas as pd
import matplotlib.pyplot as plt



async def updateData(AOELoginGroup, AOEUpdateCartGroup = None, AOEPlaceOrderGroup = None, AOETransactionGroup = None):
        tasks = []
        try: 
            #tasks.append(AOETransactionGroup[1].processDataFrame(AOETransactionGroup[0]))
            tasks.append(AOELoginGroup[1].processDataFrame(AOELoginGroup[0]))
            #tasks.append(AOEUpdateCartGroup[1].processDataFrame(AOEUpdateCartGroup[0]))
            #tasks.append(AOEPlaceOrderGroup[1].processDataFrame(AOEPlaceOrderGroup[0]))
            tasks = asyncio.gather(*tasks)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    readenv.load_env()
    AOE_KEY = os.getenv("AOE_KEY")
    URL ="https://api.newrelic.com/graphql" 

    time = "21600"
    UPDATE_TIME = "60"

    #AOE_process_transaction = Process("AOE Transactions")
    AOE_process_login= Process("AOE Login")
    #AOE_process_update = Process("AOE Cart Updates")
    #AOE_process_placeorder = Process("AOE Place Order")

    # Process AOE Transactions
    #dfAOETransaction = pd.DataFrame(asyncio.run(datarequest.AOEGetTransactionThroughput(URL, AOE_KEY, time)))
    #AOETransactionGroup = [dfAOETransaction, AOE_process_transaction]
    
    # Process AOE Login 
    print("parsing logic data")
    dfAOELogin = pd.DataFrame(asyncio.run(datarequest.AOELogin(URL, AOE_KEY, time)))
    AOELoginGroup = [dfAOELogin, AOE_process_login]
    print("parsed logic data")

    ## Process AOE cart updates
    #print("parsing cart data")
    #dfAOEUpdateCart = pd.DataFrame(asyncio.run(datarequest.AOEUpdateCart(URL, AOE_KEY, time)))
    #AOEUpdateCartGroup = [dfAOEUpdateCart, AOE_process_update]
    #print("parsed cart data")

    # Process AOE place order
    #dfAOEPlaceOrder = pd.DataFrame(asyncio.run(datarequest.AOEPlaceOrder(URL, AOE_KEY, time)))
    #AOEPlaceOrderGroup = [dfAOEPlaceOrder, AOE_process_placeorder]


    asyncio.run(updateData(AOELoginGroup))


    while True: 
        plt.pause(int(UPDATE_TIME)*60)

        ## Update AOE Transaction
        #dfAOETransactionUpdate = pd.DataFrame(asyncio.run(datarequest.AOEGetTransactionThroughput(URL, AOE_KEY, UPDATE_TIME)))
        #AOETransactionGroup[0] = pd.concat([dfAOETransaction, dfAOETransactionUpdate])
        ## Process and store Transaction Data
        #AOE_process_transaction.storeData(dfAOETransaction, "AOETransaction")

        # Update the login data with new metrics
        dfAOELoginUpdate = pd.DataFrame(asyncio.run(datarequest.AOELogin(URL, AOE_KEY, UPDATE_TIME)))
        AOELoginGroup[0]= pd.concat([dfAOELogin, dfAOELoginUpdate])
        # Process Data, Store
        #AOE_process_login.storeData(dfAOELogin, "AOELogin")
        #SendData.sendMetric(str(AOE_KEY), "AOE Login", dfAOELogin)

        ## Update AOE cart updates 
        #dfAOEUpdateCartUpdate = pd.DataFrame(asyncio.run(datarequest.AOEUpdateCart(URL, AOE_KEY, UPDATE_TIME)))
        #AOEUpdateCartGroup[0] = pd.concat([dfAOEUpdateCart, dfAOEUpdateCartUpdate])
        ### Process Data, Store
        ##AOE_process_update.storeData(dfAOEUpdateCart, "AOEUpdateCart")

        ## Update AOE place order
        #dfAOEPlaceOrderUpdate = pd.DataFrame(asyncio.run(datarequest.AOEPlaceOrder(URL, AOE_KEY, UPDATE_TIME)))
        #AOEPlaceOrderGroup[0] = pd.concat([dfAOEPlaceOrder, dfAOEPlaceOrderUpdate])
        ## Process Data, Store
        #AOE_process_placeorder.storeData(dfAOEPlaceOrder, "AOEPlaceOrder")
        #asyncio.run(updateData(AOELoginGroup, AOEUpdateCartGroup))

