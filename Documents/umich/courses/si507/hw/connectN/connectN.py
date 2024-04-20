# %% [markdown]
# 

# %%
from enum import Enum

'''
This is the start of the HW.
If there is any conflict between the doc string and the HW document,
please follow the instruction in the HW document.
Good Luck and have fun !
'''

class Notation(Enum):
    """Enumeration for representing different types of notations in the game.

    Attributes:
        EMPTY (int): Represents an empty cell on the board.
        PLAYER1 (int): Represents a cell occupied by Player 1.
        PLAYER2 (int): Represents a cell occupied by Player 2.
    """
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

class Player:
    """Represents a player in the game.

    Attributes:
        __playerName (str): The name of the player.
        __playerNotation (Notation): The notation (symbol) used by the player on the board.
        __curScore (int): The current score of the player.

    Args:
        playerName (str): The name of the player.
        playerNotation (Notation): The notation (symbol) used by the player.
        curScore (int): The initial score of the player.
    """

    def __init__(self, playerName, playerNotation, curScore):
        self.__playerName = playerName
        self.__playerNotation = playerNotation
        self.__curScore = curScore

    def display(self) -> str:
        """Displays the player's details including name, notation, and current score."""
        print(f"{self.__playerName}'s score ({self.__playerNotation}): {self.__curScore}")

    def addScoreByOne(self):
        """Increments the player's score by one."""
        self.__curScore += 1

    def getScore(self):
        """Returns the current score of the player."""
        return self.__curScore

    def getName(self):
        """Returns the name of the player."""
        return self.__playerName

    def getNotation(self):
        """Returns the notation used by the player."""
        return self.__playerNotation

class Board:
    """Represents the game board.

    Attributes:
        __rowNum (int): Number of rows in the board.
        __colNum (int): Number of columns in the board.
        __grid (list): 2D list representing the game board.

    Args:
        rowNum (int): Number of rows in the board.
        colNum (int): Number of columns in the board.
    """

    def __init__(self, rowNum, colNum) -> None:
        self.__rowNum = rowNum
        self.__colNum = colNum
        #fill grid with empty notations
        self.__grid = [[Notation.EMPTY for _ in range(colNum)] for _ in range(rowNum)]

    def initGrid(self):
        #https://stackoverflow.com/questions/52199986/use-enum-instances-in-another-class-in-python3
        """Initializes the game board with empty cells."""
        self.__grid = [[Notation.EMPTY for _ in range(self.__colNum)] for _ in range(self.__rowNum)]

    def getColNum(self):
        """Returns the number of columns in the board."""
        return self.__colNum

    def placeMark(self, colNum, mark):
        """Attempts to place a mark on the board at the specified column.

        Args:
            colNum (int): The column number where the mark is to be placed.
            mark (Notation): The mark to be placed on the board.

        Returns:
            bool: True if the mark was successfully placed, False otherwise.
        """
        #if the column number is outside the bounds of the board
        if colNum >= self.__colNum or colNum < 0:
            print(f"Error! {colNum} is not a valid column number!")
            return False
        #iterates over each row in reverse order, places mark at first available space
        #used chatgpt to know to use the reversed function
        for i in reversed(range(self.__rowNum)):
            if self.__grid[i][colNum] == Notation.EMPTY:
                self.__grid[i][colNum] = mark
                return True
            #returns false if column is full
            return False


    def checkFull(self):
        """Checks if the board is completely filled.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        #returns True if all cells != Notation.EMPTY, false if some are empty
        return all(cell != Notation.EMPTY for row in self.__grid for cell in row)

    def display(self):
        """Displays the current state of the board."""
        for row in self.__grid:
            print(''.join([str(cell.value) for cell in row]))

    # Private methods for internal use
    def __checkWinHorizontal(self, target):
        #iterate through rows
        for i in range(self.__rowNum):
            #iterate through columns
            for j in range(self.__colNum - target + 1):
                #if the cell is not empty
                if self.__grid[i][j] != Notation.EMPTY:
                    #if all of the row is equal to each other
                    if all(self.__grid[i][j] == self.__grid[i][j+k] for k in range(1, target)):
                        #return winner
                        return self.__grid[i][j]

    def __checkWinVertical(self, target):
        #iterate through rows
        for i in range(self.__rowNum - target + 1):
            #iterate through columns
            for j in range(self.__colNum):
                #if cell not empty
                if self.__grid[i][j] != Notation.EMPTY:
                    #if all of the cells in the column are the same
                    if all(self.__grid[i][j] == self.__grid[i+k][j] for k in range(1, target)):
                        #return winner
                        return self.__grid[i][j]


    def __checkWinOneDiag(self, target, rowNum, colNum):
        #iterate through rows and columns
        for i in range(self.__rowNum - target + 1):
            for j in range(self.__colNum - target + 1):
                if self.__grid[i][j] != Notation.EMPTY:
                    #if cells on the diagonal all equal each other, return winner
                    if all(self.__grid[i][j] == self.__grid[i+k][j+k] for k in range(1, target)):
                        return self.__grid[i][j]
        return None

    def __checkWinAntiOneDiag(self, target, rowNum, colNum):
        #iterate through rows and columns
        for i in range(self.__rowNum - target + 1):
            for j in range(target - 1, self.__colNum):
                if self.__grid[i][j] != Notation.EMPTY:
                    #if cells on diagonal equal each other, return winner
                    if all(self.__grid[i][j] == self.__grid[i+k][j-k] for k in range(1,target)):
                        return self.__grid[i][j]
        return None

    def __checkWinDiagonal(self, target):
        if self.__checkWinOneDiag(target, self.__rowNum, self.__colNum) != None:
            return self.__checkWinOneDiag(target, self.__rowNum, self.__colNum)
        if self.__checkWinAntiOneDiag(target, self.__rowNum, self.__colNum) != None:
            return self.__checkWinAntiOneDiag(target, self.__rowNum, self.__colNum)
        return None

    def checkWin(self, target):
        """Checks if there is a winning condition on the board.

        Args:
            target (int): The number of consecutive marks needed for a win.

        Returns:
            Notation or None: The notation of the winning player, or None if there is no winner.
        """
        result = self.__checkWinHorizontal(target)
        if result != None:
            return result 
        result = self.__checkWinVertical(target)
        if result != None:
            return result 
        result = self.__checkWinDiagonal(target)
        if result != None:
            return result 
        result = self.__checkWinAntiOneDiag(target, self.__rowNum, self.__colNum)
        if result != None:
            return result 
        return None

class Game:
    """Represents the game logic and flow.

    Args:
        rowNum (int): Number of rows in the game board.
        colNum (int): Number of columns in the game board.
        connectN (int): Number of consecutive marks needed for a win.
        targetScore (int): The score a player needs to reach to win the game.
        playerName1 (str): Name of the first player.
        playerName2 (str): Name of the second player.
    """

    def __init__(self, rowNum, colNum, connectN, targetScore, playerName1, playerName2) -> None:
        self.__board = Board(rowNum, colNum)
        self.__connectN = connectN
        self.__targetScore = targetScore
        self.__playerName1 = playerName1
        self.__playerName2 = playerName2
        self.__player1 = Player(playerName1, Notation.PLAYER1, 0)
        self.__player2 = Player(playerName2, Notation.PLAYER2, 0)
        self.__playerList = [self.__player1, self.__player2]
        self.__curPlayer = self.__player1

    def __playBoard(self, curPlayer):
        """Handles the process of a player making a move on the board.

        Args:
            curPlayer (Player): The current player who is making the move.
        """
        print(f"It is currently {curPlayer.getName()}'s turn ({curPlayer.getNotation().value})")
        self.__board.display()
        while True:
            col = input("Choose a column 0-3 to place your mark: ")
            try:
                #see if colnum can be an integer
                colNum = int(col)
                #if colnum is not within the bounds of the board
                if colNum < 0 or colNum >= self.__board.getColNum():
                    raise ValueError("Invalid Column. Try again. ")
                #if the mark can be placed, break the loop
                if self.__board.placeMark(colNum, curPlayer.getNotation()):
                    break
                else:
                    print("That column is full. Try another!")
            except ValueError:
                print("Invalid input. Enter a valid column.")



    def __changeTurn(self):
        """Switches the turn to the other player."""
        if self.__curPlayer == self.__player1:
            self.__curPlayer = self.__player2
        else:
            self.__curPlayer = self.__player1

    def playRound(self):
        """Plays a single round of the game."""
        self.__board.initGrid()
        self.__player1 = Player(self.__playerName1, Notation.PLAYER1, 0)
        self.__player2 = Player(self.__playerName2, Notation.PLAYER2, 0)

        while True:
            self.__playBoard(self.__curPlayer)
            if self.__board.checkWin(self.__connectN) == Notation.PLAYER1:
                print(f"{self.__player1.getName()} wins this round!")
                self.__player1.addScoreByOne()
                break
            if self.__board.checkWin(self.__connectN) == Notation.PLAYER2:
                print(f"{self.__player2.getName()} wins this round!")
                self.__player2.addScoreByOne()
                break
            if self.__board.checkFull():
                print("Nobody wins this round!")
                break
            self.__changeTurn()
        print(f"Scoreboard:\n{self.__player1.display()}\n{self.__player2.display()}")



    def play(self):
        """Starts and manages the game play until a player wins."""
        while True:
            self.playRound()
            if self.__player1.getScore() >= self.__targetScore:
                print(f"{self.__player1.getName()} wins!")
                break
            if self.__player2.getScore() >= self.__targetScore:
                print(f"{self.__player2.getName()} wins!")
                break
            again = input("Would you like to play again? (Y/N)?: ")
            if again.lower() != 'y':
                break

def main():
    """Main function to start the game."""
    game = Game(4, 4, 3, 2, 'P1', 'P2')
    game.play()

if __name__ == "__main__":
    main()



