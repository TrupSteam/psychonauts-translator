import argparse
import os
import re

import constants
from update_character import get_character_names
from utils.file_util import get_filenames


def get_template(file_path=constants.CUTSCENES_TEMPLATE_PATH):
    
    with open(file_path, mode="r") as f:
        text = f.read()
    start_marker = "<--start-template-->"
    end_marker = "<--end-template-->"
    start_length = len(start_marker)
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)
    string_template = text[start_index + start_length + 1 : end_index]
    return string_template


def read_dfs(file_path):
    with open(file_path, mode="r", encoding="latin-1") as f:
        raw_rows = f.readlines()

    return [(raw_row[: constants.DIALOGUE_ID_LENGTH].upper(), raw_row) for raw_row in raw_rows]


def get_dialogue(dfs_rows, folder_path):
    """
    Output: {dialogue_id: [dialogue_id,character_id,origin_dialogue,translated_dialogue]}
    """
    dialogue_ids = [_id for _id, _ in dfs_rows]
    dialogue_stack = {}
    filenames = get_filenames(folder_path)
    for filename in filenames:
        with open(filename, mode="r", encoding="latin-1") as csvfile:
            csv_text = csvfile.read()
        for dialogue_id in dialogue_ids:
            if dialogue_id in dialogue_stack:
                continue
            start_index = csv_text.find(dialogue_id)
            end_index = csv_text.find("\n", start_index)
            if start_index != -1 and end_index != -1:
                dialogue = csv_text[start_index:end_index]
                dialogue_stack[dialogue_id] = dialogue.split(";")
            if set(dialogue_stack.keys()) == set(dialogue_ids):
                return dialogue_stack

    # case id in .dfs not found in any dialogues
    difference_dialogues = set(dialogue_ids) - set(dialogue_stack.keys())
    print("🤔 {} dialogue not found.".format(", ".join(difference_dialogues)))
    return dialogue_stack


def map_cutscene_dialogues(cutscene_dialogues):
    return {
        dialogue["dfs"][: constants.DIALOGUE_ID_LENGTH].upper(): dialogue
        for dialogue in cutscene_dialogues
    }


def extract_cutscene_dialogue(file_path, template):
    if not os.path.exists(file_path):
        return
    with open(file_path, mode="r") as f:
        cutscene_text = f.read()
    pattern = re.escape(template)
    pattern = re.sub(r"\\\{(\w+)\\\}", r"(?P<\1>.*)", pattern)
    cutscene_dialogues = [
        match.groupdict() for match in re.finditer(pattern, cutscene_text)
    ]
    cutscene_dialogues = map_cutscene_dialogues(cutscene_dialogues)
    return cutscene_dialogues


def create_cutscene_dialogue(
    file_path,
    dest_folder=constants.CUTSCENES_FOLDER_NAME,
    dialogue_folder=constants.DIALOGUES_FOLDER_NAME,
):
    filename = file_path.split("/")[-1]
    if filename.endswith(".dfs"):
        filename = filename[:-4] + "_dialogue.txt"
        dest_file_path = os.path.join(dest_folder, filename)

    string_template = get_template()
    dfs_rows = read_dfs(file_path)
    dialogues = get_dialogue(dfs_rows, folder_path=dialogue_folder)
    exist_cutscene_dialogues = extract_cutscene_dialogue(
        dest_file_path, string_template
    )
    character_names = get_character_names()
    result = []
    for dialogue_id, dfs_row in dfs_rows:
        dfs = dfs_row.strip()
        en_dialogue = ""
        th_dialogue = ""
        character_id = dialogue_id[-2:]
        en_character = character_names[character_id].get("EN", character_id)
        th_character = character_names[character_id].get("TH", character_id)
        
        if dialogue_id in dialogues:
            en_dialogue = dialogues[dialogue_id][2]
            th_dialogue = dialogues[dialogue_id][3]

        # check with exist
        if exist_cutscene_dialogues:
            exist_cutscene_dialogue = exist_cutscene_dialogues[dialogue_id]
            if (
                en_character == character_id
                and exist_cutscene_dialogue["EN_Character"] != character_id
            ):
                en_character = exist_cutscene_dialogue["EN_Character"]
            if (
                th_character == character_id
                and exist_cutscene_dialogue["TH_Character"] != character_id
            ):
                th_character = exist_cutscene_dialogue["TH_Character"]
            th_dialogue = exist_cutscene_dialogue["TH_Dialogue"]

        text = string_template.format(
            dfs=dfs,
            TH_Character=th_character,
            EN_Character=en_character,
            TH_Dialogue=th_dialogue,
            EN_Dialogue=en_dialogue,
        )
        result.append(text)

    with open(dest_file_path, mode="w") as f:
        text = "".join(result)
        f.write(text)
    print("🤩 Created/Updated {}".format(dest_file_path))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Create cutscenes dialogues from *.dfs files"
    )
    arg_parser.add_argument("--file", dest="dfs_file_path", required=False)
    arg_parser.add_argument("--folder", dest="dfs_folder_path", required=False)
    arg_parser.add_argument(
        "--dest",
        dest="dest_folder",
        required=False,
        default=constants.CUTSCENES_FOLDER_NAME,
    )
    arg_parser.add_argument(
        "--dialogue-folder",
        dest="dialogue_folder",
        required=False,
        default=constants.DIALOGUES_FOLDER_NAME,
    )
    args = arg_parser.parse_args()

    if args.dfs_file_path:
        create_cutscene_dialogue(
            args.dfs_file_path, args.dest_folder, dialogue_folder=args.dialogue_folder
        )

    elif args.dfs_folder_path:
        file_paths = get_filenames(args.dfs_folder_path, type=".dfs")
        for file_path in file_paths:
            create_cutscene_dialogue(
                file_path, args.dest_folder, dialogue_folder=args.dialogue_folder
            )
