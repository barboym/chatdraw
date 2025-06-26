import tkinter as tk

from sys import platform
if platform == "linux" or platform == "linux2":
    # For Linux, we use pyscreenshot as PIL's ImageGrab may not work properly
    import pyscreenshot as ImageGrab
else:
    # For Windows and macOS, we can use PIL's ImageGrab
    from PIL import ImageGrab

def save_canvas(widget, filename="/tmp/drawing.png",verbose=False):
    x = widget.winfo_rootx()
    y = widget.winfo_rooty()
    w = widget.winfo_width()
    h = widget.winfo_height()
    ImageGrab.grab((x, y, x + w, y + h)).save(filename)
    if verbose:
        print(f"Saved to {filename}")

def draw():
    root = tk.Tk()
    root.title("Draw something and close the window to save")

    canvas = tk.Canvas(root, width=500, height=500, bg='white')
    canvas.pack()

    def paint(event):
        x1, y1 = (event.x - 3), (event.y - 3)
        x2, y2 = (event.x + 3), (event.y + 3)
        canvas.create_oval(x1, y1, x2, y2, fill="black")

    canvas.bind("<B1-Motion>", paint)
    
    def on_close():
        save_canvas(canvas)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    draw()
