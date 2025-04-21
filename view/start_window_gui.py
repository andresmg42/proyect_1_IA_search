import tkinter as tk
from tkinter import filedialog, messagebox,ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gui.gui_pygame import GUI
from algorithms.proyecto_1_GFS import Maze as m_gfs
from algorithms.proyecto_1_DFS import Maze as m_dfs
from algorithms.proyecto_1_costo import Maze as m_costo
from algorithms.proyecto_1_BFS import Maze as m_bfs
from algorithms.proyecto_1_Astar import Maze as m_astar
from time import time


class StartWindow():
    
    def __init__(self):
        self.contents=None
        
        
    def open_file(self):
        url='plane_files'
        file_path = filedialog.askopenfilename(initialdir=url)
        
        if file_path:
            with open(file_path, 'r') as file:
                self.contents=file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, self.contents)
        
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                # text_to_save=self.text.get(1.0, tk.END)
                text_to_save = self.text.get(1.0, tk.END).rstrip('\n')
                print('tex to save:',text_to_save)
                file.write(text_to_save)
                self.contents=text_to_save
            messagebox.showinfo("Info", "File saved successfully")
            
    def get_selected_algorithm(self):
        option=self.selected_option.get()
        if option=='GFS':
            return (m_gfs,option)
        elif option=='DFS':
            return (m_dfs,option)
        elif option=='COST':
            return (m_costo,option)
        elif option=='A*':
            return (m_astar,option)
        else:
            return (m_bfs,option)
        
    def report(self,execution_time,deep_tree,total_explored_nodes,selected_algorithm):
        string=f"""
        Report: 
        
        Algorithm: {selected_algorithm}
        
        Total Explored Nodes: {total_explored_nodes}
        
        Deep Tree: {deep_tree}
        
        Execution Time: {execution_time} sec
        
        """
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, string)
        
            
            
    def on_start_click(self):
        if self.contents is not None:
            algorithm=self.get_selected_algorithm()
            m=algorithm[0](self.contents)
            start=time()
            m.solve()
            end=time()
            execution_time=end-start
            solution=m.solution[1]
            deep_tree=len(solution)
            total_explored_nodes=m.num_explored
            maze=[[int(cell) for cell in line.split()] for line in self.contents.splitlines()]
            gui=GUI(maze,solution)
            m.output_image("maze.png", show_explored=True)
            m.print()
            self.report(execution_time,deep_tree,total_explored_nodes,algorithm[1])
            gui.main_lopp()
            
            
            
        else:
            messagebox.showerror('choose a valid file!')
            
            
    def last_solution_image(self):
        root=tk.Toplevel()
        root.title("LAST SOLUTION")
        root.geometry('500x500')
        
        #load image
        root.img=tk.PhotoImage(file='maze.png')
        
        #Create label whit image
        label=tk.Label(root,image=root.img)
        label.pack(fill=tk.BOTH)
        
        
        
              
    
    def main_loop(self):
        root = tk.Tk()
        root.title("SEARCH IA")
        root.geometry('1000x800')

        # Menu bar
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        #main container
        container=ttk.Frame(root,padding=10)
        container.pack_propagate(False)
        container.pack(fill= tk.BOTH, expand=True)


        #create left and right sections inside the main frame
        left_container=ttk.Frame(container)
        left_container.pack(side=tk.LEFT,fill=tk.BOTH, expand=True, padx=(0,5))

        right_container=ttk.Frame(container)
        right_container.pack(side=tk.RIGHT, fill=tk.Y)




        # Text widget with scrollbar
        self.text = tk.Text(left_container,width=40, height=15, font=('Arial',12),wrap=tk.WORD)
        scrollbar = tk.Scrollbar(left_container, command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand=True)



        #add radio button
        radio_label=ttk.Label(right_container, text="Choose an Uninformed Algorithm:")
        radio_label.pack(anchor=tk.NW,pady=(0,5))

        #variable to store selected option
        self.selected_option=tk.StringVar(value='BFS')

        #List of radio button options
        options=['BFS','DFS','COST','GFS','A*']

        #Create radio buttons uninformed algorithms
        for option in options[:3]:
            rb=ttk.Radiobutton(
                right_container,
                text=option,
                value=option,
                variable=self.selected_option
            )
            rb.pack(anchor=tk.NW)

        #add radio button
        radio_label=ttk.Label(right_container, text="Choose an Informed Algorithm:")
        radio_label.pack(anchor=tk.NW,pady=(0,5))


        #Create radio buttons informed algorithms
        for option in options[3:]:
            rb=ttk.Radiobutton(
                right_container,
                text=option,
                value=option,
                variable=self.selected_option
            )
            rb.pack(anchor=tk.NW)



        #add start button
        start_button=tk.Button(right_container,text='Start',command=self.on_start_click)
        start_button.pack(pady=10)
        
        #add start button
        image_button=tk.Button(right_container,text='Last Solution',command=self.last_solution_image)
        image_button.pack(pady=10)
        
       

        root.mainloop()
        
        
    
    