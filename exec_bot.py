import leetcode_bot
import tkinter as tk
from tkinter import messagebox


def run_script():
    script_input = entry_field.get()
    output = leetcode_bot.outer(script_input)
    messagebox.showinfo("Output", output)


# Create a root window
root = tk.Tk()

# Create a label
label = tk.Label(root, text="Input for the script")
label.pack()

# Create an entry field
entry_field = tk.Entry(root)
entry_field.pack()

# Create a run button
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack()

# Run the tkinter event loop
root.mainloop()