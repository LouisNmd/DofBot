from pathlib import Path
import json


def get_current_cell_id(message, name):
    if message["__type__"] != "MapComplementaryInformationsDataMessage":
        return

    actors_list = message["actors"]
    try:
        player = [a for a in actors_list if a["name"] == name][0]
    except IndexError:
        return

    return player["disposition"]["cellId"]


def get_map_object(message):
    map_id = message["mapId"]
    json_path = list(
        Path.glob(Path.cwd().joinpath("sources"), f"**/{int(map_id)}.json")
    )[
        0
    ]  # TODO: Handle case where json does not exist

    with open(json_path) as map_data:
        return json.load(map_data)


def move_to_cell(message):
    if message["__type__"] != "MapComplementaryInformationsDataMessage":
        return

    map_data = get_map_object(message)
    cells = map_data["cells"]
    to_string = ""
    for index, cell in enumerate(cells):
        if index % 14 == 0:
            print(to_string)
            to_string = ""
        to_string += "0" if cell["mov"] else "1"
