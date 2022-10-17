from tkinter import Button, Label
from random import sample
from settings import MINES_COUNT, CELL_COUNT
import ctypes
import sys

class Cell:
    all = []
    cell_count=CELL_COUNT
    cell_count_label_object = None
    # constructor class
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_flag = False
        self.is_question = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
            #image=None,
            #text=f'{self.x},{self.y}'  # if you want to print a text in the middle of a cell
        )
        btn.bind('<Button-1>', self.left_click_actions)  # Left Click
        btn.bind('<Button-3>', self.right_click_actions)  # Right Click
        self.cell_btn_object = btn

    @staticmethod  # useful for the class, not the instances
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg='white',
            text=f"Cells Left:{CELL_COUNT}",
            width=12,
            height=4,
            font=("",30)  # size of the font and which font is used
        )
        Cell.cell_count_label_object = lbl

    def show_mine(self):
        # interrupt the game and show a message that the player lost
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()
        
    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the x,y values
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property  # it allows you to access the return of this function like a property of the class 
    def surrounded_cells(self):  # find all the 8 surrounding cells of a middle cell
        cells = [
            self.get_cell_by_axis(self.x-1, self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x, self.y+1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property  
    def surrounded_cells_mines_length(self):
        counter = 0 
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)  # shows the amount of mines around this cell
            # Replaces the cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # If this is a flag, change the color to the button color
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )

        # Mark this cell as opened
        self.is_opened = True

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0 :
                for cell_object in self.surrounded_cells:
                    cell_object.show_cell()
            self.show_cell()   
            # if you have found all the mines
            if Cell.cell_count == MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations, you won the game!', 'Game Over', 0)
                sys.exit()

        # Cancel left and right click events now that the events are opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def right_click_actions(self, event):
        if not self.is_flag and not self.is_question:
            self.cell_btn_object.configure(
                bg="orange"
            )
            self.is_flag = True
        elif self.is_flag:
            self.cell_btn_object.configure(
                bg="purple"
            )
            self.is_flag = False
            self.is_question = True
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_flag = False
            self.is_question = False

    @staticmethod
    def randomize_mines():
        picked_cells = sample(Cell.all, MINES_COUNT)  # find which cells will be mines
        for picked_cell in picked_cells:  # convert Cell objects to mines
            picked_cell.is_mine = True


    # __repr__ is a special method used to represent a class’s objects as a string.
    # You can define your own string representation of your class objects using the __repr__ method.
    # Special methods are a set of predefined methods used to enrich your classes. They start and end with double underscores.
    # Example Cell object before the change of the __repr__ function: <cell.Cell object at 0x000001382425A340>
    # Example Cell object after the change of the __repr__ function: Cell(0, 0)
    # __repr__ is used to compute the “official” string representation of an object and is typically used for debugging.
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"