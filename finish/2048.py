import math
from tkinter import *
from random import randint
from copy import deepcopy

size = 400
margin = 6
items = 4
item_size = size / items

EMPTY_VALUE = -1
LEFT  = 0
RIGHT = 1
UP    = 2
DOWN  = 3

background_color = "#b9ac9c"
empty_color = "#cdc1b5"
text_color_low = "#70675e"
text_color_high = "#fff5e9"
values_colors = ["#eee4db", "#ece0c8", "#f3b177", "#f49662", "#f57c5f", "#f65f3c", "#ebcf72", "#edcc63", "#ebc850", "#ecc53e", "#efc32e"]

values = [
    [EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE],
    [EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE],
    [EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE],
    [EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE]
]

# desenha todos os quadados do jogo
def draw_game():
    for y, x_values in enumerate(values):
        for x, value in enumerate(x_values):
            draw_square(x, y, value)

# desenha um quadrado
def draw_square(x, y, value = EMPTY_VALUE):
    global w
    if value == -1:
        color = empty_color
    else:
        color = values_colors[int(math.log(value, 2)) - 1]

    w.create_rectangle(
        x * item_size + margin,
        y * item_size + margin,
        (x + 1) * item_size - margin,
        (y + 1) * item_size - margin,
        fill=color,
        outline="")
    if value != EMPTY_VALUE:
        if (value >= 8):
            text_color = text_color_high
        else:
            text_color = text_color_low
        w.create_text(
            x * item_size + item_size/2,
            y * item_size + item_size/2 + margin,
            text=str(value),
            fill=text_color,
            font=('Helvetica','30','bold'),
            justify="center")

# verifica se tem espaço em branco no grid do jogo
def has_space_for_new_value():
    for row in values:
        if EMPTY_VALUE in row:
            return True
    return False

# gera um novo valor no jogo se tiver espaço para isso
def generate_new_value():
    if not has_space_for_new_value():
        # não tem lugar disponível para gerar um novo valor
        return
    new_x = randint(0, items-1)
    new_y = randint(0, items-1)
    if values[new_y][new_x] != EMPTY_VALUE:
        generate_new_value()
    else:
        values[new_y][new_x] = 2

# verifica se o jogo acabou, ou seja, 
# não tem mais ações possíveis que o jogador pode fazer
def verify_end_game():
    # testa o jogo ainda tem alguma ação possível, se não tem acabou o jogo
    copy = deepcopy(values)
    if not (left_action(copy) or right_action(copy) or down_action(copy) or up_action(copy)):
        print("GAME OVER")
        master.destroy()

# faz as ações de um turno do jogo, chamado quando o usuário toca em uma seta
def game_step():
    global values
    generate_new_value()
    draw_game()
    verify_end_game()

def left_action(values):
    any_change = False
    for y in range(items):
        combine = -1
        for x in range(items-1, 0, -1):
            if values[y][x] != EMPTY_VALUE:
                if values[y][x] == values[y][x-1] and combine != x:
                    combine = x-1
                    values[y][x-1] *= 2
                    values[y][x] = EMPTY_VALUE
                    any_change = True
                elif values[y][x-1] == EMPTY_VALUE:
                    values[y][x-1] = values[y][x]
                    values[y][x] = EMPTY_VALUE
                    any_change = True
            if x < items-1 and values[y][x] == EMPTY_VALUE and values[y][x+1] != EMPTY_VALUE:
                values[y][x] = values[y][x+1]
                values[y][x+1] = EMPTY_VALUE
                any_change = True
    return any_change

def right_action(values):
    any_change = False
    for y in range(items):
        combine = -1
        for x in range(items):
            if x < items-1 and values[y][x] != EMPTY_VALUE:
                if values[y][x] == values[y][x+1] and combine != x:
                    combine = x+1
                    values[y][x+1] *= 2
                    values[y][x] = EMPTY_VALUE
                    any_change = True
                elif values[y][x+1] == EMPTY_VALUE:
                    values[y][x+1] = values[y][x]
                    values[y][x] = EMPTY_VALUE
                    any_change = True
            if x > 0 and x < items-1 and values[y][x] == EMPTY_VALUE and values[y][x-1] != EMPTY_VALUE:
                values[y][x] = values[y][x-1]
                values[y][x-1] = EMPTY_VALUE
                any_change = True
    return any_change

def down_action(values):
    any_change = False
    for x in range(items):
        combine = -1
        for y in range(items):
            if y < items-1 and values[y][x] != EMPTY_VALUE:
                if values[y][x] == values[y+1][x] and combine != y:
                    combine = y+1
                    values[y+1][x] *= 2
                    values[y][x] = EMPTY_VALUE
                    any_change = True
                elif values[y+1][x] == EMPTY_VALUE:
                    values[y+1][x] = values[y][x]
                    values[y][x] = EMPTY_VALUE
                    any_change = True
            if y > 0 and y < items-1 and values[y][x] == EMPTY_VALUE and values[y-1][x] != EMPTY_VALUE:
                values[y][x] = values[y-1][x]
                values[y-1][x] = EMPTY_VALUE
                any_change = True
    return any_change

def up_action(values):
    any_change = False
    for x in range(items):
        combine = -1
        for y in range(items-1, 0, -1):
            if values[y][x] != EMPTY_VALUE:
                if values[y][x] == values[y-1][x] and combine != y:
                    combine = y-1
                    values[y-1][x] *= 2
                    values[y][x] = EMPTY_VALUE
                    any_change = True
                elif values[y-1][x] == EMPTY_VALUE:
                    values[y-1][x] = values[y][x]
                    values[y][x] = EMPTY_VALUE
                    any_change = True
            if y < items-1 and values[y][x] == EMPTY_VALUE and values[y+1][x] != EMPTY_VALUE:
                values[y][x] = values[y+1][x]
                values[y+1][x] = EMPTY_VALUE
                any_change = True
    return any_change

# funções chamadas quando o usuário clica em alguma seta
def left_key(event):
    global values
    left_action(values)
    game_step()

def right_key(event):
    global values
    right_action(values)
    game_step()

def down_key(event):
    global values
    down_action(values)
    game_step()

def up_key(event):
    global values
    up_action(values)
    game_step()

# Cria a janela canvas do jogo
master = Tk()
master.title("2048")
master["bg"] = background_color

w = Canvas(master,
           width=size,
           height=size,
           background=background_color, 
           borderwidth=0, 
           highlightthickness=0)

w.pack(padx=margin, pady=margin, fill="both")

master.bind("<Left>", left_key)
master.bind("<Right>", right_key)
master.bind("<Up>", up_key)
master.bind("<Down>", down_key)

game_step()

master.mainloop()