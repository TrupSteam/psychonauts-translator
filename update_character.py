import csv
import json

import constants
from utils.file_util import get_filenames


def get_character_ids(file_path):
    with open(file_path, mode="r", encoding="latin-1", newline="") as csvfile:
        text = csvfile.read().replace("\n", "\\n").replace("\r\\n", "\r\n")
        reader = csv.reader(text.split("\r\n"), delimiter=";")
        character_ids = set()
        for row in reader:
            if row[0] == "id":
                continue
            character_ids.add(row[1])
    return character_ids


def get_all_character_ids(file_paths):
    all_character_ids = set()
    for file_path in file_paths:
        new_character_ids = get_character_ids(file_path)
        all_character_ids = all_character_ids.union(new_character_ids)
    return all_character_ids


def update_character_json(character_ids, filename=constants.CHARACTER_NAME_FILE_PATH):
    new_character_ids = []
    with open(filename, mode="r", encoding="utf-8") as jsonfile:
        character_obj = json.load(jsonfile)
        for character_id in character_ids:
            if character_id not in character_obj:
                character_obj[character_id] = {
                    "EN": character_id,
                    "TH": character_id,
                }
                new_character_ids.append(character_id)

    if new_character_ids:
        with open(filename, mode="w", encoding="utf-8") as jsonfile:
            json.dump(character_obj, jsonfile, indent=4, ensure_ascii=False)
        print(f"updated {new_character_ids} to {constants.CHARACTER_NAME_FILE_PATH}")
    else:
        print(f"😑 nothing to update {constants.CHARACTER_NAME_FILE_PATH}")

def update_character_name(csv_folder_name):
    file_paths = get_filenames(csv_folder_name)
    all_character_ids = get_all_character_ids(file_paths)
    update_character_json(all_character_ids)
    
def get_character_names(ids=None):
    with open(constants.CHARACTER_NAME_FILE_PATH, mode="r", encoding="utf-8") as jsonfile:
        character_obj = json.load(jsonfile)
        if not ids:
            return character_obj
        return {id: character_obj[id] for id in ids}


if __name__ == "__main__":
    update_character_name(constants.DIALOGUES_FOLDER_NAME)
