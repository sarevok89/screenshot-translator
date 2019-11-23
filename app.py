import boto3
import cv2
import numpy as np
import pyscreenshot
import pytesseract
import subprocess
import tkinter as tk

from random import choice


class MyApp:
    def __init__(self, parent):
        self.root = parent
        self.window_height = self.root.winfo_screenheight()
        self.root.overrideredirect(True)
        self.window_width = self.root.winfo_screenwidth()
        self.root.geometry(
            f'{self.window_width}x{self.window_height}+0+0')
        self.root.wait_visibility()
        self.root.wm_attributes('-alpha', 0.2)
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, cursor="diamond_cross")
        self.canvas.pack(fill='both', expand=True)
        self.rectangle_start_x = 0
        self.rectangle_start_y = 0
        self.rectangle_x = 0
        self.rectangle_y = 0
        self.rectangle = self.canvas.create_rectangle(
            self.rectangle_start_x,
            self.rectangle_start_y,
            self.rectangle_x,
            self.rectangle_y,
            fill='#c97d57',
            outline='#945738')

        self.canvas.bind("<Button-1>", self.get_starting_coords)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind('<ButtonRelease-1>', self.remove_rectangle)
        self.canvas.bind("<Button-3>", self.close_app)

    def get_starting_coords(self, event):
        self.rectangle_start_x, self.rectangle_start_y = event.x, event.y

    def draw_rectangle(self, event):
        self.rectangle_x = event.x
        self.rectangle_y = event.y
        self.canvas.coords(self.rectangle,
                           self.rectangle_start_x,
                           self.rectangle_start_y,
                           self.rectangle_x,
                           self.rectangle_y)

    def remove_rectangle(self, event):
        self.canvas.delete('all')
        self.canvas.update()
        self.root.withdraw()
        self.take_screenshot()

    def take_screenshot(self):
        if self.rectangle_start_x > self.rectangle_x:
            self.rectangle_x, self.rectangle_start_x = self.rectangle_start_x, \
                                                       self.rectangle_x
        if self.rectangle_start_y > self.rectangle_y:
            self.rectangle_y, self.rectangle_start_y = self.rectangle_start_y, \
                                                       self.rectangle_y

        screenshot = pyscreenshot.grab(bbox=(self.rectangle_start_x,
                                             self.rectangle_start_y,
                                             self.rectangle_x,
                                             self.rectangle_y))
        self.process_image(screenshot)

    def process_image(self, img):
        img_np = np.array(img)
        grayscale_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Screenshot', grayscale_img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        text = pytesseract.image_to_string(grayscale_img, lang='eng')
        self.translate_text(text)

    def translate_text(self, text):
        if len(text) > 0:
            translate = boto3.client(
                'translate', region_name='eu-central-1'
            )
            result = translate.translate_text(Text=text,
                                              SourceLanguageCode="en",
                                              TargetLanguageCode="pl")
            self.display_message(result.get('TranslatedText'))
        else:
            self.display_message()

    def display_message(self, message=None):
        if message:
            icons = ['face-angel', 'face-monkey', 'face-wink', 'face-glasses',
                     'face-devilish', 'face-cool', 'face-smile',
                     'face-smile-big', 'face-laugh']
            subprocess.Popen(['notify-send', 'Translation', '-i',
                              choice(icons), message])
        else:
            icons = ['face-sad', 'face-crying', 'face-embarrassed',
                     'face-uncertain', 'face-worried']
            subprocess.Popen(['notify-send', 'Oops...', '-i',
                              choice(icons), 'I couldn\'t recognize any text'])
        self.close_app()

    def close_app(self, event=None):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    app = MyApp(root)
    root.mainloop()
