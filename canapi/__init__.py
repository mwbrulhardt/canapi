
import json
import os

import requests

import canapi.auth as auth

from canapi.client import ClientAPI
from canapi.exceptions import ClientAPINotRegistered


_REGISTRY = {
    "github": "https://raw.githubusercontent.com/finverse/canapi/master/registry",
    "local": None
}


def init(path: str) -> None:
    """Initializes canapi to search using a specified local registry.

    Parameters
    ----------
    path : str
        The path for the local registry.
    """
    _REGISTRY["local"] = None


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


def api(name: str, version: str = None, use_cache: bool = True, **kwargs) -> ClientAPI:
    """Gets the client api associated with `name`.

    If cached is set to True then the client api will be fetched from the
    `ClientAPI.apis` dictionary. If it is not exist, then the registry
    will be searched for files with the associated name. When cached is set to
    False the registry will always be checked and then be set in the cache.

    Parameters
    ----------
    name : str
        Name of the client api.
    version : str
        Specific version of the client api.
    use_cache : bool
        Whether or not to use the `ClientAPI` cache.
    kwargs : keyword arguments
        Additional keyword arguments to set for the underlying `requests.Session`.

    Returns
    -------
    `ClientAPI`
        The client api associated with `name`.

    Raises
    ------
    ClientAPINotRegistered
        If the client api can not be found in the remote and local registries.
    """
    client = None

    if use_cache and name in ClientAPI.apis:
        client = ClientAPI.apis[name]

    file_path = f"/{name}.json" if version is None else f"/{name}/{version}.json"

    if _REGISTRY["local"] is not None and not client:
        path = _REGISTRY["local"] + file_path
        if os.path.exists(path):
            client = from_json(path)
    else:
        url = _REGISTRY["github"] + file_path
        client = from_config(requests.get(url).json())

    if not client:
        raise ClientAPINotRegistered(name, version)

    if kwargs:
        client.auth(**kwargs)

    return client
