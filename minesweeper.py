import itertools
import random
import numpy as np


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (self.count != 0 and self.count == len(self.cells)):
            return self.cells
        return set()
    
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (self.count == 0):
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # print("sentence mark mine " + str(self))
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        # print("end sentence mark mine " + str(self))


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # print("sentence mark safe " + str(self))
        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)
        # print("end sentence mark safe " + str(self))


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        print("ai mark mine " + str(self))
        self.mines.add(cell)
        to_remove = []
        for sentence in self.knowledge:
            # if all cells are mines or only one cell left that is a mine, remove the sentence cuz info is already not useful
            if sentence.count == len(sentence.cells) or sentence.cells == cell:
                print("remove sentence")
                to_remove.append(sentence)
            else:
                sentence.mark_mine(cell)

        for sentence in to_remove:
            self.knowledge.remove(sentence)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # print("ai mark safe " + str(cell))
        self.safes.add(cell)
        to_remove = []
        for sentence in self.knowledge:
            # remove sentence if we know all cells are safe already
            if sentence.count == 0:
                print("remove sentence")
                to_remove.append(sentence)
            else:
                sentence.mark_safe(cell)
        
        for sentence in to_remove:
            self.knowledge.remove(sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print()
        print()
        print("ADD KNOWLEDGE")
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Get neighbours and get unknown ones only
        neighbour_cells = self.neighbours(cell)
        unexplored_cells = neighbour_cells.difference(self.safes, self.moves_made)
        not_counting_mines = len(unexplored_cells)
        unexplored_cells.difference_update(self.mines)
        if (unexplored_cells != set()):
            new_knowledge = Sentence(unexplored_cells, count-(not_counting_mines-len(unexplored_cells)))
            self.knowledge.append(new_knowledge)

        #sabemos que 2,3 es una mina. de los 8 neighbours quitamos los safe y los moves made para saber los restantes que son minas. si quitamos las minas de alrededor sabemos cuantas minas hay
        # si restamos el len del set primero menos las minas que hay alrededor que sabemos
        self.infer_knowledge()

        self.resolve_cells_from_knowledge()


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("safe cells: " + str(self.safes))
        safe_cells = self.safes.difference(self.moves_made)
        print("safe cells that are allowed: " + str(safe_cells))
        if len(safe_cells) != 0:
            return safe_cells.pop()
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = set()
        for i in range (0,self.height):
            for j in range(0, self.width):
                all_cells.add((i, j))

        possible_moves = all_cells.difference(self.moves_made, self.mines)

        if possible_moves != set():
            return possible_moves.pop()

        return None
    
    def neighbours(self, cell):
        neighbours = set()
        for i in range (-1,2):
            for j in range(-1,2):
                neighbours.add((cell[0]+i, cell[1]+j))

        #remove self
        neighbours.remove(cell)
        # remove cells that are out of board in a very cool way hehehe
        neighbours.difference_update({cell for cell in neighbours if any(x in {-1, 8} for x in cell)})
        return neighbours
    
    # Used to get new knowledge from existing sentences
    def infer_knowledge(self):
        print("infer knowledge")
        print("current knowledge to infer from: ")
        new_knowledge =  []
        used_knowledge = []
        for sentence1 in self.knowledge:
            print(str(sentence1))
            for sentence2 in self.knowledge:
                if sentence1.cells.issubset(sentence2.cells) and sentence1 != sentence2 and sentence1.count >= 1 and sentence2.count >= 1:
                    inferred_cells = sentence2.cells.difference(sentence1.cells)
                    inferred_count = sentence2.count - sentence1.count
                    inferred_sentence = Sentence(inferred_cells, inferred_count)
                    print(str(sentence1) + " is subset of " + str(sentence2))
                    print("INFERRED SENTENCE")
                    print(str(inferred_sentence))
                    if (inferred_cells == set()):
                        raise RuntimeError("Inconsistent knowledge") 
                    new_knowledge.append(inferred_sentence)
                    used_knowledge.append(sentence2)
                
        
        # do it separately to avoid writing while iterating
        for sentence in new_knowledge:
            #sometimes we infer the same from different sentences
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)

        for sentence in used_knowledge:
            #sometimes we use the same sentence to infer and it is already removed
            if sentence in self.knowledge:
                self.knowledge.remove(sentence)

    # Check if we can mark any cell as mine or safe
    def resolve_cells_from_knowledge(self):
        print()
        print(" @@@@@@ resolve cells from knowledge")
        safe_cells = set()
        mine_cells = set()
        print("current knowledge: ")
        for sentence in self.knowledge:
            print(str(sentence))
            safe_cells.update(sentence.known_safes())

            mine_cells.update(sentence.known_mines())

        print("mark safe cells  " + str(safe_cells))
        for cell in safe_cells:
            self.mark_safe(cell)

        print("mark mine cells  " + str(mine_cells))
        for cell in mine_cells:
            self.mark_mine(cell)


