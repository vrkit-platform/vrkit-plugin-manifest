from datetime import datetime

from _utils import plugin_reader, plugin_writer, release_date, date_added

if __name__ == "__main__":
    plugin_infos = plugin_reader()

    for idx, plugin in enumerate(plugin_infos):
        # Add date added if field is not present
        if plugin.get(date_added) is None:
            plugin_infos[idx][date_added] = plugin_infos[idx][release_date] or datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
    plugin_writer(plugin_infos)
