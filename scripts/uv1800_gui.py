# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:46:42 2026

@author: alexa
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

from uv1800meltingtools.extinctioncoeff import epsilon_nn
from uv1800meltingtools.concentration import concentration_series


def calculate():
    try:
        seq = sequence_entry.get().strip()
        molecule = molecule_var.get()
        num = int(num_entry.get().strip())
        pathlength = float(pathlength_entry.get().strip())

        epsilon = epsilon_nn(seq, molecule=molecule)
        concentrations = concentration_series(
            epsilon=epsilon,
            num_concentrations=num,
            pathlength=pathlength,
        )

        epsilon_output.set(f"{epsilon:,} M⁻¹ cm⁻¹")
        formatted = ", ".join(str(val) for val in concentrations)
        concentration_output.set(formatted)

    except Exception as error:
        messagebox.showerror("Error", str(error))


root = tk.Tk()
root.geometry("700x400")
large_font = tkfont.Font(size=14)
root.title("UV1800 Melting Tools")

main = ttk.Frame(root, padding=20)
main.grid(row=0, column=0)

ttk.Label(main, text="Sequence 5'→3':").grid(row=0, column=0, sticky="w")
sequence_entry = ttk.Entry(main, width=40)
sequence_entry.grid(row=0, column=1, pady=5)

ttk.Label(main, text="Molecule:").grid(row=1, column=0, sticky="w")
molecule_var = tk.StringVar(value="DNA")
molecule_menu = ttk.Combobox(
    main,
    textvariable=molecule_var,
    values=["DNA", "RNA"],
    state="readonly",
    width=10,
)
molecule_menu.grid(row=1, column=1, sticky="w", pady=5)

ttk.Label(main, text="Number of concentrations:").grid(row=2, column=0, sticky="w")
num_entry = ttk.Entry(main, width=10)
num_entry.insert(0, "7")
num_entry.grid(row=2, column=1, sticky="w", pady=5)

ttk.Label(main, text="Pathlength (cm):").grid(row=3, column=0, sticky="w")
pathlength_entry = ttk.Entry(main, width=10)
pathlength_entry.insert(0, "1")
pathlength_entry.grid(row=3, column=1, sticky="w", pady=5)

calculate_button = ttk.Button(main, text="Calculate", command=calculate)
calculate_button.grid(row=4, column=0, columnspan=2, pady=15)

ttk.Label(main, text="Extinction coefficient:").grid(row=5, column=0, sticky="w")
epsilon_output = tk.StringVar()
ttk.Label(main, textvariable=epsilon_output, font=large_font).grid(row=5, column=1, sticky="w")

ttk.Label(main, text="Concentrations (µM):").grid(row=6, column=0, sticky="w")
concentration_output = tk.StringVar()
ttk.Label(
    main,
    textvariable=concentration_output,
    wraplength=500,
    justify="left",
    font=large_font).grid(row=6, column=1, sticky="w")

root.mainloop()