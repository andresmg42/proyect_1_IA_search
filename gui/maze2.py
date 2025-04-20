import pygame
import time


# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
RED = (254, 0, 0)
home_url='/home/andresuv/Ingenieria_De_Sistemas/Sesto_Semestre/IA/proyectos/PROYECTO-1/proyecto-1/'

class GUI():
    
    

    def __init__(self, maze, solution):

        self.solution = solution
        self.maze = maze
        self.init_pygame()
        
    def load_image(self,path):
        try:
            image=pygame.image.load(path)
            image= pygame.transform.scale(image,(self.tile_size,self.tile_size))
            return image
        except:
            print('Could not load image')
            return None
        

    def init_pygame(self):
        self.tile_size = 50
        self.width = len(self.maze[0]) * self.tile_size
        self.height = len(self.maze) * self.tile_size + 100
        pygame.init()
        font=home_url+"gui/fonts/OpenSans-Regular.ttf"
        self.mediumFont = pygame.font.Font(font, 28)
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Laberinto con Pygame")
        
    def find_start(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == 2:
                    return row, col
        return None
    
    def draw_maze(self,partial_solution):
        electromagnetic_field=self.load_image(home_url+'gui/images/electromagnetic_field.jpg')
        
        box=self.load_image(home_url+'gui/images/box.jpg')
        dron=self.load_image(home_url+'gui/images/dron.jpg')
        
        
        
        
        
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == 1:
                    color = GRAY  
                elif self.maze[row][col] == 2:
                    color = BLUE  
                elif self.maze[row][col] == 3:
                    color=ORANGE           
                elif self.maze[row][col] == 4:
                    color = GREEN  
                else:
                    color=WHITE
                    
                if (row,col) in partial_solution:
                    color=YELLOW
                
                
                pygame.draw.rect(self.screen, color, (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                
                if self.maze[row][col]==3 and electromagnetic_field is not None and (row,col) not in partial_solution:
                    self.screen.blit(electromagnetic_field,(col*self.tile_size,row*self.tile_size))
                
                if self.maze[row][col]==4 and box is not None and (row,col) not in partial_solution:
                    self.screen.blit(box,(col*self.tile_size,row*self.tile_size))
                    
                if self.maze[row][col]==2 and box is not None or (row,col)  in partial_solution:
                    self.screen.blit(dron,(col*self.tile_size,row*self.tile_size))
                
                pygame.draw.rect(self.screen, BLACK, (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size), 1)
    
    def main_lopp(self):
        running = True
        flag=False
        count=0
        partial_solution=[]

        clock=pygame.time.Clock()

        while running:
            self.screen.fill(WHITE)
        
            self.draw_maze(partial_solution)
            start_button=pygame.Rect((self.width//4-75, self.height-80,150,50))
            start_text=self.mediumFont.render('Start',True,WHITE)
            start_rect=start_text.get_rect()
            start_rect.center=start_button.center
            pygame.draw.rect(self.screen,BLACK,start_button)
            self.screen.blit(start_text,start_rect)
            
            
            exit_button=pygame.Rect((3 * self.width // 4 - 75, self.height - 80, 150, 50))
            exit_text=self.mediumFont.render('Exit',True,WHITE)
            exit_rect=exit_text.get_rect()
            exit_rect.center=exit_button.center
            pygame.draw.rect(self.screen,RED,exit_button)
            self.screen.blit(exit_text,exit_rect)
            
            
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
                        
                

            
                    
            if flag and count<len(self.solution):
                count+=1 
                partial_solution=self.solution[:count]  
                pygame.time.delay(200)
                    
                    
                
            pygame.display.flip()
            clock.tick(30)
            

        pygame.quit()
               
        
    
    
