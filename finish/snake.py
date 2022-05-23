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
user_click = False

def draw_pixel(x, y, color="yellow"):
    w.create_rectangle(
        x * pixel_size,
        y * pixel_size,
        (x + 1) * pixel_size,
        (y + 1) * pixel_size,
        fill=color)

# Gera uma nova comida em uma coordenada aleatória
def generate_food():
    global food_coord
    food_coord = (randint(0, max_x - 1), randint(0, max_y - 1))
    if coord_in_body(food_coord):
        generate_food()

# desenha a comida
def draw_food():
    draw_pixel(food_coord[0], food_coord[1], food_color)

# desenha a cobra 
def draw_snake():
    for (x, y) in snake_body:
        draw_pixel(x, y, snake_color)

# verifica se a cobrinha está com a cabela em
# cima de uma comida
def snake_eat():
    global snake_body
    if food_coord == snake_body[0]:
        snake_body.append(snake_body[-1])
        generate_food()

# movimenta a cobra de acordo com a direção atual
def snake_tick():
    global snake_direction, snake_body
    (snake_head_x, snake_head_y) = snake_body[0]
    if snake_direction == LEFT:
        snake_head_x -= 1
    elif snake_direction == RIGHT:
        snake_head_x += 1
    elif snake_direction == UP:
        snake_head_y -= 1
    elif snake_direction == DOWN:
        snake_head_y += 1
    # movimenta a cabeça na direção que a cobra está indo
    # e junta a nova posição com o resto do copo (tirando o rabo)
    snake_body = [(snake_head_x, snake_head_y)] + snake_body[:-1]

# verifica se a cobra morreu (bateu na parede ou se comeu)
def snake_die():
    global snake_body
    (head_x, head_y) = snake_body[0]
    # verifica se saiu do mapa (bateu na parede)
    if head_x < 0 or head_x > max_x - 1:
        return True
    if head_y < 0 or head_y > max_y - 1:
        return True
    # verifica se a cobra se comeu
    return snake_body[0] in snake_body[1:]

# verifica se a coordenada passada é a mesma de
# alguma parte do corpo da cobrinha
def coord_in_body(coord):
    global snake_body
    return coord in snake_body

# funções chamadas quando o usuário clica em alguma seta
def left_key(event):
    change_direction(LEFT)

def right_key(event):
    change_direction(RIGHT)

def down_key(event):
    change_direction(DOWN)

def up_key(event):
    change_direction(UP)

# muda a direção da cobra se o usuário ainda não 
# mudou nesse tick e se não for a direção oposta da atual
def change_direction(new_direction):
    global snake_direction, user_click
    if user_click or new_direction == snake_direction: 
        return
    if (snake_direction == LEFT or snake_direction == RIGHT) and (new_direction == LEFT or new_direction == RIGHT):
        return
    if (snake_direction == UP or snake_direction == DOWN) and (new_direction == UP or new_direction == DOWN):
        return
    snake_direction = new_direction
    user_click = True

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