# How to translate the game? 

0. Install Python 2.7
1. Get last *.LUB files from Psychonauts\WorkResource\Localization\English
2. Run: python unpack_strings.py AS_StringTable.lub 
3. AS_StringTable.csv should appear next to the AS_StringTable.lub
4. Change the ASCII-text of AS_StringTable.csv in a text editor or Excel
5. Keep in mind that csv strings are separated by the '\r\n', but inside one in-game string - '\n'
6. Run: python replace_strings.py AS_StringTable.lub AS_StringTable.csv AS_StringTable_new.lub
7. Replace original game file with the new one
8. If your language contains not only Latin letters, you must replace Psychonauts\WorkResource\Fonts\*.dff
9. Check the game, everything should work
