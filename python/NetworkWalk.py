from Tkinter import *
from PIL import Image, ImageTk
from DatabaseConnector import DatabaseConnector
from DeepRBM import DeepRBM
import numpy as np


networkName = "treeNetwork"

dbc = DatabaseConnector();
network = dbc.getNetwork(networkName);

rbm = DeepRBM(network.model)
rbm.setWeights(network.weights)

samplesForAverage = 10;
binarize = True;

imageWidth = network.imageWidth;
imageHeight = network.imageHeight;

input = np.random.randn(samplesForAverage, network.model[0]);

flag = True;
refreshRate = 1;

def updateImage():
    global picture
    global flag
    global input
    global samplesForAverage


    input = rbm.sample(rbm.sample(input, 0, len(network.model)-1, binarize), len(network.model)-1, 0, binarize);

    main.original.putdata(np.mean(input, 0)*255)
    main.original = main.original.transpose(Image.TRANSPOSE)

    picture = ImageTk.PhotoImage(main.original)

    main.c.itemconfigure(main.myimg, image=picture)

def toggleRefresh(event):
    global refreshRate;
    if(refreshRate == 1):
        refreshRate = 1000;
    else:
        refreshRate = 1;

class NetworkWalker(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.original = Image.new("L", (imageWidth, imageHeight), "white");
        self.picture = ImageTk.PhotoImage(self.original)
        self.geometry(str(imageWidth)+"x"+str(imageHeight)+"+0+0")
        self.c = Canvas(self, width=imageWidth, height=imageHeight);
        self.c.pack()
        self.flag = True;
        self.myimg = self.c.create_image((0,0),image=self.picture, anchor="nw")#
        self.after(1, self.update_image)

    def update_image(self):
        updateImage()
        self.after(refreshRate, self.update_image)


main = NetworkWalker()
main.c.bind("<Button-1>", toggleRefresh)
main.mainloop()




# class NetworkWalker(Tk):
#     def __init__(self, *args, **kwargs):
#         Tk.__init__(self, *args, **kwargs)
#         self.geometry(str(network.imageWidth+1)+"x"+str(network.imageHeight+1))
#         self.canvas = Canvas(self,width=network.imageWidth,height=network.imageHeight)
#         self.canvas.pack()
#
#         self.
#         self.myimg = Image.new("L", (network.imageWidth, network.imageHeight), "white");
#         self.myimg.putdata(self.input);
#         self.image = ImageTk.PhotoImage(self.myimg)
#         self.imagesprite = self.canvas.create_image(10,10,image=self.image)
#
#
#         self.update_image()
#
#     def update_image(self):
#         print(self.input)
#         self.myimg = Image.new("L", (network.imageWidth, network.imageHeight), "white")
#         print(rbm.sample(self.input, 0, len(network.model)-1));
#

#
#         self.myimg.putdata(neuronWeights*255)
#         self.myimg = self.myimg.transpose(Image.TRANSPOSE)
#
#         self.image = ImageTk.PhotoImage(self.myimg)
#         self.canvas.itemconfigure(self.imagesprite, image=self.image)
#
#         # call this function again in one second
#         self.after(1000, self.update_image)
#
#         print("looping: "+str(self.input))
#
#
# app = NetworkWalker()
# app.mainloop()