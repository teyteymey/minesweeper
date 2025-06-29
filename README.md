## What is this
This code is part of a project for CS50AI course by Harvard university. The ask was to code an AI that is able to play Minesweepere optimally. For these, I implemented the following functions:

### Sentence Class

#### `known_mines`
- Returns a `set` of all the cells in `self.cells` that are **known to be mines**.

#### `known_safes`
- Returns a `set` of all the cells in `self.cells` that are **known to be safe**.

#### `mark_mine(cell)`
- Checks if `cell` is in `self.cells`.
- If it is:
  - Removes `cell` from the sentence.
  - Updates the sentence to remain logically consistent given that `cell` is a mine.
- If `cell` is **not** in the sentence, no action is taken.

#### `mark_safe(cell)`
- Checks if `cell` is in `self.cells`.
- If it is:
  - Removes `cell` from the sentence.
  - Updates the sentence to remain logically consistent given that `cell` is safe.
- If `cell` is **not** in the sentence, no action is taken.

### MinesweeperAI Class

#### `add_knowledge(cell, count)`
- Accepts a `cell` (tuple `(i, j)`) and its corresponding `count` (number of neighboring mines).
- Updates:
  - `self.moves_made`
  - `self.mines`
  - `self.safes`
  - `self.knowledge`
- Actions:
  - Marks the cell as a move made.
  - Marks the cell as **safe** and updates any sentences containing it.
  - Adds a **new sentence** to the knowledge base reflecting that `count` of the cell’s **unknown neighbors** are mines.
  - Infers new **safe** or **mine** cells from the current knowledge.
  - Infers new sentences using the **subset method** described in the Background.
  - Recursively updates knowledge until no new inferences can be made.

#### `make_safe_move()`
- Returns a move `(i, j)` that is:
  - Known to be **safe**
  - Has **not already been made**
- If no such move exists, returns `None`.
- **Does not** modify:
  - `self.moves_made`
  - `self.mines`
  - `self.safes`
  - `self.knowledge`

#### `make_random_move()`
- Returns a **random** move `(i, j)` that:
  - Has **not been made**
  - Is **not known to be a mine**
- If no such moves exist, returns `None`.


## Usage:
Requires Python(3) and Python package installer pip(3) to run:

Install requirements: pip3 install -r requirements.txt

Run Game: python3 runner.py

