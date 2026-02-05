import asyncio
import json
import httpx
import pandas as pd

async def Request(url, headers, query_payload, clean_data, sum_or_avg = 'avg'):
    async with httpx.AsyncClient() as client:
        print("parsing...")
        try: 
            response = await client.request(method = "POST",
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
            df = df.rename(columns={'timestamp' : 'ds', clean_data :'y'})
            df = df.drop(df.columns.difference(["ds", "y"]), axis=1)
            if sum_or_avg == 'avg':
                df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).mean()
            elif sum_or_avg == 'sum':
                df = df.groupby(pd.Grouper(key='ds', freq='min', dropna=False, axis=0)).sum()
            df = df.fillna(0).reset_index()
            df = df.reset_index()
            return df
        except Exception: 
            return pd.DataFrame()


async def AOELogin(url: str, key, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    queries = []
    until_time = 0 
    increment = 60
    since_time = increment
    
    while (since_time < int(time)):
        query_payload = {
            "query": """{
              actor {
                account(id: 1927050) {
                  nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Alshaya\\\\\\SocialSignIn\\\\\\Api\\\\\\CustomerManagementInterface/createCustomerTokenBySocialDetail' or name = 'WebTransaction/Action/Webapi/Rest/Magento\\\\\\Integration\\\\\\Api\\\\\\CustomerTokenServiceInterface/createCustomerAccessToken' LIMIT MAX SINCE """ + str(since_time)+ """ minute ago UNTIL """ + str(until_time) + """ minute ago", async: true) {
                    results
                  }
                }
              }
            }""",
            "variables": "" # or {} depending on what the API expects for empty
        }    
        queries.append(Request(url, headers, query_payload, 'duration'))
        since_time += increment
        until_time += increment

    results = await asyncio.gather(*queries)
    df = pd.concat(results)
    return df

async def AOEUpdateCart(url: str, key, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    queries = []
    until_time = 0 
    increment = 60
    since_time = increment
    
    while (since_time < int(time)):
        print("AOE update cart: building query...")
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
        queries.append(Request(url, headers, query_payload, 'duration'))
        since_time += increment
        until_time += increment

    results = await asyncio.gather(*queries)
    df = pd.concat(results)
    return df


async def AOEPlaceOrder(url: str, key, time : str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    queries = []
    until_time = 0 
    increment = 60
    since_time = increment

    while (since_time < int(time)):
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
        queries.append(Request(url, headers, query_payload, 'duration'))
        since_time += increment
        until_time += increment

    results = await asyncio.gather(*queries)
    df = pd.concat(results)
    return df


async def AOEGetTransactionThroughput(url: str, key, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    queries = []
    until_time = 0 
    increment = 60
    since_time = increment

    while (since_time < int(time)):
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
        queries.append(Request(url, headers, query_payload, 'newrelic.resourceConsumption.currentValue.count', 'sum'))
        since_time += increment
        until_time += increment

    results = await asyncio.gather(*queries)
    df = pd.concat(results)
    return df

async def AOEGetCart(url: str, key: str, time: str):
    """requesting new relic aoe for login, add cart, order, and throughput"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }
    queries = []
    until_time = 0 
    increment = 480
    since_time = increment

    while (since_time < int(time)):
        query_payload = {
            "query": """{
              actor { account(id: 1927050) {
                  nrql(query: "FROM Transaction SELECT * WHERE name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForGuest' or name = 'WebTransaction/Action/Webapi/Rest/Acquia\\\\\\CommerceManager\\\\\\Api\\\\\\CartManagementInterface/getCartForCustomer' LIMIT MAX SINCE """ + time + """ minute ago", async: true) {
                    results
                  }
                }
              }
            }""",
            "variables": "" # or {} depending on what the API expects for empty

        }    
        queries.append(Request(url, headers, query_payload, 'duration'))
        since_time += increment
        until_time += increment

    results = await asyncio.gather(*queries)
    df = pd.concat(results)
    return df
