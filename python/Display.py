from Tkinter import *
from PIL import ImageTk, Image
from DatabaseConnector import DatabaseConnector
from DeepRBM import DeepRBM
import numpy as np

networkName = "testNetwork"
layerToObserve = 2;

def run():
    # root = Tk()
    # root.geometry('1000x1000')
    # canvas = Canvas(root,width=999,height=999)
    # canvas.pack()
    # pilImage = Image.open("ball.gif")
    # image = ImageTk.PhotoImage(pilImage)
    # imagesprite = canvas.create_image(400,400,image=image)
    # root.mainloop()

    image_manip().mainloop()


class image_manip(Tk):

    def __init__(self):
        Tk.__init__(self)

        dbc = DatabaseConnector();
        network = dbc.getNetwork(networkName);

        rbm = DeepRBM(network.model)
        rbm.setWeights(network.weights)

        myimg =  Image.new("L", (network.imageWidth, network.imageHeight), "white")

        input = np.zeros(network.model[1])
        input[22] = 1
        neuronWeights = rbm.sample(input, 3, 0, False);

        myimg.putdata(neuronWeights*254)

        self.configure(bg='red')

        self.ImbImage = Canvas(self, highlightthickness=0, bd=0, bg='blue')
        self.ImbImage.pack()

        self.i = ImageTk.PhotoImage(myimg)
        self.ImbImage.create_image(40, 40, image=self.i)

#########################################################################
        # self.configure(bg='red')
        # self.ImbImage = Canvas(self, highlightthickness=0, bd=0, bg='blue')
        # self.ImbImage.pack()
        #
        # for i in range(network.model[layerToObserve]):
        #     myimg = Image.new("L", (network.imageWidth, network.imageHeight), "white")
        #
        #     input = np.zeros(network.model[layerToObserve])
        #     input[i] = 1
        #     neuronWeights = rbm.sample(input, 3, 0, False);
        #
        #     myimg.putdata(neuronWeights*255)
        #
        #     self.i = ImageTk.PhotoImage(myimg)
        #     self.ImbImage.create_image(40*(i%20), 40*(i/20), image=self.i)
        #     print 40*(i%20)
        #     print 40*(i/20)
###########################################################################


if __name__ == "__main__":
    run()