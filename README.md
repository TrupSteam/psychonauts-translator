# 🧠 psychonauts-TH-translation

It is a translation of the game Psychonauts into Thai. It will collect the Dialogues files that have been translated into Thai.

The extraction code and replacement code are originally from [TrupSteam/psychonauts-translator](https://github.com/TrupSteam/psychonauts-translator) and have been further developed to support python3.X.


# How to translate the game? 

0. Install Python 3.X
1. Get last *.LUB files from `Psychonauts\WorkResource\Localization\English`
2. Run: `python unpack_strings.py AS_StringTable.lub` 
3. `AS_StringTable.csv` should appear next to the `AS_StringTable.lub`
4. Change the ASCII-text of `AS_StringTable.csv` in a text editor
5. Keep in mind that csv strings are separated by the '\r\n', but inside one in-game string - '\n'
6. Run: `python replace_strings.py AS_StringTable.lub AS_StringTable.csv AS_StringTable_new.lub`
7. Replace original game file with the new one
8. If your language contains not only Latin letters, you must replace `Psychonauts\WorkResource\Fonts\*.dff`
9. Check the game, everything should work

# Fonts

1. Check that you are using single-byte encoding in the hex-editor!
2. See how these bytes are displayed with standard fonts:

```
30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F
40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F
60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F
70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F
80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F
90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F
A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF
B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF
C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF
E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB EC ED EE EF
F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF
```

![psychonauts-char_full_eng](/docs/images/char_full_eng.jpg)
![psychonauts-char_full_eng](/docs/images/char_full_rus.jpg)

