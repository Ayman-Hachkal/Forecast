import httpx
import pandas as pd 

def sendMetric(key: str, name: str, df: pd.DataFrame) -> int:
    """send metric data to new relic"""
    headers = {
    'Content-Type': 'application/json',
    'Api-Key': key,
    }

    df = df.head(1)


    metric = {
    "name"  : f"forecast_{name}",
    "type"  : "count",
    "value" : float(df['y'].iloc[0]),
    "timestamp" : int(pd.to_datetime(df['ds'].iloc[0]).timestamp()),
    }

    body = [{ "metrics" : [metric] }]
    print(headers)
    print(body)
    response = httpx.post(url = "https://metric-api.newrelic.com/metric/v1",
                          headers = headers,
                          json = body,
                          verify = False)
    if response.status_code != 200:
        print(response.status_code)
        print(response.json)
        return 1

    return 0
