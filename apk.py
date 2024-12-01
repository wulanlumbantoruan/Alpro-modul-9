import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import threading


# Fungsi untuk Timer Belajar
class TimerBelajar:
    def __init__(self, root):
        self.time_left = 0
        self.running = False

        self.timer_frame = ttk.Frame(root)
        self.timer_frame.pack(pady=10)

        self.time_label = ttk.Label(self.timer_frame, text="00:00:00", font=("Arial", 24))
        self.time_label.pack()

        self.start_button = ttk.Button(self.timer_frame, text="Mulai", command=self.start_timer)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(self.timer_frame, text="Hentikan", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=5)

        self.reset_button = ttk.Button(self.timer_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=5)

    def update_timer(self):
        while self.running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            self.display_time()

        if self.time_left == 0:
            messagebox.showinfo("Waktu Habis", "Timer selesai!")
            self.running = False

    def display_time(self):
        hours, remainder = divmod(self.time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def start_timer(self):
        if not self.running:
            self.time_left = 1500  # Default waktu 25 menit
            self.running = True
            threading.Thread(target=self.update_timer, daemon=True).start()

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.time_left = 0
        self.display_time()


# Fungsi untuk Catatan Harian
class CatatanHarian:
    def __init__(self, root):
        self.note_frame = ttk.Frame(root)
        self.note_frame.pack(pady=10)

        self.text_area = tk.Text(self.note_frame, height=10, width=40)
        self.text_area.pack()

        self.save_button = ttk.Button(self.note_frame, text="Simpan", command=self.save_note)
        self.save_button.pack(side="left", padx=5)

        self.open_button = ttk.Button(self.note_frame, text="Buka", command=self.open_note)
        self.open_button.pack(side="left", padx=5)

    def save_note(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))
            messagebox.showinfo("Sukses", "Catatan disimpan!")

    def open_note(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, content)


# Fungsi untuk To-Do List
class ToDoList:
    def __init__(self, root):
        self.todo_frame = ttk.Frame(root)
        self.todo_frame.pack(pady=10)

        self.task_entry = ttk.Entry(self.todo_frame, width=30)
        self.task_entry.pack(side="left", padx=5)

        self.add_button = ttk.Button(self.todo_frame, text="Tambah", command=self.add_task)
        self.add_button.pack(side="left", padx=5)

        self.task_listbox = tk.Listbox(root, height=10, width=50, selectmode=tk.SINGLE)
        self.task_listbox.pack()

        self.delete_button = ttk.Button(root, text="Hapus", command=self.delete_task)
        self.delete_button.pack()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Peringatan", "Tugas tidak boleh kosong!")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.task_listbox.delete(selected_task_index)
        else:
            messagebox.showwarning("Peringatan", "Pilih tugas yang akan dihapus!")


# Fungsi untuk Kalkulator Sederhana
class Kalkulator:
    def __init__(self, root):
        self.calc_frame = ttk.Frame(root)
        self.calc_frame.pack(pady=10)

        self.expression = ""

        self.display = ttk.Entry(self.calc_frame, width=30)
        self.display.grid(row=0, column=0, columnspan=4, pady=5)

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (text, row, col) in buttons:
            button = ttk.Button(self.calc_frame, text=text, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5)

    def on_button_click(self, char):
        if char == "=":
            try:
                result = eval(self.expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.expression = ""
            except Exception:
                messagebox.showerror("Error", "Ekspresi tidak valid!")
                self.display.delete(0, tk.END)
        else:
            self.expression += char
            self.display.insert(tk.END, char)


# Aplikasi Utama
class StudentProductivityToolkit:
    def __init__(self, root):
        root.title("Student Productivity Toolkit")
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        timer_tab = ttk.Frame(notebook)
        notes_tab = ttk.Frame(notebook)
        todo_tab = ttk.Frame(notebook)
        calc_tab = ttk.Frame(notebook)

        notebook.add(timer_tab, text="Timer Belajar")
        notebook.add(notes_tab, text="Catatan Harian")
        notebook.add(todo_tab, text="To-Do List")
        notebook.add(calc_tab, text="Kalkulator")

        TimerBelajar(timer_tab)
        CatatanHarian(notes_tab)
        ToDoList(todo_tab)
        Kalkulator(calc_tab)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentProductivityToolkit(root)
    root.mainloop()
