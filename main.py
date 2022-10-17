from tkinter import *
import settings
import utils 
from cell import Cell


root = Tk()  # instantiate a window instance

# Override the settings of the window 
root.configure(bg="black")  # color of the window background
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')  # change the size of the window
root.title("Minesweeper Game")  # title of the window
root.resizable(False,False)  # don't resize width(false), height(false)

top_frame = Frame(
    root,
    bg='black',  # change later 
    width=settings.WIDTH,
    height=utils.height_percentage(25)
)

top_frame.place(x=0, y=0)  # from which pixel it starts, origin is top left from the 1440,720

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text=r"Ntelo's Minesweeper Game",
    font=('',36)
)

game_title.place(
    x=utils.width_percentage(25), y=0
)

left_frame = Frame(
    root,
    bg='black',  # change later
    width=utils.width_percentage(25),
    height=utils.height_percentage(75)
)

left_frame.place(x=0, y=utils.height_percentage(25))

center_frame = Frame(
    root,
    bg="green",  #change later
    width=utils.width_percentage(75),
    height=utils.height_percentage(75)
)
center_frame.place(
    x=utils.width_percentage(25),
    y=utils.height_percentage(25)
)

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x, row=y
        )

# Call the label from the Cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(
    x=0, y=0
)

Cell.randomize_mines()

# Run the window
root.mainloop()  # run till I close you