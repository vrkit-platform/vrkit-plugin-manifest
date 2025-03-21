# -*-coding: utf-8 -*-
import json5
import validators
import asyncio
import aiohttp
from os import getenv
from sys import argv
import traceback

from tqdm.asyncio import tqdm

from _utils import *
from discord import update_hook


async def update_plugin_manifest(session, info) -> dict:
    manifest_url = info["overview"]["manifestUrl"]
    if not validators.url(manifest_url):
        print(f"No manifest URL found for {info[plugin_name]}")
        return info

    res = await session.get(manifest_url)
    if res.status in (403, 304):
        print(f"Error code={res.status} when fetching manifest for {info[plugin_name]}")
        return info

    info_text = await res.text("utf-8")
    new_info = json5.loads(info_text)
    if new_info[id_name] != info[id_name]:
        raise Exception(f"ID mismatch in new/old manifest for {info[plugin_name]} (current={info[id_name]},new={new_info[id_name]})")

    for key in ["author", "overview", "components", "name", "description"]:
        info[key] = new_info[key]

    return info


async def batch_github_plugin_info(
    info: P, tags: ETagsType, github_token=None, webhook_url: str = None
) -> P:
    try:
        overview = info["overview"]
        headers = {"authorization": f"token {github_token}"}
        if "github.com" not in overview[url_download]:
            return info

        url_parts: List[str] = overview[url_sourcecode].split("/")
        if len(url_parts) < 5:
            return info

        repo = "/".join(url_parts[3:5])
        tag: str = tags.get(info[id_name], info.get(etag, ""))

        if release_date in info.keys():
            headers["If-None-Match"] = tag

        async with aiohttp.ClientSession() as session:
            res = await session.get(
                url_release.format(repo=repo),
                headers=headers,
            )
            if res.status in (403, 304):
                return info

            latest_rel = await res.json()

            assets = latest_rel.get("assets")
            if assets is None:
                raise Exception(f"No assets found in the latest release ({info['name']})")

            info = await update_plugin_manifest(session, info)
            overview = info["overview"]

            published_at = latest_rel.get("published_at")

            if info.get(release_date, "") != published_at:
                info[release_date] = published_at

            if info.get(date_added, "") == "":
                info[date_added] = published_at

            overview[url_download] = assets[0]["browser_download_url"]

            await send_notification(
                info, clean(latest_rel["tag_name"], "v"), latest_rel, webhook_url
            )
            info[version] = clean(latest_rel["tag_name"], "v")

            tags[info[id_name]] = res.headers.get(etag, "")

            return info
    except Exception as e:
        tb = traceback.format_exc()
        print(f"Error when processing plugin {info[plugin_name]}:\n{e} {tb}")
        return info


async def batch_plugin_infos(
    plugin_infos: Ps, tags: ETagsType, github_token, webhook_url: str = None
) -> Ps:
    return await tqdm.gather(
        *[
            batch_github_plugin_info(info, tags, github_token, webhook_url)
            for info in tqdm(plugin_infos)
        ]
    )


def remove_unused_etags(plugin_infos: Ps, etags: ETagsType) -> ETagsType:
    etags_updated = {}
    plugin_ids = [info.get(id_name) for info in plugin_infos]

    for plugin_id, tag in etags.items():

        if plugin_id not in plugin_ids:
            print(
                f"Plugin with ID {plugin_id} has been removed. The associated ETag will be also removed now."
            )
            continue

        etags_updated[plugin_id] = tag

    return etags_updated


async def send_notification(
    info: P, latest_ver, release, webhook_url: str = None
) -> None:
    if version_tuple(info[version]) != version_tuple(latest_ver):
        tqdm.write(f"Update detected: {info[plugin_name]} {latest_ver}")
        try:
            await update_hook(webhook_url, info, latest_ver, release)
        except Exception as e:
            tqdm.write(str(e))


async def main():
    webhook_url = None
    if len(argv) > 1:
        webhook_url = argv[1]
    plugin_infos = plugin_reader()
    etags = etag_reader()

    plugin_infos_new = await batch_plugin_infos(
        plugin_infos, etags, getenv("GITHUB_TOKEN"), webhook_url
    )
    plugin_writer(plugin_infos_new)

    etags_new = remove_unused_etags(plugin_infos_new, etags)
    etags_writer(etags_new)


if __name__ == "__main__":
    asyncio.run(main())
