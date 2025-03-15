
import sys
import math


class Node():
    def __init__(self, state, parent, action, g_cost, position, f_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g_cost = g_cost  # Costo acumulado hasta este nodo
        self.position = position
        self.f_cost = f_cost  # Costo total f(n) = g(n) + h(n)
        
class QueueFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
        
    def contains_state(self, state, position):
        return any(node.state == state and node.position == position for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception('empty frontier')
        else:
            nodomin = None
            min_cost = math.inf
            
            for node in self.frontier:
                if node.f_cost < min_cost:
                    min_cost = node.f_cost
                    nodomin = node
                    
            self.frontier.remove(nodomin)
            return nodomin
    
    # Función para actualizar un nodo existente si encontramos un camino mejor
    def update_node(self, state, position, new_node):
        for i, node in enumerate(self.frontier):
            if node.state == state and node.position == position:
                if new_node.f_cost < node.f_cost:
                    self.frontier[i] = new_node
                return True
        return False
            
class Maze():
    
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
            
        if contents.count('2') != 1:
            raise Exception('maze must have exactly one start point')
        if contents.count('4') == 0:
            raise Exception('maze must have at least one goal')
        
        self.contents = [line.split() for line in contents.splitlines()]
        self.height = len(self.contents)
        self.width = len(self.contents[0])
        self.boxes = set()
        
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j] == '2':
                    self.start = (i, j)
                elif self.contents[i][j] == '4':
                    self.boxes.add((i, j))
        
        self.solution = None
    
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.contents):
            for j, col in enumerate(row):
                if col == '1':
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif self.contents[i][j] == '4':
                    print('B', end="")
                elif self.contents[i][j] == '3':
                    print('E', end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
    
    def neighbors(self, position):
        row, col = position
        
        candidates = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1))
        ]
        
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.contents[r][c] == '1':
                result.append((action, (r, c)))
        return result
    
    # Heurística de distancia de Manhattan
    def manhattan_distance(self, position, goal):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
    
    # Calculamos la heurística como la suma de distancias a las cajas no alcanzadas
    def calculate_heuristic(self, position, state):
        remaining_boxes = self.boxes - state
        if not remaining_boxes:  # Si todas las cajas han sido alcanzadas
            return 0
        
        # Retornamos la distancia mínima a la caja más cercana
        return min(self.manhattan_distance(position, box) for box in remaining_boxes)
        
    def solve(self):
        self.num_explored = 0
        
        # Creamos el nodo inicial
        start = Node(state=set(), parent=None, action=None, g_cost=0, position=self.start)
        # Calculamos el f_cost inicial (g_cost + heurística)
        start.f_cost = start.g_cost + self.calculate_heuristic(start.position, start.state)
        
        frontier = QueueFrontier()
        frontier.add(start)
        
        self.explored = set()
        
        while True:
            if frontier.empty():
                raise Exception('no solution')
            
            node = frontier.remove()
            self.num_explored += 1
            
            # Si hemos alcanzado todas las cajas, encontramos la solución
            if node.state == self.boxes:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.position)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # Marcamos el nodo como explorado
            self.explored.add((node.position, tuple(sorted(node.state))))
            
            # Exploramos los vecinos
            for action, position in self.neighbors(node.position):
                i, j = position
                
                newstate = node.state.copy()
                if self.contents[i][j] == '4':
                    # newstate = node.state.copy()
                    newstate.add((i, j))
                
                if (position, tuple(sorted(newstate))) not in self.explored:
                    # Calculamos el nuevo g_cost
                    new_g_cost = node.g_cost + (8 if self.contents[i][j] == '3' else 1)
                    
                    # Calculamos la heurística
                    h_cost = self.calculate_heuristic(position, newstate)
                    
                    # Calculamos el f_cost total
                    new_f_cost = new_g_cost + h_cost
                    
                    # Creamos el nuevo nodo
                    child = Node(
                        state=newstate,
                        parent=node,
                        action=action,
                        g_cost=new_g_cost,
                        position=position,
                        f_cost=new_f_cost
                    )
                    
                    # Si el nodo ya está en la frontera pero con un costo mayor, lo actualizamos
                    if frontier.contains_state(newstate, position):
                        frontier.update_node(newstate, position, child)
                    else:
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