import tkinter as tk
from tkinter import messagebox


def calculate():
    try:
        n1 = float(entry1.get())
        n2 = float(entry2.get())
        n3 = float(entry3.get())

        res = (n1 - n2) * n3
        result_label.config(text=f"Result: {res}", fg="blue")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")


# ساخت پنجره
app = tk.Tk()
app.title("Calculator")
app.geometry("300x250")

tk.Label(app, text="Number 1:").pack(pady=2)
entry1 = tk.Entry(app)
entry1.pack()

tk.Label(app, text="Number 2:").pack(pady=2)
entry2 = tk.Entry(app)
entry2.pack()

tk.Label(app, text="Number 3:").pack(pady=2)
entry3 = tk.Entry(app)
entry3.pack()

tk.Button(
    app, text="Calculate", command=calculate, bg="green", fg="white"
).pack(pady=15)

result_label = tk.Label(app, text="Result: -", font=("Arial", 12, "bold"))
result_label.pack()

app.mainloop()a
