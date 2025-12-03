Module Architecture:
The module is organized into functions for loading data, validating it, parsing text blocks, and creating default files. Each part has a clear responsibility so the game can reliably use quests and items.

Exception Strategy:
The code raises specific custom exceptions when files are missing, incorrectly formatted, or corrupted. This helps the game understand exactly what went wrong and react appropriately.

Design Choices:
Text files were used for easy editing, validation was separated for clarity, and custom exceptions make debugging clearer. Default files are generated to prevent startup errors and help new users.

AI Usage:
I used AI to help write comments, clarify the code’s structure, and create short explanations. All main code decisions and logic were written by me.

How to Play:
Run the main game file, create a character when prompted, explore quests and items, and play through battles. The module loads data automatically, and progress is saved when exiting.
