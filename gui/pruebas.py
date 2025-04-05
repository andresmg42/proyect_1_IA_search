import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from view.start_window_gui import StartWindow


start=StartWindow()
start.main_loop()

