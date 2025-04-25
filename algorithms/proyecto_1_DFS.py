import sys
import math
import copy

class Node():
    def __init__(self,state,parent,action,position):
        self.state=state
        self.parent=parent
        self.action= action
        self.position=position
        
class StackFrontier():
    def __init__(self):
        self.frontier=[]
    
    def add(self,node):
        self.frontier.append(node)
        
    def contains_state(self,state,position):
        return any(node.state==state and node.position==position for node in self.frontier)
    
    def empty(self):
        return len(self.frontier)==0
    
    def remove(self):
        
        if self.empty():
            raise Exception('empty frontier')
        else:
       
            node=self.frontier[-1]
            self.frontier=self.frontier[:-1]
            
            return node
           
                
                
class Maze():
    
    def __init__(self,contents):
        
            
        if contents.count('2')!=1:
            raise Exception('maze must have exactly one start point')
        if contents.count('4')==0:
            raise Exception('maze must have exactly one goal')
        
        
        self.contents= [line.split() for line in contents.splitlines()]
        
      
        self.height=len(self.contents)
        
        print(f'height: {self.height}')
      
        
        self.width=len(self.contents[0])
        
        print(f'widht: {self.width}')
        
        self.boxes=set()
        
        for i in range(self.height):
            
            for j in range(self.width):
                if self.contents[i][j]== '2':
                        self.start=(i,j)
                elif self.contents[i][j]=='4':
                    self.boxes.add((i,j))
        
        self.solution=None
    
    
    def print(self):
        solution=self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.contents):
            for j,col in enumerate(row):
                if col=='1':
                    print("█",end="")
                elif (i,j)== self.start:
                    print("A",end="")
                elif self.contents[i][j]=='4':
                    print('B',end="")
                elif self.contents[i][j]=='3':
                    print('E',end="")
                elif solution is not None and (i,j) in solution:
                    print("*",end="")
                else:
                    print(" ",end="")
            print()
        print()
        
    
    def neighbors(self,position):
        row,col=position
        
        
        candidates=[
            ("up",(row-1,col)),
            ("down",(row+1,col)),
            ("left",(row,col-1)),
            ("right",(row,col+1))
        ]
        
        result=[]
        for action, (r,c) in candidates:
            if 0<= r < self.height and 0 <= c < self.width and not self.contents[r][c]=='1':
                result.append((action,(r,c)))
        return result
    
    
    def verify_loops(self,node):
       
        first_node=copy.copy(node)
        while node.parent is not None:
            if first_node.state==node.state and first_node.position==node.position:
                return True
            node=node.parent
        return False
        
                
     
    def solve(self):
        
        self.num_explored=0
        
        start=Node(state=set(),parent=None,action=None,position=self.start)
        frontier=StackFrontier()
        frontier.add(start)
        
        self.explored=set()
        
        while True:
            
            if frontier.empty():
                raise Exception('no solution')
            
            node=frontier.remove()
            
                
                
            self.num_explored+=1
            
            if len(node.state) == len(self.boxes):
                actions=[]
                cells=[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.position)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution= (actions,cells)
                return
            
            self.explored.add((node.position,tuple(sorted(node.state))))
            
            
            for action,position in self.neighbors(node.position):
                i,j=position
                
                newstate=node.state
                if self.contents[i][j]=='4':
                    newstate = node.state.copy()
                    newstate.add((i,j))
                    
                    
            
                
                
                
                if not frontier.contains_state(newstate,position) and (position,tuple(sorted(newstate)))  not in self.explored:
                    
                    child=Node(state=newstate,parent=node,action=action,position=position)
                    
                    frontier.add(child)
                    
                    
                
    def output_image(self, filename, show_solution=True, show_explored=False):
            from PIL import Image, ImageDraw
            cell_size = 50
            cell_border = 2

            # Create a blank canvas
            img = Image.new(
                "RGBA",
                (self.width * cell_size, self.height * cell_size),
                "black"
            )
            draw = ImageDraw.Draw(img)

            solution = self.solution[1] if self.solution is not None else None
            for i, row in enumerate(self.contents):
                for j, col in enumerate(row):

                    # Walls
                    if col=='1':
                        fill = (40, 40, 40)

                    # Start
                    elif (i, j) == self.start:
                        fill = (255, 0, 0)

                    # Goal
                    elif (i, j)=='4':
                        fill = (0, 171, 28)

                    # Solution
                    elif solution is not None and show_solution and (i, j) in solution:
                        fill = (220, 235, 113)

                    # Explored
                    elif solution is not None and show_explored and (i, j) in self.explored:
                        fill = (212, 97, 85)

                    # Empty cell
                    else:
                        fill = (237, 240, 252)

                    # Draw cell
                    draw.rectangle(
                        ([(j * cell_size + cell_border, i * cell_size + cell_border),
                        ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                        fill=fill
                    )

            img.save(filename)


 