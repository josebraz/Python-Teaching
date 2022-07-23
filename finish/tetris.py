from sys import exit
from tkinter import Tk, Canvas
from random import randint, choice
from copy import deepcopy
from utils import adjust_lightness

velocity = 2
columns = 10
lines   = 20
item_size = 30
width = item_size * columns
heigh = item_size * lines
margin = 3

EMPTY_VALUE = -1

job = None
background_color = "#b9ac9c"
empty_color = "#cdc1b5"
values_colors = ["#efff00", "#00ff00", "#6cc0ff", "#6700ff", "#ff6000", "#ff0000", "#e500ff"]
outline_colors = [adjust_lightness(color, 0.2) for color in values_colors]
light_colors = [adjust_lightness(color, 1.35) for color in values_colors]
dark_colors = [adjust_lightness(color, 0.65) for color in values_colors]

figures = {
    "figure0": (0, ((0, -1), (1, -1), (0, 0), (1, 0)), ((0, -1), (1, -1), (0, 0), (1, 0)), ((0, -1), (1, -1), (0, 0), (1, 0)), ((0, -1), (1, -1), (0, 0), (1, 0))),
    "figure1": (1, ((0, 0), (-1, 0), (0, 1), (1, 1)), ((0, 0), (0, -1), (-1, 0), (-1, 1)), ((0, 0), (-1, 0), (0, 1), (1, 1)), ((0, 0), (0, -1), (-1, 0), (-1, 1))),
    "figure2": (2, ((0, 0), (-1, 0), (1, 0), (1, 1)), ((0, 0), (0, -1), (0, 1), (-1, 1)), ((0, 0), (-1, 0), (1, 0), (-1, -1)), ((0, 0), (0, -1), (0, 1), (1, -1))),
    "figure3": (3, ((0, 0), (0, -1), (0, -2), (0, -3)), ((-2, 0), (-1, 0), (0, 0), (1, 0)), ((0, 0), (0, -1), (0, -2), (0, -3)), ((-2, 0), (-1, 0), (0, 0), (1, 0))),
    "figure4": (4, ((0, 0), (-1, 0), (1, 0), (-1, 1)), ((0, 0), (0, -1), (0, 1), (-1, -1)), ((0, 0), (1, 0), (-1, 0), (1, -1)), ((0, 0), (0, 1), (0, -1), (1, 1))),
    "figure5": (5, ((0, 0), (-1, 0), (1, 0), (0, -1)), ((0, 0), (0, -1), (0, 1), (1, 0)), ((0, 0), (1, 0), (-1, 0), (0, 1)), ((0, 0), (0, 1), (0, -1), (-1, 0))),
    "figure6": (6, ((0, 0), (-1, 0), (0, -1), (1, -1)), ((0, 0), (0, -1), (1, 0), (1, 1)), ((0, 0), (1, 0), (0, 1), (-1, 1)), ((0, 0), (0, 1), (-1, 0), (-1, -1)))
}

current_figure = ("figure6", (3, 4), 0)
old_figure = current_figure

values = [[EMPTY_VALUE for _ in range(columns)] for _ in range(lines)]
old_values = [[EMPTY_VALUE for _ in range(columns)] for _ in range(lines)]

# desenha todos os quadados do jogo
def draw_game(force = False):
    # desenha primeiro os quadrados vazios, por causa da borda
    for y, x_values in enumerate(values):
        for x, value in enumerate(x_values):
            if value == EMPTY_VALUE:
                draw_square(x, y, value, force=force)
    for y, x_values in enumerate(values):
        for x, value in enumerate(x_values):
            if value != EMPTY_VALUE:
                draw_square(x, y, value, force=force)
    draw_current_figure()

def get_figure_points(figure):
    (figure_name, (x, y), figure_orientation) = figure
    figure_desloc = figures[figure_name][figure_orientation+1]
    return [(x_desloc + x, y_desloc + y) for (x_desloc, y_desloc) in figure_desloc ]

def draw_current_figure():
    global current_figure, old_figure, values
    # apaga o desenho anterior
    if old_figure != None:
        old_points = get_figure_points(old_figure)
        for (x, y) in old_points:
            draw_square(x, y, EMPTY_VALUE, force=True)

    figure_color = figures[current_figure[0]][0]
    points = get_figure_points(current_figure)
    for (x, y) in points:
        draw_square(x, y, figure_color)

def create_rectangle_or_edit(x0, y0, x1, y1, tag, **kw):
    if w.find_withtag(tag):
        w.itemconfig(tag, kw)
    else:
        w.create_rectangle(x0, y0, x1, y1, kw)

def create_line_or_edit(x0, y0, x1, y1, tag, **kw):
    if w.find_withtag(tag):
        w.itemconfig(tag, kw)
    else:
        w.create_line(x0, y0, x1, y1, kw)  

# desenha um quadrado
def draw_square(x, y, value = EMPTY_VALUE, debug_number = -1, force = False):
    if old_values[y][x] == value and not force: 
        # otimização: não precisa redesenhar porque o valor não mudou
        return
    if value == EMPTY_VALUE:
        color = empty_color
        outline = empty_color
        light_color = empty_color
        dark_color = empty_color
    else:
        color = values_colors[value]
        outline = outline_colors[value]
        light_color = light_colors[value]
        dark_color = dark_colors[value]
    
    tag = "(" + str(x) + "," + str(y) + ")"
    create_rectangle_or_edit(
        x * item_size + margin/2,
        y * item_size + margin/2,
        (x + 1) * item_size - margin/2,
        (y + 1) * item_size - margin/2,
        tag,
        fill=color,
        outline=outline,
        width=margin/2,
        tags=tag)   

    create_line_or_edit(
        x * item_size + margin, 
        y * item_size + margin, 
        (x + 1) * item_size - margin, 
        y * item_size + margin,
        tag + "1",
        width=margin,
        fill=light_color)
    create_line_or_edit(
        (x + 1) * item_size - margin, 
        y * item_size + margin, 
        (x + 1) * item_size - margin, 
        (y + 1) * item_size - margin, 
        tag + "2",
        width=margin,
        fill=light_color)
    create_line_or_edit(
        x * item_size + margin, 
        (y + 1) * item_size - margin, 
        (x + 1) * item_size - margin, 
        (y + 1) * item_size - margin,
        tag + "3",
        width=margin,
        fill=dark_color)
    create_line_or_edit(
        x * item_size + margin, 
        y * item_size + margin, 
        x * item_size + margin, 
        (y + 1) * item_size - margin, 
        tag + "4",
        width=margin,
        fill=dark_color)

    # if debug_number != -1:
    #     w.create_text(
    #         x * item_size + item_size/2,
    #         y * item_size + item_size/2 + margin,
    #         text=str(debug_number),
    #         fill="black",
    #         font=('Helvetica', int(item_size/3.5), 'bold'),
    #         justify="center")

# verifica se o jogo acabou
def verify_end_game():
    global current_figure, values
    points = get_figure_points(current_figure)
    for (x, y) in points:
        if y < 0 and y+1 >= 0 and values[y+1][x] != EMPTY_VALUE:
            print("GAME OVER")
            master.destroy()
            exit()

def consume_lines():
    global values, old_values
    indexes = []
    for y, x_values in enumerate(values):
        for value in x_values:
            if (value == EMPTY_VALUE):
                break
        else: # não caiu no break, toda a linha tem um bloco
            indexes.append(y)
    
    if len(indexes) > 0:
        old_values = deepcopy(values)
    for index in indexes:
        values.pop(index)
        values.insert(0, [EMPTY_VALUE for _ in range(columns)])

# faz as ações de um turno do jogo, chamado quando o usuário toca em uma seta
def game_step():
    consume_lines()
    verify_end_game()
    draw_game()

def valid_new_figure(figure):
    points = get_figure_points(figure)
    for (x, y) in points:
        if x < 0 or x > columns-1:
            return False
        if y > lines-1:
            return False
        if y >= 0 and x >= 0 and values[y][x] != EMPTY_VALUE:
            return False
    return True

# funções chamadas quando o usuário clica em alguma seta
def left_key(event):
    global current_figure, old_figure
    (figure_name, (x, y), figure_orientation) = current_figure
    new_figure = (figure_name, (x-1, y), figure_orientation)
    if valid_new_figure(new_figure):
        old_figure = current_figure
        current_figure = new_figure
        game_step()

def right_key(event):
    global current_figure, old_figure
    (figure_name, (x, y), figure_orientation) = current_figure
    new_figure = (figure_name, (x+1, y), figure_orientation)
    if valid_new_figure(new_figure):
        old_figure = current_figure
        current_figure = new_figure
        game_step()

def down_key(event):
    global job, current_figure, old_figure
    cancel()
    (figure_name, (x, y), figure_orientation) = current_figure
    new_figure = (figure_name, (x, y+1), figure_orientation)
    if valid_new_figure(new_figure):
        old_figure = current_figure
        current_figure = new_figure
    else:
        # figura atual bateu, vamos gerar outra e salvar essa
        save_current_figure()
        generate_new_figure()
    game_step()
    job = master.after(int(1000 / velocity), game_loop)

def up_key(event):
    global current_figure, old_figure
    (figure_name, (x, y), figure_orientation) = current_figure
    new_figure = (figure_name, (x, y), (figure_orientation + 1) % 4)
    if valid_new_figure(new_figure):
        old_figure = current_figure
        current_figure = new_figure
        game_step()

def cancel():
    global job, master
    if job is not None:
        master.after_cancel(job)
        job = None

def generate_new_figure():
    global figures, current_figure, old_figure
    new_figure_name = choice(list(figures.keys()))
    new_x = randint(3, columns-3)
    new_orientation = randint(0, 3)
    old_figure = None
    current_figure = (new_figure_name, (new_x, -1), new_orientation)

def save_current_figure():
    global figures, current_figure, values, old_values
    figure_value = figures[current_figure[0]][0]
    points = get_figure_points(current_figure)
    old_values = deepcopy(values)
    for (x, y) in points:
        if y >= 0 and x >= 0 and x < columns and y < lines:
            values[y][x] = figure_value

# Função principal do jogo, fica rodando sempre
# e chamando as outras funções para controlar as ações
def game_loop():
    global job, current_figure, old_figure
    (figure_name, (x, y), figure_orientation) = current_figure
    new_figure = (figure_name, (x, y+1), figure_orientation)
    if valid_new_figure(new_figure):
        old_figure = current_figure
        current_figure = new_figure
    else:
        # figura atual bateu, vamos gerar outra e salvar essa
        save_current_figure()
        generate_new_figure()

    game_step()
    job = master.after(int(1000 / velocity), game_loop)

# Cria a janela canvas do jogo
master = Tk()
master.title("Tetris")
master["bg"] = background_color

w = Canvas(master,
           width=width,
           height=heigh,
           background=background_color, 
           borderwidth=0, 
           highlightthickness=0)

w.pack(padx=margin, pady=margin, fill="both")

master.bind("<Left>", left_key)
master.bind("<Right>", right_key)
master.bind("<Up>", up_key)
master.bind("<Down>", down_key)

draw_game(force=True)
master.after(int(1000 / velocity), game_loop)

master.mainloop()