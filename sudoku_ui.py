import string
from datetime import datetime
import PySimpleGUI as sg

# UI Settings
sg.theme('DarkBlue12')
l_font = ("Microsoft YaHei UI", 12)
pun = set(string.punctuation)
selection = None

# init
vis = False
mod = ["None"]
domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

s_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# SOLVE FUNCTIONS
def clear_map(m):
    for i in range(9):
        for j in range(9):
            m[i][j] = 0
            win[(i, j)].Update(disabled=False)
            win[(i, j)].Update(text="", button_color=("white", "#5069a9"))


def read_map(m):
    for i in range(9):
        for j in range(9):
            if win[(i, j)].get_text() == "":
                m[i][j] = 0
            else:
                m[i][j] = int(win[(i, j)].get_text())
    upd_map(m)


def check_square(m, num, pos):
    for i in range(9):
        if m[pos[0]][i] == num and pos[1] != i:  # check row
            return 0

    for i in range(9):
        if m[i][pos[1]] == num and pos[0] != i:  # check col
            return 0

    mini_x = pos[1] // 3  # check mini-grid
    mini_y = pos[0] // 3

    for i in range(3 * mini_y, 3 * mini_y + 3):
        for j in range(3 * mini_x, 3 * mini_x + 3):
            if m[i][j] == num and (i, j) != pos:
                return 0

    return 1


def find_next(m):  # return the next empty square
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == 0:
                if vis:
                    win[(i, j)].Update(disabled_button_color=("black", "khaki2"))
                    win.read(timeout=int((1 / spd) * 50))
                    win[(i, j)].Update(disabled_button_color=("white", "#5069a9"))
                    upd_map(m)
                return i, j


def print_map(m):
    for i in range(len(m)):
        if i % 3 == 0 and i != 0:
            print("— — — — — — — — — — — ")

        for j in range(len(m[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")

            if j == 8:
                print(m[i][j])
            else:
                print(str(m[i][j]) + " ", end="")


def solve(m):
    if mod[0] == "None":
        emp = find_next(m)
        if emp:
            y, x = emp
        else:
            return 1

        for i in range(1, 10):
            if check_square(m, i, (y, x)):
                m[y][x] = i

                if solve(m):
                    return 1

            m[y][x] = 0

        return 0
    if mod[0] == "Forward Checking":
        emp = find_next(m)
        if emp:
            y, x = emp
        else:
            return 1  # finished solving

        for i in domain:
            if check_square(m, i, (y, x)):
                m[y][x] = i
                domain.remove(i)

                if solve(m):
                    for j in range(9):
                        domain[j] = j
                    return 1
            domain.insert(i, i)
            m[y][x] = 0

        return 0
    if mod[0] == "Minimum Remaining Values":
        return 0
    if mod[0] == "Hill Climbing":
        return 0
    if mod[0] == "Random Restart":
        return 0


def generate_solution(m):
    # print("**INPUT**")
    # print_map(s_map)
    start = datetime.now()
    solve(m)
    sol_time = (datetime.now() - start).total_seconds()
    upd_map(m)
    # print("\n\n**OUTPUT**")
    # print_map(s_map)
    print("\nSolved in " + str(sol_time * 1000) + " ms (" + str(sol_time) + " seconds)" + " [BACKTRACKING]")


# UI FUNCTIONS
def upd_map(m):  # populate values in the ui grid
    for i in range(9):
        for j in range(9):
            if m[i][j] == 0:
                win[(i, j)].Update(text="", disabled_button_color=("white", "#5069a9"))
            else:
                win[(i, j)].Update(text=m[i][j], disabled=True)


def settings():  # "copy" settings window layout each time it is opened
    s_layout = [[sg.Text("Modification:",
                         font=l_font)],
                [sg.Listbox(size=(558, 6),
                            values=(
                                "None", "Forward Checking", "Minimum Remaining Values", "Hill Climbing",
                                "Random Restart"),
                            key="in_mod",
                            default_values=["None"],
                            font=l_font)],
                [sg.Text("\nVisualizer ————————————————————————",
                         font=l_font)],
                [sg.Checkbox("Enable Visualizer",
                             key="in_vis",
                             font=l_font)],
                [sg.Text("Visualizer Speed:",
                         font=l_font),
                 sg.Slider(range=(1, 3),
                           orientation="h",
                           default_value=2,
                           size=(50, 15),
                           key="in_speed",
                           font=l_font,
                           pad=((0, 0), (0, 20)))],
                [sg.Text("")],
                [sg.Button("Apply",
                           font=l_font,
                           size=(7, 1),
                           border_width=0,
                           pad=((142, 0), (0, 15))),
                 sg.Button("Cancel",
                           font=l_font,
                           size=(7, 1),
                           border_width=0,
                           pad=((10, 0), (0, 15)))]]
    return sg.Window("Settings", s_layout, size=(300, 320), use_default_focus=False, finalize=True)


# UI CREATION
main_layout = [
    [sg.Text("Sudoku Solver",  # title
             font=("Microsoft YaHei UI", 20),
             pad=((5, 0), (10, 0))),
     sg.Button("Settings",  # settings button
               pad=((500, 0), (10, 0)),
               border_width=0,
               font=("Microsoft YaHei UI Light", 15))],
    [sg.Text("_" * 500)],
    [sg.Text("                  Modification: None | Visualizer: False | Speed: N/A                  ",
             # settings display
             key="stats",
             font=("Microsoft YaHei UI Light", 14),
             pad=((0, 0), (0, 5)))],
    [[sg.Frame("", [[sg.Button("", size=(2, 2),
                               font=("Microsoft YaHei UI", 12),
                               pad=(1, 1),
                               key=(mini_y * 3 + row, mini_x * 3 + col),
                               border_width=0,
                               mouseover_colors=("seashell2", "seashell2"),
                               disabled_button_color=("white", "#606982"))
                     for col in range(3)] for row in range(3)], pad=(1, 1), border_width=0)  # create mini-grid
      for mini_x in range(3)] for mini_y in range(3)],  # duplicate mini-grid 9 times (big rows/cols)
    [sg.Button("Reset",
               pad=((0, 0), (25, 0)),
               border_width=0,
               size=(5, 1),
               font=("Microsoft YaHei UI Light", 15)),
     sg.Button("Solve",
               pad=((5, 0), (25, 0)),
               border_width=0,
               size=(5, 1),
               font=("Microsoft YaHei UI Light", 15))]
]

win = sg.Window("Sudoku Solver", main_layout, use_default_focus=False, element_justification="c", size=(800, 700),
                finalize=True, return_keyboard_events=True)

# BUTTON FUNCTIONS
while True:
    event, values = win.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Settings":  # opens settings window
        s_win = settings()
        event2, values = s_win.read()
        if event2 == "Apply":
            print(values["in_mod"], "|", values["in_vis"], "|", values["in_speed"])
            mod = values["in_mod"]
            vis = values["in_vis"]
            if not vis:
                spd = "N/A"
            else:
                spd = int(values["in_speed"])
            win["stats"].Update("Modification: " + mod[0] + " | Visualizer: " + str(vis) + " | Speed: " + str(spd))
            s_win.close()
        elif event2 == "Cancel":
            s_win.close()
    elif (type(event) is tuple) and event >= (0, 0):  # called when square is pressed
        print(event, " was pressed, waiting for input")
        if selection is not None:
            win[selection].Update(button_color=("white", "#5068A9"), text="")
        win[event].Update(button_color=("seashell2", "seashell2"))
        selection = event
    if (len(event) == 1) and (selection is not None):  # called when a square is selected and a key is pressed
        try:
            if int(event) > 0:
                win[selection].Update(text=event, button_color=("white", "#606982"))
                print(event, "was input at", selection)
                selection = None
        except TypeError and ValueError:  # ignores key pressed if it is not an integer
            pass
    if event == "Reset":
        if selection is not None:
            win[selection].Update(button_color=("white", "#5068A9"))
            selection = None
        clear_map(s_map)
    if event == "Solve":
        if selection is not None:
            win[selection].Update(button_color=("white", "#5068A9"))
            selection = None
        read_map(s_map)
        print_map(s_map)
        generate_solution(s_map)
        print_map(s_map)

win.close()
