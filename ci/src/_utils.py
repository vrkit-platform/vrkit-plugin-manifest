# -*-coding: utf-8 -*-
import json
import json5
from pathlib import Path
from typing import Dict, List, TypeVar
import re
import os

# path
utils_path = Path(__file__).resolve()

src_dir = utils_path.parent
ci_dir = src_dir.parent
base_dir = ci_dir.parent
plugin_dir = base_dir / "plugins/"
etag_file = base_dir / "etags.json"

# constants
id_name = "id"
etag = "ETag"
version = "version"
url_sourcecode = "sourceUrl"
url_download = "downloadUrl"
url_release = "https://api.github.com/repos/{repo}/releases/latest"
# icon_path = "IcoPath"
author = "author"
plugin_name = "name"
github_url = "https://github.com"
release_date = "updatedAt"
date_added = "createdAt"

# typing
PluginType = Dict[str, str]
P = TypeVar("P", bound=PluginType)
PluginsType = List[PluginType]
Ps = TypeVar("Ps", bound=PluginsType)

ETagsType = Dict[str, str]


def plugin_reader() -> P:
    plugin_file_paths = get_plugin_file_paths()

    manifests = []

    for plugin_path in plugin_file_paths:
        with open(plugin_path, "r", encoding="utf-8") as f:
            manifests.append(json5.load(f))

    return manifests

def get_plugin_file_paths() -> list[str]:
    return [os.path.join(plugin_dir, filename) for filename in get_plugin_filenames()]

def get_plugin_filenames() -> list[str]:
    return os.listdir(plugin_dir)

def etag_reader() -> ETagsType:
    with open(etag_file, "r", encoding="utf-8") as f:
        return json5.load(f)


def plugin_writer(content: P):
    for plugin in content:
        with open(plugin_dir / f"{plugin[plugin_name]}-{plugin[id_name]}.json", "w", encoding="utf-8") as f:
            json.dump(plugin, f, indent=4)
        
def etags_writer(content: ETagsType):
    with open(etag_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)


def clean(string: str, flag="-") -> str:
    return string.lower().replace(flag, "").strip()

def version_tuple(version: str) -> tuple:
    version = clean(version, "v")
    return tuple(version.split("."))

def check_url(url: str) -> bool:
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None


def get_file_plugins_json_info(required_key: str = "") -> list[dict[str, str]]:
    with open("plugins.json", "r", encoding="utf-8") as f:
        data = json5.load(f)

    if not required_key:
        return data

    return [{required_key: plugin[required_key]} for plugin in data]
