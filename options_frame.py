import tkinter as tk
from PIL import ImageTk, Image
from functools import partial

from image_editor import ImageEditor

class OptionsFrame(tk.Frame):
    frame_width = 300
    def __init__(self, master=None):
        super().__init__(master, width=OptionsFrame.frame_width, height=600, bg="gray")

        canvas = tk.Canvas(self, width=OptionsFrame.frame_width-20, height=600, bg="gray")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg = "gray")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.grid_propagate(0)
        self.master = master

    def create_menu(self, img):
        padding = 5
        img_orig = img
        img = img.copy()
        img.thumbnail((OptionsFrame.frame_width//2 - padding * 3 - 10, OptionsFrame.frame_width//2 - padding * 3 - 10))

        image_editor_model = ImageEditor()
        image_editor_model.load_image(img)

        def on_effect_click(effect_fun):
            self.master.load_image_preview(effect_fun(img_orig))
            self.master.crop_params = None

        def on_index(ind, event):
            on_effect_click(image_editor_model.get_effect(ind)[0])

        accept_btn = tk.Button(self.scrollable_frame, text = "Apply")
        accept_btn.grid(row=0, column=0, padx=padding, pady = padding, sticky="nesw")
        def on_apply():
            if self.master.crop_params != None:
                print("cropping!")
                self.master.img = self.master.img.crop(self.master.crop_params)
                self.master.crop_params = None
            self.master.load_image(self.master.img)

        accept_btn['command'] = on_apply

        cancel_btn = tk.Button(self.scrollable_frame, text = "Revert")
        cancel_btn.grid(row=0, column=1, padx=padding, pady = padding, sticky="nesw")
        def on_cancel():
            self.master.load_options_prev(self.master.img_orig)
            self.master.load_image_preview(self.master.img_orig)
        cancel_btn['command'] = on_cancel

        for i, image_with_effect in enumerate(image_editor_model.get_images_with_effects()):
            thumbn_frame = tk.Frame(self.scrollable_frame, bg="black")
            thumbn_frame.grid(row=((i + 2)//2), column=(i%2), pady=padding, padx=padding, sticky="W")
            thumbn_frame.bind("<Button-1>", partial(on_index, i))

            #image_with_effect[0].thumbnail((OptionsFrame.frame_width//2, OptionsFrame.frame_width//2))
            img_tk = ImageTk.PhotoImage(image=image_with_effect[0])

            thumbn_photo = tk.Label(thumbn_frame, text='image_here', image=img_tk)
            thumbn_photo.image = img_tk
            thumbn_photo.pack(side=tk.TOP)
            thumbn_photo.bind("<Button-1>", partial(on_index, i))

            thumbn_name = tk.Label(thumbn_frame, text=image_with_effect[1])
            thumbn_name.pack(side=tk.TOP)
            thumbn_name.bind("<Button-1>", partial(on_index, i))
