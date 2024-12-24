import aiohttp

from _utils import *

MAX_BODY_LEN = 1024


async def update_hook(webhook_url: str, info: dict, latest_ver: str, release: dict) -> None:
    overview = info["overview"]
    author_info = info[author]
    embed = {
        "content": None,
        "embeds": [
            {
                "title": info[plugin_name],
                "description": f"Updated to v{latest_ver}!",
                "url": release['html_url'],
                "color": None,
                "fields": [
                    {
                        "name": "Plugin Description",
                        "value": overview.get("featureContent", "No content provided.")
                    }
                ],
                "author": {
                    "company": author_info.get("company", "No company provided."),
                    "name": author_info.get("name", "No name provided."),
                    "email": author_info.get("email", "No email provided."),
                },
                "thumbnail": {
                    "url": overview["iconUrl"]
                }
            }
        ]
    }
    if 'github.com' in overview[url_sourcecode].lower():
        github_username = overview[url_sourcecode].split('/')[3]
        embed['embeds'][0]['author']['name'] = github_username
        embed['embeds'][0]['author']['company'] = author_info.get("company", "No company provided.")
        embed['embeds'][0]['author']['url'] = f"{github_url}/{github_username}"
        embed['embeds'][0]["author"]["icon_url"] = overview["iconUrl"] or f"{github_url}/{github_username}.png?size=40"
    release_notes = release.get('body')
    if release_notes and release_notes.strip():
        embed['embeds'][0]['fields'].append(
            {"name": "Release Notes", "value": truncate_release_notes(release['html_url'], release.get('body', ""))}
        )
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=embed)


def truncate_release_notes(url: str, release_notes: str, length: int = MAX_BODY_LEN) -> str:
    if len(release_notes) <= length:
        return release_notes

    truncation_message = f"\n[Show more...]({url})"

    # First get the exact length index that we must break at
    # But, this might cut ``, (), [], etc in half
    rough_truncation_index = length - len(truncation_message)

    # So, we will attempt to discard this entire line so it does not mess up any embed rendering with truncated markdown
    last_included_newline = release_notes[:rough_truncation_index].rfind('\n')
    graceful_truncation_index = last_included_newline if last_included_newline != -1 else rough_truncation_index

    return release_notes[:graceful_truncation_index] + truncation_message
