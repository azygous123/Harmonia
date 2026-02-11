#!/usr/bin/python3
import tkinter as tk

root = tk.Tk()
root.title("Pynorfair IDE")
root.geometry("800x600")  # optional, just a nice starting size

# Text editor widget
text_editor = tk.Text(root, wrap="none")
text_editor.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(root, command=text_editor.yview)
scrollbar.pack(side="right", fill="y")

text_editor.config(yscrollcommand=scrollbar.set)

root.mainloop()
