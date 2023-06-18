import leetcode_bot
import tkinter as tk
from tkinter import messagebox


def run_script():
    script_input = entry_field.get()
    output = leetcode_bot.outer(script_input)
    # Insert the output into the text widget
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)


# Create a root window
root = tk.Tk()


# Set the window title
root.title("Yihao's Leetcode Bot GUI")

# Set the window size
root.geometry("800x600")


# Create a label
label = tk.Label(root, text="Leetcode URL")
label.pack()

# Create an entry field
entry_field = tk.Entry(root)
entry_field.pack()

# Create a run button
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack()


# Add an output text widget
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=20)

# Run the tkinter event loop
root.mainloop()