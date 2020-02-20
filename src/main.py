
from PyQt5 import uic
from PyQt5.Qt import QApplication, QMainWindow, QThread, pyqtSignal
import sys
from PyQt5.QtWidgets import QTableWidgetItem

# thread class
class Solve(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self,sudoku):
        super(Solve, self).__init__()
        self.sudocu = sudoku
    
    # Try to insert number in a cell
    def tryfornum(self, y, x, num):
        for i in range(0,9):
            if self.sudocu[y][i] == num:
                return False
        for i in range(0,9):
            if self.sudocu[i][x] == num:
                return False
        
        x_ = (x//3)*3
        y_ = (y//3)*3
        for i in range(0,3):
            for j in range(0,3):
                if self.sudocu[y_+i][x_+j] == num:
                    return False
        return True

    
    def solve(self):
        for y in range(9):
            for x in range(9):
                
                if self.sudocu[y][x] == 0:
                    for n in range(1,10):
                        if self.tryfornum(y, x, n):
                            self.sudocu[y][x] = n
                            result = self.solve()
                            if result == None:
                                self.sudocu[y][x] = 0
                            else:
                                return result
                    return
        return "risolto"

    def run(self):
        self.solve()
        self.signal.emit([self.sudocu])

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Default sudoku
        self.sudoku = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
        ]

        self.changeScreen("mainWin.ui",self.mainWin)

    def changeScreen(self, fileUi, nextFunct=""):
        self.__nextFunct = nextFunct
        uic.loadUi(fileUi, self)
        if self.__nextFunct != "":
            self.__nextFunct()
        self.show()
    
    # Load default sudoku or solved sudoku
    def loadSudoku(self, _sudoku=""):
        if _sudoku == "":
            _sudoku = self.sudoku
        else:
            _sudoku = _sudoku[0]

        # Add number to grid
        for y in range(9):
            for x in range(9):
                if _sudoku[y][x] != 0:
                    item = QTableWidgetItem(str(_sudoku[y][x]))
                else:
                    item = QTableWidgetItem("")
                self.tableSudoku.setItem(y,x,item)

    # Load sudoku to be solved in self.sudoku
    def storeSudoku(self):
        for y in range(9):
            for x in range(9):
                if self.tableSudoku.item(y,x).text() != "":
                    self.sudoku[y][x] = int(self.tableSudoku.item(y,x).text())
                else:
                    self.sudoku[y][x] = 0

    # Start thread to solve sudoku
    def solveTable(self):
        self.storeSudoku()

        self.thread = Solve(self.sudoku)
        self.thread.signal.connect(self.loadSudoku)
        self.thread.start()

    # Clear grid
    def clearTable(self):
        for y in range(9):
            for x in range(9):
                item = QTableWidgetItem("")
                self.tableSudoku.setItem(y,x,item)

    # Main funct
    def mainWin(self):
        self.loadSudoku()
        self.solveBtn.clicked.connect(lambda: self.solveTable())
        self.clearBtn.clicked.connect(lambda: self.clearTable())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
