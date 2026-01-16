import httpx
import pandas as pd 

async def sendMetric(key: str, name: str, df: pd.DataFrame) -> int:
    """send metric data to new relic"""
    headers = {
        "Content-Type":  "application/json",
        "API-Key": key
    }

    metrics = []

    for record in df:
        metric = {
            "name"  : f"forecast {name}",
            "type"  : "count",
            "value" : record['y'],
            "timestamp" : record['ds'],

        }
        metrics.append(metric)

    body = { "metrics" : metrics}
    async with httpx.AsyncClient() as client:
            response = await client.request(  method = "POST",
                                                        url = "https://metric-api.newrelic.com/metric/v1",
                                                        headers = headers,
                                                        json = body)
    return 0
