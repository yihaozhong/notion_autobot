import leetcode_bot
import tkinter as tk
from tkinter import messagebox, ttk, tkFont
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

def run_script():
    script_input = entry_field.get()
    output = leetcode_bot.outer(script_input)
    # Insert the output into the text widget
    #output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, current_time+output)


# Create a root window
root = tk.Tk()
custom_font = tkFont.Font(family="Helvetica", size=18)

# Set the window title
root.title(u"Yihao's Leetcode Bot GUI \U0001F916")

# Set the window size
root.geometry("800x600")


# Create a label
label = tk.Label(root, text=u"Leetcode URL \U0001F517", font=custom_font)
label.pack(pady=20)

# Create an entry field
entry_field = tk.Entry(root, font=custom_font, width=100)
entry_field.pack(pady=20)

# Create a progress bar
progress_bar = ttk.Progressbar(root, length=200, mode='indeterminate')

# Create a run button
run_button = tk.Button(root, text="Run Script", command=run_script, font=custom_font)
run_button.pack(pady=20)


# Add an output text widget
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=20)


# Run the tkinter event loop
root.mainloop()