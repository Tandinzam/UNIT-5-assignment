import tkinter as tk

root = tk.Tk()

root.title("Hello World - Tkinter")
root.geometry("400x200")

label = tk.Label(
    root,
    text="Hello, World!",
    font=("Arial", 18)
)

label.pack(expand=True)

root.mainloop()