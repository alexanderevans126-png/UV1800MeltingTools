# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:04:29 2026

@author: alexa
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from uv1800meltingtools.postmelt import analyze_post_melt


def parse_concentrations(text):
    return [float(x.strip()) for x in text.split(",") if x.strip()]


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        directory_var.set(folder)


def run_analysis():
    try:
        directory_path = directory_var.get().strip()
        experiment_name = experiment_name_var.get().strip()
        concentrations = parse_concentrations(concentrations_var.get())
        wells = int(wells_var.get().strip())
        blanks = int(blanks_var.get().strip())

        if not directory_path:
            raise ValueError("Please choose a folder.")
        if not experiment_name:
            raise ValueError("Please enter an experiment name.")
        if not concentrations:
            raise ValueError("Please enter at least one concentration.")

        results = analyze_post_melt(
            directory_path=directory_path,
            experiment_name=experiment_name,
            concentrations=concentrations,
            wells=wells,
            blanks=blanks,
        )

        output_text = (
            "Analysis complete!\n\n"
            f"Excel file:\n{results['excel_path']}\n\n"
            f"MeltWin PRN file:\n{results['prn_path']}\n\n"
            f"MeltR CSV file:\n{results['meltr_path']}"
        )

        output_var.set(output_text)

    except Exception as error:
        messagebox.showerror("Error", str(error))


root = tk.Tk()
root.title("UV1800 Post-Melt Analysis")
root.geometry("800x450")

main = ttk.Frame(root, padding=20)
main.grid(row=0, column=0, sticky="nsew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main.columnconfigure(1, weight=1)

ttk.Label(main, text="Folder containing .txt files:").grid(row=0, column=0, sticky="w", pady=5)

directory_var = tk.StringVar()
directory_entry = ttk.Entry(main, textvariable=directory_var, width=70)
directory_entry.grid(row=0, column=1, sticky="ew", pady=5)

browse_button = ttk.Button(main, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

ttk.Label(main, text="Experiment name:").grid(row=1, column=0, sticky="w", pady=5)
experiment_name_var = tk.StringVar()
ttk.Entry(main, textvariable=experiment_name_var, width=25).grid(row=1, column=1, sticky="w", pady=5)

ttk.Label(main, text="Concentrations (comma-separated, µM):").grid(row=2, column=0, sticky="w", pady=5)
concentrations_var = tk.StringVar(value="3, 4, 5, 6, 8, 10, 13")
ttk.Entry(main, textvariable=concentrations_var, width=40).grid(row=2, column=1, sticky="w", pady=5)

ttk.Label(main, text="Number of wells:").grid(row=3, column=0, sticky="w", pady=5)
wells_var = tk.StringVar(value="8")
ttk.Entry(main, textvariable=wells_var, width=10).grid(row=3, column=1, sticky="w", pady=5)

ttk.Label(main, text="Number of blanks:").grid(row=4, column=0, sticky="w", pady=5)
blanks_var = tk.StringVar(value="1")
ttk.Entry(main, textvariable=blanks_var, width=10).grid(row=4, column=1, sticky="w", pady=5)

run_button = ttk.Button(main, text="Generate Analysis Files", command=run_analysis)
run_button.grid(row=5, column=0, columnspan=3, pady=20)

output_var = tk.StringVar()
output_label = ttk.Label(
    main,
    textvariable=output_var,
    wraplength=700,
    justify="left",
)
output_label.grid(row=6, column=0, columnspan=3, sticky="w", pady=10)

root.mainloop()