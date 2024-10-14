import csv
import json
import os
from typing import Final

CHARACTER_FILENAME: Final[str] = "character.json"


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


def update_character_json(character_ids,filename=CHARACTER_FILENAME):
    new_character_ids = []
    with open(filename, mode="r", encoding="utf-8") as jsonfile:
        character_obj = json.load(jsonfile)
        for character_id in character_ids:
            if character_id not in character_obj:
                character_obj[character_id] = {
                    "EN": "",
                    "TH": "",
                }
                new_character_ids.append(character_id)

    if new_character_ids:
        with open(filename, mode="w", encoding="utf-8") as jsonfile:
            json.dump(character_obj, jsonfile, indent=4, ensure_ascii=False)
        print(f"updated {new_character_ids} to {CHARACTER_FILENAME}")
    else:
        print(f"nothing to update {CHARACTER_FILENAME}")


def get_filenames(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            yield os.path.join(folder_path, filename)


def update_character_name(csv_folder_name):
    file_paths = get_filenames(csv_folder_name)
    all_character_ids = get_all_character_ids(file_paths)
    update_character_json(all_character_ids)


if __name__ == "__main__":
    CSV_FOLDER_NAME = "dialogues"
    update_character_name(CSV_FOLDER_NAME)
