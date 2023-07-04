import tkinter as tk
from tkinter import ttk

import pandas as pd


class SelecterPanel:

    def __init__(self, window, self_window):
        self.window = window
        self.self_window = self_window
        self.window.geometry("1400x700")
        self_window.center_window(self.window)

        self.x_columns = {}
        self.y_columns = {}

        self.model_predicted = tk.StringVar()
        self.model_classifier = tk.StringVar()
        self.model_predicted.set("Linear Regression")
        self.model_classifier.set("KNieghbors")

        self.panel = tk.Frame(self.window)

        # Predicted
        self.cbox_predicted = tk.Checkbutton(self.panel, text="Predecir", bg=None, fg="black", font="none 16 bold")
        self.menu_predicted = tk.OptionMenu(self.panel, self.model_predicted, "Algoritmo 1", "Algoritmo 2", "Algoritmo 3")
        # Classifier
        self.cbox_classifier = tk.Checkbutton(self.panel, text="Clasificar", bg=None, fg="black", font="none 16 bold")
        self.menu_classifier = tk.OptionMenu(self.panel, self.model_classifier, "Algoritmo 1", "Algoritmo 2", "Algoritmo 3")
        # Table
        self.table_container = tk.Frame(self.panel, bg="red")
        self.scrollbar = ttk.Scrollbar(self.table_container, orient=tk.HORIZONTAL)
        self.table = ttk.Treeview(self.table_container, xscrollcommand=self.scrollbar.set)
        # x, y
        self.btn_x = tk.Button(self.panel, text="X", bg="blue", fg="white", font="none 16 bold", command=self.select_x)
        self.btn_y = tk.Button(self.panel, text="Y", bg="blue", fg="white", font="none 16 bold", command=self.select_y)
        self.x_columns_container = tk.Frame(self.panel, bg=None)
        self.y_columns_container = tk.Frame(self.panel, bg=None)
        # Columns
        self.x_columns_list = tk.Listbox(self.x_columns_container, bg=None, font="none 16 bold")
        self.y_columns_list = tk.Listbox(self.y_columns_container, bg=None, font="none 16 bold")

        self.scrollbar.config(command=self.table.xview)
        self.table.configure(xscrollcommand=self.scrollbar.set)
        self.table.bind("<Button-1>", self.column_selected)

        self.panel.pack(fill=tk.BOTH, expand=True)
        self.cbox_predicted.pack()
        self.menu_predicted.pack()
        self.cbox_classifier.pack()
        self.menu_classifier.pack()
        self.table_container.pack()
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.table.pack()
        self.btn_x.pack()
        self.btn_y.pack()

        self.x_columns_container.pack()
        self.y_columns_container.pack()
        self.x_columns_list.pack()
        self.y_columns_list.pack()

        self.cbox_predicted.place(x=50, y=50, width=150, height=30)
        self.menu_predicted.place(x=50, y=100, width=150, height=30)

        self.cbox_classifier.place(x=50, y=200, width=150, height=30)
        self.menu_classifier.place(x=50, y=250, width=150, height=30)

        self.table_container.place(x=250, y=50, width=800, height=600)
        self.table.place(x=0, y=0, width=800, height=585)

        self.btn_x.place(x=50, y=350, width=150, height=30)
        self.btn_y.place(x=50, y=400, width=150, height=30)
        self.x_columns_container.place(x=1100, y=50, width=250, height=500)
        self.y_columns_container.place(x=1100, y=600, width=250, height=50)
        self.x_columns_list.place(x=0, y=0, width=250, height=500)
        self.y_columns_list.place(x=0, y=0, width=250, height=50)

        self.upload_file()

    def upload_file(self):
        file = open(self.self_window.file, 'r')
        self.df = pd.read_csv(file)
        self.clean_df()
        self.headers = self.df.columns.values.tolist()
        self.table["columns"] = self.headers
        for header in self.headers:
            self.table.heading(header, text=header, anchor=tk.CENTER)
            self.table.column(header, anchor=tk.W)
        for i, row in enumerate(self.df.values.tolist()):
            self.table.insert("", "end", text=str(i), values=row)
        file.close()

    def column_selected(self, event):
        x = event.x
        column = self.table.identify_column(x)
        index = int(column.replace("#", "")) 
        self.add_column(index - 1)

    def add_column(self, index):
        header = self.headers[index]
        if self.btn_x["state"] == "disabled":
            if self.x_columns.get(index) is not None:
                del self.x_columns[index]
                self.reload_list()
                return
            if self.y_columns.get(index) is not None:
                return
            self.x_columns[index] = header
            self.x_columns_list.insert(tk.END, header)
        elif self.btn_y["state"] == "disabled":
            if self.y_columns.get(index) is not None:
                del self.y_columns[index]
                self.reload_list()
                return
            if self.x_columns.get(index) is not None:
                return
            self.y_columns = {index: header}
            self.y_columns_list.delete(0, tk.END)
            self.y_columns_list.insert(tk.END, header)


    def reload_list(self):
        self.x_columns_list.delete(0, tk.END)
        self.y_columns_list.delete(0, tk.END)
        for index, header in self.x_columns.items():
            self.x_columns_list.insert(tk.END, header)
        for index, header in self.y_columns.items():
            self.y_columns_list.insert(tk.END, header)


    def select_x(self):
        self.btn_x["state"] = "disabled"
        self.btn_y["state"] = "normal"

    def select_y(self):
        self.btn_x["state"] = "normal"
        self.btn_y["state"] = "disabled"

    def clean_df(self):
        column_count = len(self.df.columns)
        total_row_count = len(self.df.index)
        for i in range(column_count):
            column = self.df.columns[i]
            column_type = self.df[column].dtype
            row_count = self.df[column].count()
            if row_count < total_row_count * 0.70:
                self.df = self.df.drop(column, axis=1)
                continue
            if column_type == "object":
                if self.df[column].unique().size > 10:
                    self.df = self.df.drop(column, axis=1)