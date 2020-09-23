
import json
import os

import canapi.auth as auth

from canapi.client import ClientAPI


def from_config(config: dict) -> ClientAPI:
    """Generates a client api from a `config` dictionary.

    Parameters
    ----------
    config : dict
        The configuration dictionary.

    Returns
    -------
    `ClientAPI`
        A client api.
    """
    api = ClientAPI(
        name=config['name'],
        uri=config['uri'],
        endpoints=config['endpoints'],
        **config.get('session', {})
    )
    return api


def from_json(path: str) -> ClientAPI:
    """Generates a `ClientAPI` from a json configuration file.

    Parameters
    ----------
    path : str
        The path of the configuration file.

    Returns
    -------
    `ClientAPI`
        A client api.
    """
    config = json.load(open(path))
    return from_config(config)


def api(name: str, use_cache: bool = True, **kwargs) -> ClientAPI:
    client = None

    if use_cache and name in ClientAPI.apis:
        client = ClientAPI.apis[name]
        if kwargs:
            client.auth(**kwargs)
        return client

    path = __path__[0] + f"/registry/{name}.json"
    if os.path.exists(path):
        client = from_json(path)
        if kwargs:
            client.auth(**kwargs)
        return client

    return client
