import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gui.maze2 import GUI
from gui.pruebas import maze,solution
from algorithms.proyecto_1_GFS import Maze

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

def open_file():
    file_path = filedialog.askopenfilename()
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
    m=Maze('plane_files/Prueba1.txt')
    m.solve()
    solution=m.solution[1]
    print(solution)
    gui=GUI(maze,solution)
    gui.main_lopp()
    
    
    
    

root = tk.Tk()
root.title("Simple Text Editor")

# Menu bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

container=tk.Frame(root,width=600,height=300)
container.pack_propagate(False)
container.pack(expand=True,pady=50,padx=50)

start_button=tk.Button(container,text='Start',command=on_start_click)
start_button.pack(pady=10)


# Text widget with scrollbar
text = tk.Text(container, width=50,height=15, font=('Arial',12))
scrollbar = tk.Scrollbar(container, command=text.yview)
text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.pack()

root.mainloop()