from Tkinter import *
from PIL import ImageTk, Image
from DatabaseConnector import DatabaseConnector
from DeepRBM import DeepRBM
import numpy as np

networkName = "testNetwork"
layerToObserve = 3;

canvasWidth = 1400;
canvasHeight = 1000;

dbc = DatabaseConnector();
network = dbc.getNetwork(networkName);

rbm = DeepRBM(network.model)
rbm.setWeights(network.weights)

root = Tk()
root.geometry(str(canvasWidth)+'x'+str(canvasHeight))
canvas = Canvas(root,width=canvasWidth-1,height=canvasHeight-1)
canvas.pack()

references = []

for i in range(network.model[layerToObserve]):
    myimg = Image.new("L", (network.imageWidth, network.imageHeight), "white")

    input = np.zeros(network.model[layerToObserve])
    input[i] = 1

    neuronWeights = rbm.sample(input, layerToObserve, 0, False);

    myimg.putdata(neuronWeights*255)

    imagesPerLine = canvasWidth/network.imageWidth - 2;

    image = ImageTk.PhotoImage(myimg)
    imagesprite = canvas.create_image(
        20+(network.imageWidth+2)*(i%imagesPerLine),
        20+(network.imageHeight+2)*(i/imagesPerLine),
        image=image)

    references.append(image)
    references.append(imagesprite)

root.mainloop()