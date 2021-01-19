import tkinter as tk

class HistoryWindow(tk.Toplevel):
    def __init__(self, parent, history_data):
        super().__init__(parent)
        self.title('History')
        self.geometry("400x200")
        self.parent = parent

        self.history_data = history_data
        self.show_history()
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def show_history(self):
        self.listbox = tk.Listbox(self)
        for i, data in enumerate(self.history_data[::-1]):
            self.listbox.insert(i, f"{data}")
        self.listbox.pack(fill=tk.BOTH)

        def lb_callback(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                print(f"chosen option {index}")
                self.parent.load_img_from_history(index)
                self.destroy()
                self.update()
            else:
                print('empty selection')

        self.listbox.bind("<<ListboxSelect>>", lb_callback)
