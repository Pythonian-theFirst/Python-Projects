import turtle
import time

# ---------- SETUP ----------
screen = turtle.Screen()
screen.setup(900, 600)
screen.bgcolor("black")
screen.title("MS-DOS Executive")
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# ---------- DATA ----------
menus = ["File", "View", "Special"]
menus_dict = {
    "File": ["Open", "Close", "Exit"],
    "View": ["Details", "Icons", "Refresh"],
    "Special": ["Run", "Properties", "Help"]
}

current_path = "C:\\"
files = ["NOTEPAD.EXE", "CALC.EXE", "PAINT.EXE", "WRITE.EXE", "CLOCK.EXE", "README.TXT"]
rows = 6

selected = 0
selected_menu = 0
mode = "files"  # "files" or "menu"
windows = []

# ---------- DRAWING ----------
def draw_rect(x, y, w, h, color):
    pen.penup()
    pen.goto(x, y)
    pen.setheading(0)
    pen.color(color)
    pen.begin_fill()
    for _ in range(2):
        pen.forward(w)
        pen.right(90)
        pen.forward(h)
        pen.right(90)
    pen.end_fill()

def draw_window(title, content, wx, wy):
    window_width = 300
    title_height = 25
    padding_x = 10
    padding_y = 10

    # Make README wider
    if title == "README.TXT":
        extra_width = 40
        wx -= extra_width
        window_width += extra_width

    # Split content into lines
    lines = content.split("\n")
    line_height = 15
    window_height = max(title_height + padding_y*2 + len(lines)*line_height, 140)

    # Draw window
    draw_rect(wx, wy, window_width, window_height, "lightgray")
    draw_rect(wx, wy, window_width, title_height, "blue")

    # Title
    pen.goto(wx + padding_x, wy - 20)
    pen.color("white")
    pen.write(title, font=("Courier", 10, "bold"))

    # Content offset
    content_offset = 20 if title == "README.TXT" else 5
    start_y = wy - title_height - padding_y - content_offset
    for i, line in enumerate(lines):
        pen.goto(wx + padding_x, start_y - i*line_height)
        pen.color("black")
        pen.write(line, font=("Courier", 10, "normal"))

def draw_ui():
    pen.clear()
    # TITLE BAR
    draw_rect(-450, 300, 900, 30, "blue")
    pen.goto(-150, 280)
    pen.color("white")
    pen.write("MS-DOS Executive", font=("Courier", 12, "bold"))

    # MENU BAR
    draw_rect(-450, 270, 900, 30, "lightgray")
    x = -430
    for i, m in enumerate(menus):
        w = len(m) * 9
        if mode == "menu" and i == selected_menu:
            draw_rect(x - 5, 268, w + 10, 20, "blue")
            pen.color("white")
        else:
            pen.color("black")
        pen.goto(x, 250)
        pen.write(m, font=("Courier", 12, "normal"))
        x += w + 30

    # PATH BAR
    draw_rect(-450, 240, 900, 30, "white")
    pen.goto(-430, 220)
    pen.color("black")
    pen.write(current_path, font=("Courier", 12, "normal"))

    # MAIN AREA
    draw_rect(-450, 210, 900, 450, "white")
    # FILES
    for i, file in enumerate(files):
        col = i // rows
        row = i % rows
        x = -430 + col * 300
        y = 180 - row * 22
        if mode == "files" and i == selected:
            draw_rect(x - 10, y + 17, 260, 20, "blue")
            pen.color("white")
        else:
            pen.color("black")
        pen.goto(x, y)
        pen.write(file, font=("Courier", 12, "normal"))

    # WINDOWS
    for i, win in enumerate(windows):
        wx = -400 + (i % 2) * 350
        wy = 60 - (i // 2) * 180
        draw_window(win["title"], win["content"], wx, wy)

# ---------- FILE ACTIONS ----------
def open_selected_file():
    global windows
    file = files[selected]

    if file == "NOTEPAD.EXE":
        windows.append({"title": "Notepad", "content": "Simple text editor"})
    elif file == "CALC.EXE":
        windows.append({"title": "Calculator", "content": "2 + 2 = 4"})
    elif file == "PAINT.EXE":
        windows.append({"title": "Paint", "content": "Drawing program"})
    elif file == "WRITE.EXE":
        windows.append({"title": "Write", "content": "Word processor"})
    elif file == "CLOCK.EXE":
        windows.append({"title": "Clock", "content": time.strftime("%H:%M:%S")})
    elif file == "README.TXT":
        windows.append({
            "title": "README.TXT",
            "content": (
                "• Microsoft MS-DOS Operating System 6.2\n"
                "• Microsoft Windows 1.01\n"
                "• Copyright Microsoft Corp.\n\n"
                "System Features:\n"
                "- File management\n"
                "- Program launching\n"
                "- Basic applications\n\n"
                "Memory: 640 KB\n"
                "Drives: A:\\  C:\\\n\n"
                "Use arrow keys to navigate."
            )
        })
    draw_ui()

# ---------- MENU ACTIONS ----------
def open_menu_option():
    global windows
    menu_name = menus[selected_menu]
    option = menus_dict[menu_name][0]  # always first for simplicity

    if menu_name == "File":
        if option == "Open":
            open_selected_file()  # open the highlighted file
        elif option == "Close":
            if windows:
                windows.pop()  # close top window
        elif option == "Exit":
            screen.bye()  # exit program

    elif menu_name == "View":
        if option == "Details":
            # Show file list in main area (already done by default)
            draw_ui()
        elif option == "Icons":
            # For now, just refresh main area
            draw_ui()
        elif option == "Refresh":
            draw_ui()

    elif menu_name == "Special":
        if option == "Run":
            open_selected_file()  # run highlighted file
        elif option == "Properties":
            file = files[selected]
            windows.append({
                "title": f"{file} Properties",
                "content": (
                    f"File: {file}\n"
                    f"Size: 640 KB\n"
                    f"Type: EXE\n"
                    f"Created: 01/01/1985"
                )
            })
        elif option == "Help":
            windows.append({"title": "Help", "content": "MS-DOS Executive Help"})

    draw_ui()

# ---------- CONTROLS ----------
def up():
    global selected
    if mode == "files" and selected > 0:
        selected -= 1
    draw_ui()

def down():
    global selected
    if mode == "files" and selected < len(files) - 1:
        selected += 1
    draw_ui()

def left():
    global selected_menu, selected
    if mode == "files":
        if selected - rows >= 0:
            selected -= rows
    else:
        if selected_menu > 0:
            selected_menu -= 1
    draw_ui()

def right():
    global selected_menu, selected
    if mode == "files":
        if selected + rows < len(files):
            selected += rows
    else:
        if selected_menu < len(menus) - 1:
            selected_menu += 1
    draw_ui()

def switch_mode():
    global mode
    mode = "menu" if mode == "files" else "files"
    draw_ui()

def enter_key():
    if mode == "files":
        open_selected_file()
    else:
        open_menu_option()

def close_window():
    if windows:
        windows.pop()
    draw_ui()

# ---------- KEY BINDINGS ----------
screen.listen()
screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")
screen.onkey(switch_mode, "Tab")
screen.onkey(enter_key, "Return")
screen.onkey(close_window, "Escape")

# ---------- START ----------
draw_ui()
turtle.done()
