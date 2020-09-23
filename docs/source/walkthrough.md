# Walkthrough


## Goal
The goal of this project is to quickly build client apis and use them without needing to install a package for every rest api that needs to be accessed.

## Design

The design of this library is made specifically for the user to be able to quickly add and adjust their client api. As a design choice, `canapi` stays tightly coupled with the `requests.Session` interface. Since the requests library is very popular, using canapi will be quite familiar. Behind every `ClientAPI` is a session with persistent information provided by the user upon initialization.

There are two ways you can access a rest api:
1. Install a client sdk built by either the community or a company.
2. Build it yourself by making functions that only access the parts of the rest api you need.

The problems with the first way arise when you need to access a lot of different client sdks and you do not want to have all of these packages installed. There also may be conflicting dependencies among these packages as well. In addition, you may not want all the functions that they provide, only the ones that are important for your use case. Lastly, you may not always agree with the logical structure of the SDK and would like the option to change it.

For the second method, writing client apis can be time consuming, especially when you feel you are repeating yourself. Part of the reason this library was built, was to follow the DRY principle. Additionally, if you have a habit of renaming functions, then having them hard coded is not something that is desired.

### Example
The following is an example of what writing a client api would look like when hard coding it yourself.

```python
from requests import Session


session = Session()
session.params = {
    "apiKey": "fake-key"
}
uri = "https://api.polygon.io"


def get_tickers(sort: str,
                type: str,
                market: str,
                locale: str,
                search: str,
                perpage: int = 50,
                page: int = 1,
                active: bool = True) -> dict:
    path = "/v2/reference/tickers"
    params = {
        "sort": sort,
        "type": type,
        "market": market,
        "locale": locale,
        "search": search,
        "perpage": perpage,
        "page": page,
        "active": active
    }
    r = session.get(
        url=uri + path
        params=params
    )
    return r.json()


def get_ticker_news(symbol: str,
                    perpage: int = 50,
                    page: int = 1) -> dict:
    path = f"/v1/meta/symbols/{symbol}/news"
    params = {
        "perpage": perpage,
        "page": page
    }
    r = session.get(
        url=uri + path,
        params=params
    )
    return r.json()

def all_stocks_snapshot():
    path = "/v2/snapshot/locale/us/markets/stocks/tickers"
    r = session.get(url=uri + path)
    return r.json()


def forex_snapshot():
    path = "/v2/snapshot/locale/global/markets/forex/tickers"
    r = session.get(uri + path)
    return r.json()
```

The problems with code above are the following:
1. Failure to recognize the DRY principle.
2. Putting every parameter needed to make the request in the signature of the function, making it difficult to utilize the commonalities between all methods.
3. Inability to group under a common sub-api to be structured logically.

For every request, the essential parameters are the http method and url. More information can be provided through keyword arguments as you normally would when making a request. Another problem is dealing with parameters that need to be substituted in the url and not sent in the keyword arguments of the request. Here is a reformatting of the above code to address some of the concerns.

```python
from requests import Session
from string import Template


session = Session()
session.params = {
    "apiKey": "fake-key"
}
uri = "https://api.polygon.io"


def get_tickers(**kwargs) -> dict:
    url = uri + "/v2/reference/tickers"
    r = session.request("get", url, **kwargs)
    return r.json()


def get_ticker_news(**kwargs) -> dict:
    url_params = kwargs.pop("url_params", {})
    path = Template("/v1/meta/symbols/${symbol}/news").substitute(**url_params)
    url = uri + path
    r = session.request("get", url, **kwargs)
    return r.json()


def all_stocks_snapshot(**kwargs):
    url = uri + "/v2/snapshot/locale/us/markets/stocks/tickers"
    r = session.request("get", url, **kwargs)
    return r.json()


def forex_snapshot(**kwargs):
    url= uri + "/v2/snapshot/locale/global/markets/forex/tickers"
    r = session.request("get", url, **kwargs)
    return r.json()
```

All function signatures are the same now. The keyword arguments of the functions are passed directly to the session's request method. Some of the issues have now been addressed, but others still remain. We still need to solve the logical grouping problem as well as not repeating ourselves. Resolving these issues any further is beyond the scope of this walkthrough of the library. You can check out the final resolutions in the library code. But to show the utility of the library, we will write the equivalent client api of the code above.

```python
polygon = cp.from_config({
    "name": "polygon",
    "uri": "https://api.polygon.io",
    "endpoints": {
        "reference": {
            "tickers": {
                "method": "get",
                "path": "/v2/reference/tickers",
                "kwargs": {
                    "params": {
                        "perpage": 50,
                        "page": 1,
                        "active": True
                    }
                }
            },
            "news": {
                "method": "get",
                "path": "/v1/meta/symbols/${symbol}/news",
                "kwargs": {
                    "params": {
                        "perpage": 50,
                        "page": 1
                    }
                }
            }
        },
        "stocks": {
            "snapshot": {
                "all": {
                    "method": "get",
                    "path": "/v2/snapshot/locale/us/markets/stocks/tickers"
                }
            }
        },
        "forex": {
            "snapshot": {
                "all": {
                    "method": "get",
                    "path": "/v2/snapshot/locale/global/markets/forex/tickers"
                }
            }
        }
    },
    "session": {
        "params": {
            "apiKey": "fake-key"
        }
    }
})
```

The code above solves the grouping and repetition problems that we needed. You can also change it by using different names for the sub-apis if you don't like the names that have already been chosen. The following are some calls that you can make with the client api defined above.

```python
polygon.reference.tickers(params={
    "sort": "ticker",
    "market": "STOCKS"
})

polygon.reference.news(url_params={"symbol": "AAPL"})

polygon.stocks.snapshot.all()

polygon.forex.snapshot.all()
```

You can also always get access to the same instance of the client api by using,
```python
cp.api("polygon")
```
and if you want to change your authentication information instead use

```python
cp.api("polygon", params={"apiKey": "fake-key"})
```


## Writing a configuration file

Writing a configuration file is quite simple. You only need to give some key
information:

1. Name of the client.
2. URI for the rest.
3. Endpoints of the rest.
4. Session parameters that need to persist for the lifetime of the client.

Here is an example using the `httpbin`, a rest api used to test the requests
library.

```json
{
    "name": "httpbin",
    "uri": "https://httpbin.org",
    "endpoints": {
        "get_anything": {
            "method": "get",
            "path": "/anything"
        }
    }
}
```

Using the `canapi` library you can use this configuration file as follows,
```python
httpbin = cp.from_json("http.json")
```

Equivalently, if you do not have the json file and only the python dictionary
you can do the following
```python

httpbin = cp.from_config({
    "name": "httpbin",
    "uri": "https://httpbin.org",
    "endpoints": {
        "get_anything": {
            "method": "get",
            "path": "/anything"
        }
    }
})
```

After you generate a client using one of these methods, it is cached. For the rest of your session, you will have access to the client by using,



```python
httpbin = cp.api("httpbin")
```

## How do you authenticate?
Authentication is done when calling a client api from the `cp.api` function. For example, the following are different ways authentication can be achieved using the library.

#### Query Authentication
```python
polygon = cp.api("polygon", params={"apiKey": POLYGON_API_KEY})
iexcloud = cp.api("iexcloud", params={"token": IEXCLOUD_API_KEY})

# For changing credential information
polygon.auth(params={"apiKey": "another-fake-key"})
```

#### Authentication Object
```python
from canapi.auth import CoinbaseExchangeAuth

auth = CoinbaseExchangeAuth(
    COINBASE_API_KEY,
    COINBASE_API_SECRET,
    COINBASE_API_PASS
)
coinbasepro = cp.api("coinbasepro", auth=auth)

```
Passing authentication information to the api is the same as passing it to a `request` in the requests library.

## Why not use OpenAPI to generate a Client SDK?
There are a couple of reasons that we do not have complete reliance on OpenAPI:

1. Not every company uses OpenAPI, hence making it difficult to rely solely on the
   configuration files needed to generate the client SDK.
2. Using this package does not mean you can't use OpenAPI configuration files. You
   can easily create a json file, usable by this library, from the yaml
   configuration files of OpenAPI.
3. There is no need to generate or install an entire client SDK package for every api you are looking to use.
4. Using `canapi`, you have immediate control over the naming and logical grouping of your client.


## Conclusion
This concludes our walkthrough. We would love to see some new ideas and feature requests by submitting issues on the GitHub. We hope you enjoyed getting to know the `canapi` library!
