
import json
import requests
import string

from requests import Session
from requests.structures import CaseInsensitiveDict
from typing import Callable


class Endpoint:
    """A class that provides the functionality of accessing and describing an
    endpoint.

    Parameters
    ----------
    api : `ClientAPI`
        The client api that this endpoint belongs to.
    info : dict
        Information needed to make a successful request to the endpoint.
    """

    def __init__(self, api: 'ClientAPI', info: dict) -> None:
        self.api = api
        self.info = info
        self.url_template = string.Template(self.api.uri + info["path"])

    def __call__(self, **kwargs) -> dict:
        url_params = kwargs.pop('url_params', {})
        kwargs = {**self.info.get("kwargs", {}), **kwargs}

        response = self.api.session.request(
            method=self.info["method"],
            url=self.url_template.substitute(**url_params),
            **kwargs
        )

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            data = response.content

        return data


class ClientAPI:
    """"A class for building any client api using the information about all of
    their endpoints.

    Parameters
    ----------
    name : str
        Name of the client api.
    uri : str
        Base uri to use for all endpoints in the api.
    endpoints : dict
        Available subapis and endpoints for the client.
    kwargs : dict
        Other persistent information to intialize the `Session`.
    """

    apis = {}

    def __init__(self,
                 name: str,
                 uri: str,
                 endpoints: dict,
                 **kwargs) -> None:
        self.name = name
        self.uri = uri

        if self.name not in ClientAPI.apis.keys():
            self.apis[self.name] = self
            self.session = Session()
            self.persist(**kwargs)

        for k, info in endpoints.items():
            if "path" in info.keys():
                endpoint = Endpoint(
                    api=ClientAPI.apis[self.name],
                    info=info
                )
                setattr(self, k, endpoint)
            else:
                api = ClientAPI(name, uri, info)
                setattr(self, k, api)

    def persist(self, **kwargs) -> None:
        """Persists given parameters for the client session."""
        for k in Session.__attrs__:

            if k in kwargs.keys():
                v = getattr(self.session, k)

                if k == "headers":
                    v = dict(v, **CaseInsensitiveDict(kwargs[k]))
                elif isinstance(v, dict):
                    v = dict(v, **kwargs[k])
                else:
                    v = kwargs.get(k)

                setattr(self.session, k, v)

    def auth(self, **kwargs) -> None:
        """Persists authentication information for the client."""
        self.persist(**kwargs)
