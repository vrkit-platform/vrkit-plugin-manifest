# -*-coding: utf-8 -*-
import uuid

from _utils import (
    check_url, clean, get_file_plugins_json_info, get_plugin_file_paths, get_plugin_filenames,
    id_name, plugin_reader, url_icon, plugin_name
)

plugin_infos = plugin_reader()


def test_uuid_unique():
    uuids = [clean(info[id_name]) for info in plugin_infos]
    duplicates = set([plugin_id for plugin_id in uuids if uuids.count(plugin_id) > 1])

    msg = f"{id_name} not unique: {duplicates}"
    assert len(duplicates) == 0, msg


def test_valid_icon_url():
    for plugin in plugin_infos:
        msg = f"The URL in {url_icon} is not a valid URL."
        assert check_url(plugin["overview"][url_icon]), msg


def test_file_type_json():
    incorrect_ext_files = [file_path for file_path in get_plugin_file_paths() if not file_path.endswith(".json")]

    assert len(incorrect_ext_files) == 0, f"Expected the following file to be of .json extension: {incorrect_ext_files}"


def test_file_name_construct():
    filenames = get_plugin_filenames()
    for info in plugin_infos:
        assert (
                f"{info[plugin_name]}-{info[id_name]}.json" in filenames
        ), (f"Plugin {info[plugin_name]} with ID {info[id_name]} does not have the correct filename. "
            f"Make sure it's name + ID, i.e. {info[plugin_name]}-{info[id_name]}.json")


def test_submitted_plugin_id_is_valid_uuid():
    plugins_json_ids = [item[id_name] for item in get_file_plugins_json_info(id_name)]
    existing_plugin_file_ids = [info[id_name] for info in plugin_infos]

    for plugin_id in existing_plugin_file_ids:
        # plugins.json would not contain new submission's ID.
        if plugin_id in plugins_json_ids:
            continue

        try:
            uuid.UUID(plugin_id, version=4)
            outcome = True
        except ValueError:
            outcome = False

        assert outcome is True, f"The submission plugin ID {plugin_id} is not a valid v4 UUID"
