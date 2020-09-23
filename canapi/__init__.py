
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
    """Gets the client api associated with `name`.

    If cached is set to True then the client api will be fetched from the
    `ClientAPI.apis` dictionary. If it is not exist, then the registry
    will be searched for files with the associated name. When cached is set to
    False the registry will always be checked and then be set in the cache.

    Parameters
    ----------
    name : str
        Name of the client api.
    use_cache : bool
        Whether or not to use the `ClientAPI` cache.
    kwargs : keyword arguments
        Additional keyword arguments to set for the underlying `requests.Session`.

    Returns
    -------
    `ClientAPI`
        The client api associated with `name`.
    """
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
