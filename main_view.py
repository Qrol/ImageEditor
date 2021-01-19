import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import pickle
from PIL import ImageTk, Image, UnidentifiedImageError

from history import HistoryWindow
from photo_frame import PhotoFrame
from options_frame import OptionsFrame

history_filename = 'history.data'

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        self.menu = tk.Menu(self.master)
        self.menu_file = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label = 'File', menu=self.menu_file)
        self.menu_file.add_command(label = "Load", command=self.load_img_from_dialog)
        self.menu_file.add_command(label = "Save", command=self.save_image)
        self.menu_file.add_command(label = "Save As", command=self.save_image_as)

        self.menu_history= tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label = 'History', menu=self.menu_history)
        self.menu_history.add_command(label = "Load history", command=self.on_load_history)

        self.master.config(menu = self.menu)

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=5, uniform='x')
        self.grid_columnconfigure(1, weight=3, uniform='x')
        self.grid_rowconfigure(0, weight=1, uniform='x')

        self.photo_frame = PhotoFrame(lambda: self.load_img_from_dialog(), self)
        self.photo_frame.grid(row=0, column=0)

        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=0, column=1)

    def load_img_from_dialog(self):
        self.image_path = tk.filedialog.askopenfilename(filetypes=[('Obrazy', '.png .jpg .jpeg')])
        if not self.image_path:
            return
        self.img = Image.open(self.image_path)
        self.load_image(self.img)

        return self.img

    def load_image(self, img):
        self.img_orig = self.img
        self.load_image_preview(img)
        self.load_options_prev(img)

        self.photo_frame.load_img_button.place_forget()

    def load_options_prev(self, img):
        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=0, column=1)
        self.options_frame.create_menu(img)

    def load_image_preview(self, img):
        self.photo_frame.display_image(img)
        self.img = img

    def load_img_from_history(self, index):
        self.image_path = self.history[::-1][index]
        try:
            self.img = Image.open(self.image_path)
            self.load_image(self.img)
        except UnidentifiedImageError:
            tk.messagebox.showinfo("File doesn't exist", f'File "{self.image_path}" does not exist. Reference is getting removed from history')
            del self.history[-index - 1]
            self.save_history(history_filename, self.history)
            self.image_path = None

    @staticmethod
    def save_image_glob(img, path):
        img.save(path)
        print(f"image saved to {path}")

    def save_image(self):
        Application.save_image_glob(self.img, self.image_path)

        self.load_history(history_filename)

        self.history = self.load_history(history_filename)
        if self.image_path in self.history:
            self.history.remove(self.image_path)

        self.history.append(self.image_path)

        self.save_history(history_filename, self.history)

    def save_image_as(self):
        self.image_path = tk.filedialog.asksaveasfilename(filetypes=[('Obrazy', '.png .jpg .jpeg')])
        if not self.image_path:
            return
        self.save_image()

    def save_history(self, file_name, data):
        with open(file_name, mode='wb') as f:
            pickle.dump(data, f)

    def load_history(self, file_name):
        try:
            with open(file_name, mode='rb') as f:
                history_data = pickle.load(f)
        except FileNotFoundError:
            history_data = []
        finally:
            return history_data

    def on_load_history(self):
        self.history = self.load_history(history_filename)
        HistoryWindow(self, self.history)

def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.resizable(False, False)
    root.title('Photo editor')
    app = Application(master=root)

    app.mainloop()

if __name__ == '__main__':
    main()
