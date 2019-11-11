import tkinter as tk
import keyboard


class MyApp:
    def __init__(self, parent):
        self.root = parent
        self.window_height = self.root.winfo_screenheight()
        self.window_width = self.root.winfo_screenwidth()
        self.root.overrideredirect(True)
        self.root.wait_visibility()
        self.root.geometry(
            f'{self.window_width}x{self.window_height}+0+0')
        self.root.wm_attributes('-alpha', 0.1)
        self.root.wm_title('Area picker')
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
            fill='yellow')

        self.canvas.bind("<Button-1>", self.get_starting_coords)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind('<ButtonRelease-1>', self.remove_rectangle)
        self.canvas.bind("<Button-3>", self.cancel_screenshot)
        keyboard.add_hotkey('pause', self.take_screenshot)
        keyboard.add_hotkey('escape', self.cancel_screenshot)
        keyboard.add_hotkey('ctrl+escape', self.close_app)

    def get_starting_coords(self, event):
        self.rectangle_start_x, self.rectangle_start_y = event.x, event.y

    def draw_rectangle(self, event):
        self.rectangle_x = event.x
        self.rectangle_y = event.y
        self.canvas.coords(self.rectangle,
                           self.rectangle_start_x,
                           self.rectangle_start_y,
                           self.rectangle_x,
                           self.rectangle_y,)

    def remove_rectangle(self, event):
        print('Removing rectangle')
        self.canvas.coords(self.rectangle, 0, 0, 0, 0)

    def take_screenshot(self):
        self.root.update()
        self.root.deiconify()

    def cancel_screenshot(self, event=None):
        self.root.update()
        self.root.withdraw()

    def close_app(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    app = MyApp(root)
    root.mainloop()
