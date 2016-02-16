import Tkinter
from PIL import ImageTk, Image


class image_manip(Tkinter.Tk):

    def __init__(self):
        Tkinter.Tk.__init__(self)

        self.configure(bg='red')

        self.ImbImage = Tkinter.Canvas(self, highlightthickness=0, bd=0, bg='blue')
        self.ImbImage.pack()

        self.i = ImageTk.PhotoImage(Image.new("L", (40, 40), "white"))
        self.ImbImage.create_image(150, 100, image=self.i)


def run():
    image_manip().mainloop()
if __name__ == "__main__":
    run()