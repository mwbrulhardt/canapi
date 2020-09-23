# CanAPI

![License](https://img.shields.io/github/license/finverse/canapi)
![Build Status](https://img.shields.io/github/workflow/status/finverse/canapi/CanAPI)
![Documentation Status](https://readthedocs.org/projects/canapi/badge/?version=latest)
![Stars](https://img.shields.io/github/stars/finverse/canapi)


A universal client api generator. To learn more about the design and how to use please read our [documentation](https://canapi.readthedocs.io/en/latest/)


## Installation
Install `canapi` from PyPi using:
```bash
pip install canapi
```

## Making a ClientAPI
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

You can also practice making your own client by finding a rest api and trying to make a configuration for it. For example, using [httpbin](https://httpbin.org/) the following client can be made.

```python
httpbin = cp.from_config({
    "name": "httpbin",
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

print(httpbin.anything.get(params={"p0": 0}))
```

## Contributors
Here are some good ideas for contributions to the library at this point:
* More json configuration files for the registry
* Tool for converting OpenAPI yaml file into a usable json file for the registry.
* Webscraping tools for creating a configuration files from rest api documentation online.

If you can think of more than create a new issue!
