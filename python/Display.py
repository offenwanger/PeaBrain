from Tkinter import *
from PIL import ImageTk, Image
from DatabaseConnector import DatabaseConnector
from DeepRBM import DeepRBM
import numpy as np

# networkName = "testNetwork"
# networkName = "faceNetworkNoLD"
networkName = "treeNetwork"
# networkName = "cupNetwork"
# networkName = "cupNetworkSmall"
# networkName = "treeNetworkSmall"



layerToObserve = 1;

binarize = False
samplesForAverage = 1

canvasWidth = 900;
canvasHeight = 600;

dbc = DatabaseConnector();
network = dbc.getNetwork(networkName);

rbm = DeepRBM(network.model)
rbm.setWeights(network.weights)

root = Tk()
root.geometry(str(canvasWidth)+'x'+str(canvasHeight))
canvas = Canvas(root,width=canvasWidth,height=canvasHeight)
canvas.pack()

references = []

for i in range(network.model[layerToObserve]):
    print "Sampling neuron "+str(i)

    myimg = Image.new("L", (network.imageWidth, network.imageHeight), "white")

    if(samplesForAverage <= 1):
        input = np.zeros(network.model[layerToObserve])
        input[i] = 1

    if(samplesForAverage > 1):
        input = np.zeros((samplesForAverage, network.model[layerToObserve]))
        input[:,i] = np.ones(samplesForAverage)

    neuronWeights = rbm.sample(input, layerToObserve, 0, binarize);

    if(samplesForAverage > 1):
        neuronWeights = np.mean(neuronWeights, 0)


    myimg.putdata(neuronWeights*255)
    myimg = myimg.transpose(Image.TRANSPOSE)

    imagesPerLine = canvasWidth/network.imageWidth - 2;

    image = ImageTk.PhotoImage(myimg)
    imagesprite = canvas.create_image(
        20+(network.imageWidth+2)*(i%imagesPerLine),
        20+(network.imageHeight+2)*(i/imagesPerLine),
        image=image)

    references.append(image)
    references.append(imagesprite)

root.mainloop()