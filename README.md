<center>
<img src="https://static.wikia.nocookie.net/psychonauts/images/2/21/Tumblr_m5h0k8g0kQ1qjm1bzo1_500.png/revision/latest?cb=20120822013745"
width="200" 
height="150" />
<h1>🧠 psychonauts-TH-translation 🧠</h1>

<b>EN</b> |
<a href="https://github.com/Onyx-Nostalgia/psychonauts-TH-translation/blob/master/docs/README-TH.md">TH</a>

<img src="http://ForTheBadge.com/images/badges/made-with-python.svg"/>
</center>

----------------------------

It is a translation of the game Psychonauts into **Thai**. It will collect the Dialogues files that have been translated into **Thai**.

The extraction code and replacement code are originally from [TrupSteam/psychonauts-translator](https://github.com/TrupSteam/psychonauts-translator) and have been further developed to support python3.X.

# 🧠 What have we here ?
- Extract dialogues from game file (`.lub` file) to csv
- [dialogues/](/dialogues) to store csv file of dialogues that are being translated or have been translated
- [cutscenes/](/cutscenes) to store dialogue files according to cutscenes for easy translation
  
# 🧠 Dialogues csv file
see sample in [dialogues/](/dialogues)

| id        | character | origin_dialogue      | translated_dialogue       |
| --------- | --------- | -------------------- | ------------------------- |
| CABD001RA | RA        | Dogen! Are you okay? | โดแกน! นายไม่เป็นอะไรใช่ไหม? |

**id**: There will be 9 characters consisting of 3 UPPER Characters + 3 numbers + 2 UPPER Characters, where the last 2 characters are an abbreviation of the name of the character being spoken.

**character**: It is derived from the last two characters of `id` and is like an abbreviation of the character name or you can view it as a "character id". We will store the character abbreviation and the full name in a separate file named [character_name.json](/character_name.json).

**origin_dialogue**: The original English dialogue, some of which may contain special characters such as `\n`.

**translated_dialogue**: Column for adding Thai translations

**Note:** File CSV use delimeter `;` and endline `\r\n`

# 🧠 Pre-request
- Install Python 3.X (recommend 3.10+)

**Comming Soon !!** 
- Workspace to Easy Development
  - Docker
  - Devcontainer

# 🧠 Extract dialogue from game file
The game will store dialogue files in a path like this `Psychonauts/WorkResource/Localization/English/**_StringTable.lub`
Which can be extracted into a CSV file using the command

## Extract each dialogue file
Example: Need a CSV file of dialogue from `AS_StringTable.lub`
```bash
python unpack_strings.py --file AS_StringTable.lub
```
You will get a file `dialogues/AS_StringTable.csv`

## Extract all file in folder
Example: Need a CSV file of all dialogues from `Psychonauts/WorkResource/Localization/English`
```bash
python unpack_strings.py --folder Psychonauts/WorkResource/Localization/English
```
The file will be in `dialogues/`

## Optional
Sometimes if you want to change the destination folder where you want to save the csv from `dialogues/` to another folder, you can do it by adding the `--dest` flag, for example:
```bash
python unpack_strings.py --folder Psychonauts/WorkResource/Localization/English --dest new_dialogues/
```
