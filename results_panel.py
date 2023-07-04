from sklearn import linear_model, neighbors, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import tkinter as tk
import pandas as pd

class ResultsPanel:

    def __init__(self, window, self_window, type, model, x_columns, y_column, file):
        self.window = window
        self.window_self = self_window
        self.panel = tk.Frame(self.window)
        self.lblTitle = tk.Label(self.panel, text="Resultados", bg="white", fg="black", font="none 18 bold")

        self.lblFirstModel = tk.Label(self.panel, text="Modelo 1", bg="white", fg="black", font="none 16 bold")
        self.lblSecondModel = tk.Label(self.panel, text="Modelo 2", bg="white", fg="black", font="none 16 bold")
        self.lblThirdModel = tk.Label(self.panel, text="Modelo 3", bg="white", fg="black", font="none 16 bold")

        self.panel.pack(fill=tk.BOTH, expand=True)
        self.lblTitle.pack()

        self.lblFirstModel.pack()
        self.lblSecondModel.pack()
        self.lblThirdModel.pack()
        self.setupLabels(type)

    def setupLabels(self, type):
        self.lblFirstModel.place(x=100, y=50)
        self.lblSecondModel.place(x=100, y=125)
        self.lblThirdModel.place(x=100, y=200)
        if type == 1:
            self.lblFirstModel["text"] = "Linear Regression"
            self.lblSecondModel["text"] = "Ridge Regression"
            self.lblThirdModel["text"] = "Lasso Regression"
        elif type == 2:
            self.lblFirstModel["text"] = "Decission Tree"
            self.lblSecondModel["text"] = "Random Forest"
            self.lblThirdModel["text"] = "KNeighbors"

    def cleanDf(self, df):
        df = df.dropna()
        df = df.drop_duplicates()
        return df