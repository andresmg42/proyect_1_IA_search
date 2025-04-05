import tkinter as tk
from tkinter import filedialog, messagebox,ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gui.maze2 import GUI
from algorithms.proyecto_1_GFS import Maze as m_gfs

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

maze_path=None

def open_file():
    file_path = filedialog.askopenfilename()
    maze_path=file_path
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))
        messagebox.showinfo("Info", "File saved successfully")
        
def on_start_click():
    m=m_gfs('plane_files/Prueba1.txt')
    m.solve()
    solution=m.solution[1]
    print(solution)
    gui=GUI(maze,solution)
    gui.main_lopp()
    
    
    
    

root = tk.Tk()
root.title("SEARCH IA")
root.geometry('700x400')

# Menu bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
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
text = tk.Text(left_container,width=40, height=15, font=('Arial',12),wrap=tk.WORD)
scrollbar = tk.Scrollbar(left_container, command=text.yview)
text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.pack(fill=tk.BOTH, expand=True)



#add radio button
radio_label=ttk.Label(right_container, text="Choose an Uninformed Algorithm:")
radio_label.pack(anchor=tk.NW,pady=(0,5))

#variable to store selected option
selected_option=tk.StringVar(value='BFS')

#List of radio button options
options=['BFS','DFS','COST','GFS','A*']

#Create radio buttons uninformed algorithms
for option in options[:3]:
    rb=ttk.Radiobutton(
        right_container,
        text=option,
        value=option,
        variable=selected_option
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
        variable=selected_option
    )
    rb.pack(anchor=tk.NW)



#add start button
start_button=tk.Button(right_container,text='Start',command=on_start_click)
start_button.pack(pady=10)

root.mainloop()