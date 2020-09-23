# Quickstart


### Installation
Install `canapi` from PyPi using:
```bash
pip install canapi
```

### Making a ClientAPI
You can get started by using one of the client apis in our registry. Before running the following code, you must go to [polygon](https://polygon.io/) and obtain a free api key.
```python
import canapi as cp

polygon = cp.api("polygon", params={"apiKey": POLYGON_API_KEY})

data = polygon.reference.news(url_params={"symbol": "AAPL"})[0]

print(data)
```

```bash
{'symbols': ['AAPL'], 'timestamp': '2020-03-26T23:52:51.000Z', 'title': 'Apple (AAPL): Despite Likely iPhone 12 Delays, the Risk-Reward Remains Compelling, Says Analyst', 'url': 'https://fin
ance.yahoo.com/news/apple-aapl-despite-likely-iphone-235251688.html', 'source': 'finance yahoo', 'summary': 'When considering the fortunes of the FAANG family since the viral outbreak, it ap
pears Apple (AAPL) has most to lose. Amazon and Netflix can count their internet driven models as particularly well set up for a hibernation period. And while Google and Facebook stand to lo
se significant advertising revenue', 'image': 'https://s.yimg.com/uu/api/res/1.2/Su.8VniRbi_GL2B3BruK5w--~B/aD0zMzc7dz0xMDI0O3NtPTE7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en-US/smarter
analyst_347/6909df17d6ef3af25ac79e2e6c0078d5', 'keywords': ['aapl']}
```

You can also practice making your own client by finding a rest api and trying to make a configuration for it. For example, using the [httpbin](https://httpbin.org/) api the following configurations can be made that are functionally the same, but offer different client methods.

```python

httpbinv0 = cp.from_config({
    "name": "httpbinv0",
    "uri": "https://httpbin.org",
    "endpoints": {
        "anything": {
            "get": {
                "method": "get",
                "path": "/anything"
            },
            "post": {
                "method": "post",
                "path": "/anything"
            },
            "put": {
                "method": "put",
                "path": "/anything"
            }
        }
    }
})


httpbinv1 = cp.from_config({
    "name": "httpbinv1",
    "uri": "https://httpbin.org",
    "endpoints": {
        "get_anything": {
            "method": "get",
            "path": "/anything"
        },
        "post_anything": {
            "method": "post",
            "path": "/anything"
        },
        "put_anything": {
            "method": "put",
            "path": "/anything"
        }
    }
})
```

The functionality of the two clients are equivalent. The only differences are in the grouping and naming of the endpoints. Essentially, the mapping of methods between the two clients is `httpbinv0.anything.<method> == httpbinv1.<method>_anything`.


Hope you enjoyed the quickstart, if you would like to know more go through our more thorough walkthrough!
