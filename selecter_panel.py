import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel, config

import pandas as pd
import math


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
        self.is_predicted = tk.BooleanVar()
        self.is_classifier = tk.BooleanVar()
        self.is_predicted.set(True)
        self.model_predicted.set("Linear Regression")
        self.model_classifier.set("KNieghbors")

        self.panel = tk.Frame(self.window)

        # Predicted
        self.cbox_predicted = tk.Checkbutton(self.panel, text="Predecir", bg=None, fg="black", font="none 16 bold", command=self.predicted_selected, variable=self.is_predicted)
        self.menu_predicted = tk.OptionMenu(self.panel, self.model_predicted, "Algoritmo 1", "Algoritmo 2", "Algoritmo 3")
        # Classifier
        self.cbox_classifier = tk.Checkbutton(self.panel, text="Clasificar", bg=None, fg="black", font="none 16 bold", command=self.classifier_selected, variable=self.is_classifier)
        self.menu_classifier = tk.OptionMenu(self.panel, self.model_classifier, "Algoritmo 1", "Algoritmo 2", "Algoritmo 3")
        # Table
        self.table_container = tk.Frame(self.panel, bg="red")
        # x, y
        self.btn_x = tk.Button(self.panel, text="X", bg="blue", fg="white", font="none 16 bold", command=self.select_x)
        self.btn_y = tk.Button(self.panel, text="Y", bg="blue", fg="white", font="none 16 bold", command=self.select_y)
        self.x_columns_container = tk.Frame(self.panel, bg=None)
        self.y_columns_container = tk.Frame(self.panel, bg=None)
        # Columns
        self.x_columns_list = tk.Listbox(self.x_columns_container, bg=None, font="none 16 bold")
        self.y_columns_list = tk.Listbox(self.y_columns_container, bg=None, font="none 16 bold")

        self.panel.pack(fill=tk.BOTH, expand=True)
        self.cbox_predicted.pack()
        self.menu_predicted.pack()
        self.cbox_classifier.pack()
        self.menu_classifier.pack()
        self.table_container.pack()
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

        self.btn_x.place(x=50, y=350, width=150, height=30)
        self.btn_y.place(x=50, y=400, width=150, height=30)
        self.x_columns_container.place(x=1100, y=50, width=250, height=500)
        self.y_columns_container.place(x=1100, y=600, width=250, height=50)
        self.x_columns_list.place(x=0, y=0, width=250, height=500)
        self.y_columns_list.place(x=0, y=0, width=250, height=50)

        self.upload_file()

    def predicted_selected(self):
        if not self.is_predicted.get():
            self.recommend_classifier_y_columns()
            self.is_classifier.set(True)
        else: 
            self.recommend_predicted_y_columns()
            self.is_classifier.set(False)

    def classifier_selected(self):
        if not self.is_classifier.get():
            self.recommend_predicted_y_columns()
            self.is_predicted.set(True)
        else:
            self.recommend_classifier_y_columns()
            self.is_predicted.set(False)


    def upload_file(self):
        file = open(self.self_window.file, 'r')
        self.df = pd.read_csv(file)
        self.clean_df()
        self.verify_columns_sequence()
        self.model = TableModel(self.df)
        self.table = Table(self.table_container, model=self.model, editable=False, enable_menus=False)
        self.table.bind("<Button-1>", self.column_selected)
        self.table.show()
        file.close()

    def column_selected(self, event):
        column = self.table.get_col_clicked(event)
        column_name = self.df.columns[column]
        # self.table.columncolors[column_name] = '#ff0000'
        self.table.redraw()
        # LOGICA PARA AGREGAR LA COLUMNA A LA LISTA
        

    def add_column(self, column_name, index):
        if self.btn_x["state"] == "disabled":
            if self.x_columns.get(index) is not None:
                del self.x_columns[index]
                self.reload_list()
                return
            if self.y_columns.get(index) is not None:
                return
            self.x_columns[index] = column_name
            self.x_columns_list.insert(tk.END, column_name)
        elif self.btn_y["state"] == "disabled":
            if self.y_columns.get(index) is not None:
                del self.y_columns[index]
                self.reload_list()
                return
            if self.x_columns.get(index) is not None:
                return
            self.y_columns = {index: column_name}
            self.y_columns_list.delete(0, tk.END)
            self.y_columns_list.insert(tk.END, column_name)


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
        total_row_count = len(self.df.index)
        for column in self.df.columns:
            column_type = self.df[column].dtype
            row_count = self.df[column].count()
            if row_count < total_row_count * 0.70:
                self.df = self.df.drop(column, axis=1)
                continue
            if column_type == "object":
                if self.df[column].unique().size > 10:
                    self.df = self.df.drop(column, axis=1)

    def verify_columns_sequence(self):
        is_sequence = True
        for column in self.df.columns:
            if self.df[column].dtype == "object":
                continue
            limit = math.ceil(len(self.df[column].index) * 0.25)
            for i in range(1, limit):
                if self.df[column][i] + 1 != self.df[column][i + 1]:
                    is_sequence = False
            if is_sequence:
                self.df = self.df.drop(column, axis=1)

    def recommend_predicted_y_columns(self):
        self.remove_all_color_columns()
        for column_name in self.df.columns:
            column_type = self.df[column_name].dtype
            if column_type != "object":
                self.paint_column(column_name)

    def recommend_classifier_y_columns(self):
        self.remove_all_color_columns()
        for column_name in self.df.columns:
            column_type = self.df[column_name].dtype
            if column_type == "object":
                self.paint_column(column_name)

    def remove_all_color_columns(self):
        for column_name in self.df.columns:
            self.table.columncolors[column_name] = '#ffffff'
            self.table.redraw()

    def paint_column(self, column_name):
        self.table.columncolors[column_name] = '#ebc034'
        self.table.redraw()

# Falta que no se muevan las columnas