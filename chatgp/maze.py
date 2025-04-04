import pygame
import time

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
GRAY=(200,200,200)
YELLOW=(255, 255, 0)
RED=(254,0,0)


# Matriz del laberinto
maze = [
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 2, 0, 3, 4, 4, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [3, 3, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

solution=[(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 9), (4, 9), (4, 8), (4, 7), (4, 6), (4, 5), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (8, 9), (8, 8), (8, 7), (8, 6)]



# Dimensiones de la pantalla
tile_size = 50
width = len(maze[0]) * tile_size
height = len(maze) * tile_size + 100


# Inicializar pygame
pygame.init()
mediumFont = pygame.font.Font("fonts/OpenSans-Regular.ttf", 28)
# largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
# moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
# pygame.font.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Laberinto con Pygame")

def find_start():
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 2:
                return row, col
    return None

def draw_maze(partial_solution):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                color = GRAY  
            elif maze[row][col] == 2:
                color = BLUE  
            elif maze[row][col] == 3:
                color = ORANGE  
            elif maze[row][col] == 4:
                color = GREEN  
            else:
                color=WHITE
                
            if (row,col) in partial_solution:
                color=YELLOW
            
            
            pygame.draw.rect(screen, color, (col * tile_size, row * tile_size, tile_size, tile_size))
            pygame.draw.rect(screen, BLACK, (col * tile_size, row * tile_size, tile_size, tile_size), 1)
            
    
           

# Bucle principal
running = True
flag=False
count=0
partial_solution=[]

clock=pygame.time.Clock()

while running:
    screen.fill(WHITE)
 
    draw_maze(partial_solution)
    start_button=pygame.Rect((width//4-75, height-80,150,50))
    # pygame.draw.rect(screen,BLACK,(width*3//4-75, height-80,150,50))
    start_text=mediumFont.render('Start',True,WHITE)
    start_rect=start_text.get_rect()
    start_rect.center=start_button.center
    pygame.draw.rect(screen,BLACK,start_button)
    screen.blit(start_text,start_rect)
    
    
    exit_button=pygame.Rect((3 * width // 4 - 75, height - 80, 150, 50))
    exit_text=mediumFont.render('Exit',True,WHITE)
    exit_rect=exit_text.get_rect()
    exit_rect.center=exit_button.center
    pygame.draw.rect(screen,RED,exit_button)
    screen.blit(exit_text,exit_rect)
    
    # click, _,_=pygame.mouse.get_pressed()
    # if click==1:
    #     mouse= pygame.mouse.get_pos()
    #     if start_button.collidepoint(mouse):
        
    #         flag=True
    #     elif exit_button.collidepoint(mouse):
    #         running=False
    
    for event in  pygame.event.get():
        if  event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse=pygame.mouse.get_pos()
            if start_button.collidepoint(mouse):
                flag=True
                count=0
                partial_solution=[]
            
            elif exit_button.collidepoint(mouse):
                running=False
                
        

    
            
    if flag and count<len(solution):
        count+=1 
        partial_solution=solution[:count]  
        pygame.time.delay(200)
             
            
           
    pygame.display.flip()
    clock.tick(30)
    
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    
    
    
pygame.quit()