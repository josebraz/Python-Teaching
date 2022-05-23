from tkinter import *
from random import randint

##########################################
# Configurações do jogo
canvas_width = 600
canvas_height = 400
pixel_size = 20
velocity = 5  # ticks por segundo
snake_color = "red"
food_color = "green"

max_x = int(canvas_width / pixel_size)
max_y = int(canvas_height / pixel_size)

# constantes das direções que a cobra pode ter 
LEFT  = 0
RIGHT = 1
UP    = 2
DOWN  = 3

##########################################

# Variáveis do jogo
food_coord = (-1, -1)
snake_body = [(max_x / 2, max_y / 2), (max_x / 2 - 1, max_y / 2), (max_x / 2 - 2, max_y / 2)]
snake_direction = RIGHT

def draw_pixel(x, y, color="yellow"):
    w.create_rectangle(
        x * pixel_size,
        y * pixel_size,
        (x + 1) * pixel_size,
        (y + 1) * pixel_size,
        fill=color)

# Gera uma nova comida em uma coordenada aleatória
def generate_food():
    pass

# desenha a comida (usar a função draw_pixel)
def draw_food():
    pass

# desenha a cobra (usar a função draw_pixel)
def draw_snake():
    pass

# verifica se a cobrinha está com a cabela em
# cima de uma comida
def snake_eat():
    pass

# movimenta a cobra de acordo com a direção atual
def snake_tick():
    pass

# verifica se a cobra morreu (bateu na parede ou se comeu)
def snake_die():
    pass

# verifica se a coordenada passada é a mesma de
# alguma parte do corpo da cobrinha
def coord_in_body(coord):
    pass

# funções chamadas quando o usuário clica em alguma seta
def left_key(event):
    pass

def right_key(event):
    pass

def down_key(event):
    pass

def up_key(event):
    pass

# Função principal do jogo, fica rodando sempre
# e chamando as outras funções para controlar as ações
def game_loop():
    global user_click
    user_click = False
    w.delete("all") ## limpa todos os elementos do desenhados anteriormente
    snake_tick()
    draw_food()
    draw_snake()
    snake_eat()
    if snake_die():
        print("END GAME")
        master.destroy()
    else:
        master.after(int(1000 / velocity), game_loop)

# ---------------------------------------

# Cria a janela canvas do jogo
master = Tk()
master.title("Snake Game")

w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()

master.bind("<Left>", left_key)
master.bind("<Right>", right_key)
master.bind("<Up>", up_key)
master.bind("<Down>", down_key)

generate_food()
master.after(int(1000 / velocity), game_loop)
master.mainloop()