import json
import httpx
import pandas as pd


async def AOELogin(url: str, key, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Alshaya\\\\\\SocialSignIn\\\\\\Api\\\\\\CustomerManagementInterface/createCustomerTokenBySocialDetail' or name = 'WebTransaction/Action/Webapi/Rest/Magento\\\\\\Integration\\\\\\Api\\\\\\CustomerTokenServiceInterface/createCustomerAccessToken' LIMIT MAX SINCE """ + time + """ minute ago", async: true) {
                results
              }
            }
          }
        }""",
        "variables": "" # or {} depending on what the API expects for empty

    }    
    async with httpx.AsyncClient() as client:
        try: 
            response = await client.request(  method = "POST",
                                                        url = url,
                                                        headers = headers,
                                                        json = query_payload)
            data = response.json()
            cleaned = json.dumps(data, indent=4, sort_keys=True)
            parsed = json.loads(cleaned)
            # Put it into a dataframe 
            df = pd.json_normalize(parsed['data']['actor']['account']['nrql']['results'])
            # Convert from epoch to date_time
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.rename(columns={'timestamp' :'ds', 'duration' :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).mean()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df
        except Exception: 
            return pd.DataFrame()

async def AOEUpdateCart(url: str, key, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/updateCart' LIMIT MAX SINCE """ + time + """ minute ago", async: true) {
                results
              }
            }
          }
        }""",
        "variables": "" # or {} depending on what the API expects for empty

    }    
    async with httpx.AsyncClient() as client:
        try: 
            response = await client.request(  method = "POST",
                                                        url = url,
                                                        headers = headers,
                                                        json = query_payload)
            data = response.json()
            cleaned = json.dumps(data, indent=4, sort_keys=True)
            parsed = json.loads(cleaned)
            # Put it into a dataframe 
            df = pd.json_normalize(parsed['data']['actor']['account']['nrql']['results'])
            # Convert from epoch to date_time
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.rename(columns={'timestamp' :'ds', 'duration' :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).mean()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df
        except Exception: 
            return pd.DataFrame()


async def AOEPlaceOrder(url: str, key, time : str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/updateCart' LIMIT MAX SINCE """ + time + """ minute ago", async: true) {
                results
              }
            }
          }
        }""",
        "variables": "" # or {} depending on what the API expects for empty

    }    
    async with httpx.AsyncClient() as client:
        try: 
            response = await client.request(  method = "POST",
                                                        url = url,
                                                        headers = headers,
                                                        json = query_payload)
            data = response.json()
            cleaned = json.dumps(data, indent=4, sort_keys=True)
            parsed = json.loads(cleaned)
            # Put it into a dataframe 
            df = pd.json_normalize(parsed['data']['actor']['account']['nrql']['results'])
            # Convert from epoch to date_time
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.rename(columns={'timestamp' :'ds', 'duration' :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).mean()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df
        except Exception: 
            return pd.DataFrame()


async def AOEGetTransactionThroughput(url: str, key, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050){
              nrql(query: "FROM Metric SELECT * WHERE dataType='APM Agent API transaction events' and metricName = 'newrelic.resourceConsumption.currentValue' LIMIT MAX SINCE """ + time + """ minute ago", async: true) {
                results
              }
            }
          }
        }""",
        "variables": "" # or {} depending on what the API expects for empty

    }    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(  method = "POST",
                                                        url = url,
                                                        headers = headers,
                                                        json = query_payload)
            data = response.json()
            cleaned = json.dumps(data, indent=4, sort_keys=True)
            parsed = json.loads(cleaned)
            # Put it into a dataframe 
            df = pd.json_normalize(parsed['data']['actor']['account']['nrql']['results'])
            # Convert from epoch to date_time
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.rename(columns={'timestamp' :'ds', 'newrelic.resourceConsumption.currentValue.count' :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).sum()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df
        except Exception: 
            return pd.DataFrame()

async def AOEGetCart(url: str, key: str, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForGuest' or name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForCustomer' LIMIT MAX SINCE """ + time + """ minute ago", async: true) {
                results
              }
            }
          }
        }""",
        "variables": "" # or {} depending on what the API expects for empty

    }    
    async with httpx.AsyncClient() as client:
        try: 
            response = await client.request(  method = "POST",
                                                        url = url,
                                                        headers = headers,
                                                        json = query_payload)
            data = response.json()
            cleaned = json.dumps(data, indent=4, sort_keys=True)
            parsed = json.loads(cleaned)
            # Put it into a dataframe 
            df = pd.json_normalize(parsed['data']['actor']['account']['nrql']['results'])
            # Convert from epoch to date_time
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.rename(columns={'timestamp' :'ds', 'duration' :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).mean()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df
        except Exception: 
            return pd.DataFrame()

