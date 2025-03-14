import sys
import math

class Node():
    def __init__(self,state,parent,action,position):
        self.state=state
        self.parent=parent
        self.action= action
        self.position=position
        self.m_d=sys.maxsize
       
        
        
    def manhatan_dist(self,boxes):
        min=sys.maxsize
        sum=0
        for box in boxes:
            if box not in self.state:
                sum=(abs(box[0]-self.position[0])+abs(box[1]-self.position[1]))
                if sum<min:
                    min=sum
        self.m_d=sum
        
        
        
class QueueFrontier():
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
       
            nodomin=None
            min=math.inf
            
            for node in self.frontier:
                if node.m_d < min:
                    min=node.m_d
                    nodomin=node
                    
            self.frontier.remove(nodomin)
            return nodomin
            
            
           
                
                
            
            
        

class Maze():
    
    def __init__(self,filename):
        with open(filename) as f:
            contents=f.read()
            
        if contents.count('2')!=1:
            raise Exception('maze must have exactly one start point')
        if contents.count('4')==0:
            raise Exception('maze must have exactly one goal')
        
        
        self.contents= [line.split() for line in contents.splitlines()]
        
      
        self.height=len(self.contents)
      
        
        self.width=len(self.contents[0])
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
        
    def solve(self):
        
        self.num_explored=0
        
        start=Node(state=set(),parent=None,action=None,position=self.start)
        frontier=QueueFrontier()
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
            
            # self.explored.add(node)
            self.explored.add((node.position,tuple(sorted(node.state))))
            
            
            for action,position in self.neighbors(node.position):
                i,j=position
                
                newstate=node.state
                if self.contents[i][j]=='4':
                    newstate = node.state.copy()
                    newstate.add((i,j))
                    
                    
               
                
                child=Node(state=newstate,parent=node,action=action,position=position)
                
                child.manhatan_dist(self.boxes)
                
                if not frontier.contains_state(newstate,position) and (child.position,tuple(sorted(child.state)))  not in self.explored:
                    
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


if len(sys.argv) != 2:
    sys.exit("Usage: python proyecto_1.py Prueba1.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
print(m.solution) 