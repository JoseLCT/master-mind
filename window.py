import tkinter as tk
from tkinter import filedialog

from home_panel import HomePanel
from selecter_panel import SelecterPanel
from results_panel import ResultsPanel

class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x300")
        self.center_window(self.window)
        self.file = None
        self.open_home_panel()
        self.window.mainloop()
        
    def open_home_panel(self):
        self.home_panel = HomePanel(self.window, self)

    def open_selecter_panel(self):
        self.home_panel.panel.destroy()
        self.model_selecter_panel = SelecterPanel(self.window, self)

    #def open_results_panel(self, model, x_columns, y_columns):
        #self.model_selecter_panel.panel.destroy()
        #self.results_panel = ResultsPanel(self.window, self, 1,model, x_columns, y_columns, self.file)

    def center_window(self, window):
        window.update_idletasks()  # Actualiza el tamaño y posición de la ventana
        width = window.winfo_width()
        height = window.winfo_height()
        x_offset = (window.winfo_screenwidth() - width) // 2
        y_offset = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")