import tkinter as tk
from PIL import ImageTk

class PhotoFrame(tk.Frame):
    def __init__(self, load_func, master=None):
        super().__init__(master, width=500, height=600, padx=10)
        self.pack_propagate(0)
        self.master = master
        self.img_canv = None
        self.create_load_button(load_func)

    def on_load(self, load_func):
        img = load_func()

    def create_load_button(self, load_func):
        self.load_img_button = tk.Button(self, text="Load image")
        self.load_img_button.place(relx=.5, rely=.5, anchor="center")
        self.load_img_button['command'] = lambda: self.on_load(load_func)

    def display_image(self, img):
        img = img.copy()
        img.thumbnail((500, 500))
        width, height = img.size
        self.img_tk = ImageTk.PhotoImage(image=img)
        if self.img_canv != None:
            self.img_canv.pack_forget()
            self.img_canv.destroy()

        self.img_canv = tk.Canvas(self, width=width, height=height, bg="black")
        self.img_id = self.img_canv.create_image(0,0, anchor=tk.NW, image=self.img_tk)
        self.rect = None
        self.img_canv.bind('<Button-1>', lambda event: self.cut_rectangle_start(event))
        self.img_canv.bind('<B1-Motion>', lambda event: self.cut_rectangle(event))
        self.img_canv.bind('<ButtonRelease-1>', lambda event: self.cut_rectangle_stop(event))


        self.img_canv.pack() # pady=(600 - height)/2

    def cut_rectangle_start(self, event):
        if self.rect != None:
            self.img_canv.delete(self.rect)
        self.cut_coords_start = event.x, event.y

    def cut_rectangle(self, event):
        if self.rect != None:
            self.img_canv.delete(self.rect)
        x1, y1 = self.cut_coords_start
        x2, y2 = event.x, event.y
        if(x2 < x1):
            temp = x1
            x1 = x2
            x2 = temp
        if(y2 < y1):
            temp = y1
            y1 = y2
            y2 = temp
        self.rect_params = (x1, y1, x2, y2)
        self.rect = self.img_canv.create_rectangle(x1, y1, x2, y2)

    def cut_rectangle_stop(self, event):
        print(f"{self.img_canv.winfo_width()}, {self.img_canv.winfo_height()}")
        prev_width, prev_height = self.img_canv.winfo_width(), self.img_canv.winfo_height()
        x1, y1, x2, y2 = self.rect_params
        img = self.master.img
        left = int(x1 / prev_width * img.size[0])
        top = int(y1 / prev_height * img.size[1])
        right = int(x2 / prev_width * img.size[0])
        bot = int(y2/prev_height * img.size[1])
        print((left, top, right, bot))
        self.master.crop_params = (left, top, right, bot)
        print(img.size)
