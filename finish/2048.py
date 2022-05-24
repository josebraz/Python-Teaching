import math
from tkinter import *
from random import randint
from copy import deepcopy

items = 4
item_size = 100
size = item_size * items
margin = item_size/20

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

values = [[EMPTY_VALUE for _ in range(items)] for _ in range(items)]
old_values = [[0 for _ in range(items)] for _ in range(items)]

# desenha todos os quadados do jogo
def draw_game():
    for y, x_values in enumerate(values):
        for x, value in enumerate(x_values):
            draw_square(x, y, value)

# desenha um quadrado
def draw_square(x, y, value = EMPTY_VALUE):
    global w, old_values
    if (old_values[y][x] == value): 
        # otimização: não precisa redesenhar porque o valor não mudou
        return
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
            font=('Helvetica', int(item_size/3.5), 'bold'),
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
    while True:
        new_x = randint(0, items-1)
        new_y = randint(0, items-1)
        if values[new_y][new_x] == EMPTY_VALUE:
            values[new_y][new_x] = 2
            break          

# verifica se o jogo acabou, ou seja, 
# não tem mais ações possíveis que o jogador pode fazer
def verify_end_game():
    # otimização: se tem um espaço disponível, tem jogada possível
    if has_space_for_new_value():
        return
    # testa o jogo ainda tem alguma ação possível, se não tem acabou o jogo
    copy = deepcopy(values)
    left_action(copy)
    if (copy != values):
        return
    right_action(copy)
    if (copy != values):
        return
    down_action(copy)
    if (copy != values):
        return
    up_action(copy)
    if (copy != values):
        return
    print("GAME OVER")
    master.destroy()

# faz as ações de um turno do jogo, chamado quando o usuário toca em uma seta
def game_step():
    global values
    generate_new_value()
    draw_game()
    verify_end_game()

def filter_empty_value(list):
    filtered = []
    for value in list:
        if value != EMPTY_VALUE:
            filtered.append(value)
    return filtered

def get_column(matrix, i):
    return [row[i] for row in matrix]

def set_column(matrix, i, value):
    index = 0
    for row in matrix:
        row[i] = value[index]
        index += 1

def combine(list):
    filtered = filter_empty_value(list)
    new_list = []
    combined_index = -1
    for index, value in enumerate(filtered):
        if combined_index != index:
            if index < len(filtered)-1 and filtered[index+1] == value:
                new_list.append(value * 2)
                combined_index = index+1
            else:
                new_list.append(value)
    return new_list + [EMPTY_VALUE] * (items - len(new_list))

def left_action(values):
    for y in range(items):
        new_list = combine(values[y])
        values[y] = new_list

def right_action(values):
    for y in range(items):
        new_list = list(reversed(combine(reversed(values[y]))))
        values[y] = new_list

def down_action(values):
    for x in range(items):
        new_list = list(reversed(combine(reversed(get_column(values, x)))))
        set_column(values, x, new_list)

def up_action(values):
    for x in range(items):
        new_list = combine(get_column(values, x))
        set_column(values, x, new_list)

# funções chamadas quando o usuário clica em alguma seta
def left_key(event):
    global values, old_values
    old_values = deepcopy(values)
    left_action(values)
    game_step()

def right_key(event):
    global values, old_values
    old_values = deepcopy(values)
    right_action(values)
    game_step()

def down_key(event):
    global values, old_values
    old_values = deepcopy(values)
    down_action(values)
    game_step()

def up_key(event):
    global values, old_values
    old_values = deepcopy(values)
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