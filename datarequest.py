import json
import httpx
import pandas as pd
from pandas._libs.tslibs import timestamps


async def AOELogin(url: str, key):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Alshaya\\\\\\SocialSignIn\\\\\\Api\\\\\\CustomerManagementInterface/createCustomerTokenBySocialDetail' or name = 'WebTransaction/Action/Webapi/Rest/Magento\\\\\\Integration\\\\\\Api\\\\\\CustomerTokenServiceInterface/createCustomerAccessToken' LIMIT MAX SINCE 30 days ago", async: true) {
                results
              }
            }
          }
        }""",
        "variables": "" # or {} depending on what the API expects for empty

    }    
    async with httpx.AsyncClient() as client:
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
            df = df.rename(columns={'timestamp' :'ds', 'http.statusCode' :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).count()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df


async def AOELoginOneMinute(url: str, key):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Alshaya\\\\\\SocialSignIn\\\\\\Api\\\\\\CustomerManagementInterface/createCustomerTokenBySocialDetail' or name = 'WebTransaction/Action/Webapi/Rest/Magento\\\\\\Integration\\\\\\Api\\\\\\CustomerTokenServiceInterface/createCustomerAccessToken' LIMIT MAX SINCE 1 minute ago", async: true) {
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
            print(df)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.rename(columns={'timestamp' :'ds', 'Response.StatusCode' :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).count()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df
        except Exception:
            print("No return")
            return pd.DataFrame()

async def AOEUpdateCart(url: str, key):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/updateCart' LIMIT MAX SINCE 30 days ago", async: true) {
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
            df = df.reset_index()
            return df
        except Exception: 
            return None


async def AOEPlaceOrder(url: str, key):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/updateCart' LIMIT MAX SINCE 30 days ago", async: true) {
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
            df = df.reset_index()
            return df
        except Exception: 
            return None


async def AOEGetTransactionThroughput(url: str, key):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050){
              nrql(query: "FROM Metric SELECT * WHERE dataType='APM Agent API transaction events' and metricName = 'newrelic.resourceConsumption.currentValue' LIMIT MAX SINCE 30 day ago", async: true) {
                results
              }
            }
          }
        }""",
        "variables": "" # or {} depending on what the API expects for empty

    }    
    async with httpx.AsyncClient() as client:
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
            df = df.reset_index()
            return df

async def AOEGetCart(url: str, key: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForGuest' or name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForCustomer' LIMIT MAX SINCE 30 days ago", async: true) {
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
            return None


async def AOEGetCartOneMinute(url: str, key: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    query_payload = {
        "query": """{
          actor {
            account(id: 1927050) {
              nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForGuest' or name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForCustomer' LIMIT MAX SINCE 1 minute ago", async: true) {
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
            return None
