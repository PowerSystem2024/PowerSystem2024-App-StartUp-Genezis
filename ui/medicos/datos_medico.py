from tkinter import *

class DatosMedicoFrame(Frame):
    def __init__(self, parent, datos):
        super().__init__(parent)

        Label(self, text="Datos del Médico", font=("Arial", 14, "bold")).pack(pady=10)

        for key, value in datos.items():
            Label(self, text=f"{key}: {value}", anchor="w").pack(fill=X, padx=10)