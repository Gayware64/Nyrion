import os
import platform
import time
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

VERSION = "Nyrion v1.3.1 - Lion 0.1.9 (Copyright GayWare64)"

class NyrionShell(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nyrion 1.3")
        self.geometry("900x600")
        self.configure(bg="#282c34")

        self.command_history = []
        self.chat_log = []

        # Create UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Top Frame: Buttons for apps
        top_frame = tk.Frame(self, bg="#21252b")
        top_frame.pack(fill='x')

        buttons = [
            ("Help", self.show_help),
            ("Specs", self.show_specs),
            ("Version", self.show_version),
            ("Base", self.show_base),
            ("Web", self.open_web),
            ("Edit", self.launch_editor),
            ("Explore", self.open_file_explorer),
            ("New File", self.create_file),
            ("New Folder", self.create_folder),
            ("Read File", self.read_file_prompt),
            ("Chat", self.open_chatbot),
            ("Chat Log", self.view_chatlog),
            ("Draw", self.open_ascii_draw),
            ("History", self.show_history),
            ("Clear", self.clear_output),
            ("Exit", self.exit_app),
        ]

        for (text, cmd) in buttons:
            btn = tk.Button(top_frame, text=text, command=cmd, bg="#3b3f6b", fg="white")
            btn.pack(side='left', padx=2, pady=5)

        # Main Text Output Area
        self.output = scrolledtext.ScrolledText(self, bg="#1e1e2f", fg="white", font=("Consolas", 12))
        self.output.pack(fill='both', expand=True, padx=10, pady=10)

        self.write_output(f"Welcome to Nyrion GUI v{VERSION}\nType Help for commands.\n")

    def write_output(self, text):
        self.output.insert('end', text)
        self.output.see('end')

    def clear_output(self):
        self.output.delete(1.0, 'end')

    # Command functions
    def show_help(self):
        help_text = """
Available Commands:
Help        - Show this help message
Specs       - Show system specs
Version     - Show version info
Base        - Show OS info
Web         - Open browser to Google
Edit        - Launch text editor
Explore     - Open file explorer
New File    - Create a new file
New Folder  - Create a new folder
Read File   - View contents of a file
Chat        - Open chatbot window
Chat Log    - View/save chatbot log
Draw        - Open ASCII drawing tool
History     - Show recent commands
Clear       - Clear output
Exit        - Quit application
"""
        self.write_output(help_text + "\n")
        self.command_history.append("help")

    def show_specs(self):
        specs = f"OS: {platform.system()} {platform.release()}\nCPU: {platform.processor()}\nPython: {platform.python_version()}\n"
        self.write_output(specs + "\n")
        self.command_history.append("specs")

    def show_version(self):
        self.write_output(f"Nyrion Shell Version: {VERSION}\n\n")
        self.command_history.append("version")

    def show_base(self):
        self.write_output(f"Platform: {platform.platform()}\n\n")
        self.command_history.append("base")

    def open_web(self):
        webbrowser.open("https://www.google.com")
        self.write_output("Opening web browser to Google...\n\n")
        self.command_history.append("web")

    def launch_editor(self):
        try:
            if os.name == "nt":
                os.system("notepad")
            else:
                os.system("nano")
            self.write_output("Launched editor.\n\n")
        except Exception as e:
            self.write_output(f"Error launching editor: {e}\n\n")
        self.command_history.append("edit")

    def open_file_explorer(self):
        FileExplorer(self, os.getcwd())
        self.command_history.append("explore")

    def create_file(self):
        def save_file():
            filename = entry.get().strip()
            if not filename:
                messagebox.showerror("Error", "File name cannot be empty.")
                return
            try:
                with open(filename, "w") as f:
                    pass
                messagebox.showinfo("Success", f"File '{filename}' created.")
                top.destroy()
                self.write_output(f"Created file: {filename}\n\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        top = tk.Toplevel(self)
        top.title("Create New File")
        tk.Label(top, text="Enter new file name:").pack(pady=5)
        entry = tk.Entry(top, width=40)
        entry.pack(padx=10)
        tk.Button(top, text="Create", command=save_file).pack(pady=10)
        self.command_history.append("newfile")

    def create_folder(self):
        def save_folder():
            foldername = entry.get().strip()
            if not foldername:
                messagebox.showerror("Error", "Folder name cannot be empty.")
                return
            try:
                os.makedirs(foldername, exist_ok=True)
                messagebox.showinfo("Success", f"Folder '{foldername}' created.")
                top.destroy()
                self.write_output(f"Created folder: {foldername}\n\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        top = tk.Toplevel(self)
        top.title("Create New Folder")
        tk.Label(top, text="Enter new folder name:").pack(pady=5)
        entry = tk.Entry(top, width=40)
        entry.pack(padx=10)
        tk.Button(top, text="Create", command=save_folder).pack(pady=10)
        self.command_history.append("newfolder")

    def read_file_prompt(self):
        def read_file():
            filename = entry.get().strip()
            if not filename:
                messagebox.showerror("Error", "File name cannot be empty.")
                return
            if not os.path.isfile(filename):
                messagebox.showerror("Error", "File not found.")
                return
            try:
                with open(filename, "r") as f:
                    content = f.read()
                top.destroy()
                self.write_output(f"--- Contents of {filename} ---\n{content}\n---------------------------\n\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        top = tk.Toplevel(self)
        top.title("Read File")
        tk.Label(top, text="Enter file name to read:").pack(pady=5)
        entry = tk.Entry(top, width=50)
        entry.pack(padx=10)
        tk.Button(top, text="Read", command=read_file).pack(pady=10)
        self.command_history.append("readfile")

    def open_chatbot(self):
        ChatbotWindow(self, self.chat_log)
        self.command_history.append("chat")

    def view_chatlog(self):
        if not self.chat_log:
            self.write_output("No chat history yet.\n\n")
            return
        try:
            with open("chatlog.txt", "w") as f:
                f.write("\n".join(self.chat_log))
            self.write_output("Chat log saved to 'chatlog.txt'. Last 5 lines:\n")
            self.write_output("\n".join(self.chat_log[-5:]) + "\n\n")
        except Exception as e:
            self.write_output(f"Error saving chat log: {e}\n\n")
        self.command_history.append("chatlog")

    def open_ascii_draw(self):
        ASCIIDrawWindow(self)
        self.command_history.append("draw")

    def show_history(self):
        if not self.command_history:
            self.write_output("No commands executed yet.\n\n")
            return
        self.write_output("Last 10 commands:\n" + "\n".join(self.command_history[-10:]) + "\n\n")
        self.command_history.append("history")

    def exit_app(self):
        self.write_output("Goodbye!\n")
        self.after(500, self.destroy)

# --- Additional Windows ---

class FileExplorer(tk.Toplevel):
    def __init__(self, master, start_path):
        super().__init__(master)
        self.title("File Explorer")
        self.geometry("700x500")
        self.configure(bg="#282c34")

        self.current_path = start_path

        self.path_var = tk.StringVar(value=self.current_path)
        path_entry = tk.Entry(self, textvariable=self.path_var, font=("Segoe UI", 12))
        path_entry.pack(fill='x', padx=10, pady=5)
        path_entry.bind("<Return>", self.go_to_path)

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree.heading("#0", text="Files and Folders", anchor='w')
        self.populate_tree(self.current_path)

        self.tree.bind("<Double-1>", self.on_double_click)

    def populate_tree(self, path):
        self.tree.delete(*self.tree.get_children())
        try:
            items = os.listdir(path)
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    self.tree.insert("", "end", iid=full_path, text=item, values=("Folder",))
                else:
                    self.tree.insert("", "end", iid=full_path, text=item, values=("File",))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_double_click(self, event):
        item = self.tree.focus()
        if os.path.isdir(item):
            self.current_path = item
            self.path_var.set(item)
            self.populate_tree(item)
        else:
            try:
                if os.name == "nt":
                    os.startfile(item)
                else:
                    # On macOS/Linux, open with default app
                    import subprocess
                    subprocess.Popen(["xdg-open", item])
            except Exception:
                messagebox.showinfo("Open", f"Cannot open file: {item}")

    def go_to_path(self, event):
        path = self.path_var.get()
        if os.path.exists(path) and os.path.isdir(path):
            self.current_path = path
            self.populate_tree(path)
        else:
            messagebox.showerror("Error", "Path does not exist or is not a directory.")

class ChatbotWindow(tk.Toplevel):
    def __init__(self, master, chat_log):
        super().__init__(master)
        self.title("Chatbot")
        self.geometry("500x400")
        self.configure(bg="#282c34")
        self.chat_log = chat_log

        self.text_area = scrolledtext.ScrolledText(self, state='disabled', bg="#1e1e2f", fg="white",
                                                   font=("Segoe UI", 11))
        self.text_area.pack(fill='both', expand=True, padx=10, pady=10)

        self.entry = tk.Entry(self, font=("Segoe UI", 12))
        self.entry.pack(fill='x', padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.process_input)

        self.show_welcome()

    def show_welcome(self):
        self.append_text("Chatbot: Hello! Ask me anything.\n")

    def append_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert('end', text)
        self.text_area.config(state='disabled')
        self.text_area.see('end')

    def process_input(self, event):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.append_text(f"You: {user_text}\n")
        self.entry.delete(0, 'end')

        # Simple chatbot logic
        user_lower = user_text.lower()
        if user_lower == "exit":
            self.append_text("Chatbot: Bye!\n")
            self.destroy()
            return
        elif "hello" in user_lower:
            reply = "Hi there!"
        elif "time" in user_lower:
            reply = "The time is " + time.strftime("%H:%M:%S")
        elif "name" in user_lower:
            reply = "I'm NyrionBot!"
        else:
            reply = "I don't understand that yet."

        self.append_text(f"Chatbot: {reply}\n")
        self.chat_log.append(f"You: {user_text}\nBot: {reply}\n")

class ASCIIDrawWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("ASCII Draw")
        self.geometry("420x300")
        self.configure(bg="#282c34")

        self.grid_width = 20
        self.grid_height = 10
        self.grid = [[" " for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        self.text_area = tk.Text(self, font=("Courier New", 14), bg="#1e1e2f", fg="white", width=40, height=12)
        self.text_area.pack(padx=10, pady=10)

        bottom_frame = tk.Frame(self, bg="#282c34")
        bottom_frame.pack(fill='x')

        tk.Label(bottom_frame, text="Draw (x y char):", fg="white", bg="#282c34").pack(side='left', padx=5)
        self.entry = tk.Entry(bottom_frame, width=10)
        self.entry.pack(side='left')
        self.entry.bind("<Return>", self.draw_char)

        tk.Button(bottom_frame, text="Save", command=self.save_drawing).pack(side='left', padx=5)
        tk.Button(bottom_frame, text="Clear", command=self.clear_grid).pack(side='left', padx=5)
        tk.Button(bottom_frame, text="Exit", command=self.destroy).pack(side='left', padx=5)

        self.update_text_area()

    def update_text_area(self):
        self.text_area.delete(1.0, 'end')
        for row in self.grid:
            self.text_area.insert('end', "".join(row) + "\n")

    def draw_char(self, event):
        cmd = self.entry.get().strip()
        self.entry.delete(0, 'end')
        try:
            x, y, ch = cmd.split()
            x, y = int(x), int(y)
            if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
                self.grid[y][x] = ch[0]
                self.update_text_area()
            else:
                messagebox.showerror("Error", "Coordinates out of bounds.")
        except:
            messagebox.showerror("Error", "Invalid format. Use: x y char")

    def save_drawing(self):
        try:
            with open("drawing.txt", "w") as f:
                for row in self.grid:
                    f.write("".join(row) + "\n")
            messagebox.showinfo("Saved", "Drawing saved to 'drawing.txt'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_grid(self):
        self.grid = [[" " for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.update_text_area()

if __name__ == "__main__":
    try:
        app = NyrionShell()
        app.mainloop()
    except Exception as e:
        import traceback
        print("An error occurred:")
        traceback.print_exc()
        input("Press Enter to exit...")


