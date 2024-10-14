def get_template():
    file_path = "cutscenes/template.sample"
    with open(file_path, mode="r") as f:
        text = f.read()
    start_marker = "<--start-template-->"
    end_marker = "<--end-template-->"
    start_length = len(start_marker)
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)
    string_template = text[start_index + start_length+1: end_index]
    print("====>",string_template,"<====")
    return string_template


def read_dfs(file_path):
    with open(file_path, mode="r") as f:
        raw_rows = f.readlines()
    
    return [(raw_row[:9],raw_row) for raw_row in raw_rows]
            
    


import os

from update_character import get_character_names


def get_filenames(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            yield os.path.join(folder_path, filename)


def get_dialogue(dfs_rows, folder_path):
    """
    Output: {dialogue_id: [dialogue_id,character_id,origin_dialogue,translated_dialogue]}
    """
    dialogue_ids = [_id for _id,_ in dfs_rows]
    dialogue_stack = {}
    filenames = get_filenames(folder_path)
    for filename in filenames:
        with open(filename, mode="r", encoding="latin-1") as csvfile:
            csv_text = csvfile.read()
        for dialogue_id in dialogue_ids:
            if dialogue_id in dialogue_stack:
                continue
            start_index = csv_text.find(dialogue_id)
            end_index = csv_text.find("\n",start_index)
            if start_index != -1 and end_index != -1:
                dialogue = csv_text[start_index : end_index]
                dialogue_stack[dialogue_id] = dialogue.split(";")
            if set(dialogue_stack.keys()) == set(dialogue_ids):
                return dialogue_stack
    
    print("🤔 dialogue not found.")


def create_cutscene_dialogue(file_path="cutscenes/INTRO.dfs"):
    string_template = get_template()
    dfs_rows = read_dfs(file_path)
    dialogue = get_dialogue(dfs_rows,folder_path="dialogues")
    result = []
    character_names = get_character_names()
    for dialogue_id,dfs_row in dfs_rows:
        character_id = dialogue[dialogue_id][1]
        text = string_template.format(
            dfs=dfs_row.strip(),
            TH_Character=character_names[character_id].get("TH",character_id),
            EN_Character=character_names[character_id].get("EN",character_id),
            TH_Dialogue=dialogue[dialogue_id][3],
            EN_Dialogue=dialogue[dialogue_id][2],
        )
        result.append(text)
    # create_file
    with open("cutscenes/cutscene_dialogue.txt", mode="w") as f:
        text = "".join(result)
        f.write(text)


if __name__ == "__main__":
    create_cutscene_dialogue()
