import numpy as np
from scipy.special import expit

#Holds the weights

# o o o o o o o o o
#/\/\/\/\//\\/\//\\
#o o  o o o o o o o
# \/  \/\/\/\/\/\/
#  o o o o o o o

#Need to be able to update all the weights based on a gradient

#----------- PROGRAM CONVENTIONS --------------
#Weight matricies are always <num units in output> by <num units in input>
# o o o o    layer 0 = 4
#/\/\/\/\
#o  o  o     layer 1 = 3
#weight matrix 0 to 1 is 4x3, so 4 rows 3 cols

#input matrices are always <num of cases> by <num of units>
#case 1: [0,0,0,1,0]
#case 2: [0,1,1,1,0]
#case 3: [0,1,0,1,1]
# matrix would be 3x5, and look exactly like that

class DeepRBM:
    def __init__(self, model):
        #randomly initializa the model
        self.weights = []
        for i, count in enumerate(model):
            if i+1 < len(model):
                #set up weight matrices, <output> by <input>
                self.weights.append(np.random.randn(model[i+1],model[i]))
        self.model = model

    #Takes the input layer then samples adjacent layers from the input to the output layer
    def sample(self, input, layerIn, layerOut, bin = True):
        while(layerIn != layerOut):
            if(layerIn<layerOut):
                input = passForward(self.weights[layerIn], input, bin)
                layerIn = layerIn + 1
            if(layerIn > layerOut):
                layerIn = layerIn - 1
                input = passForward(self.weights[layerIn].transpose(), input, bin)

        return input

    # sets a weights from the given layer, from the given neuron,
    # to a given neuron in the next layer
    def setWeight(self, fromLayer, fromNeuron, toNeuron, value):
        self.weights[fromLayer][fromNeuron][toNeuron] = value;

    def setWeights(self, weights):
        if (len(weights) != len(self.weights)):
            raise ValueError('Weights incorrect shape');

        for index in range(len(weights)):
            if(self.weights[index].shape != weights[index].shape):
                raise ValueError('Weights incorrect shape, '+str(weights[index].shape)+"!="+str(self.weights[index].shape))

        self.weights = weights;

    # weights is a python array of numpy 2d arrays
    def addToAllWeights(self, weights):
        for i, count in enumerate(self.weights):
            self.weights[i] = self.weights[i] + weights[i];

    # weights is a numpy 2d array of weights
    def addToWeights(self, weights, fromLayer):
        self.weights[fromLayer] = self.weights[fromLayer] + weights;


#input single dimentional array
def binarize(input):
    return (input > np.random.uniform(size = input.shape)).astype(float)

#inputs is <num cases> by <size input>
#takes an array of weights <outputs> by <inputs>
def passForward(weights, input, bin = True):
    input = expit(input.dot(weights.transpose()))
    if(bin):
        input = binarize(input)
    return input


#input is assumed to be an array of floats with value 1 or 0 binary
#inputs is <num of cases> by <size of input>
#weights is <size of next layer> by <size of input>
def cd1(weights, input):
    units_j_0 = passForward(weights, input)
    units_i_1 = passForward(weights.transpose(), units_j_0)
    units_j_1 = passForward(weights, units_i_1)

    grad_data = configurationGoodnessGradient(input, units_j_0)
    grad_model = configurationGoodnessGradient(units_i_1, units_j_1)

    return grad_data - grad_model


#input is <number of cases> by <number units layer i> output is <number of cases> by <number of units layer j>
#return value is <output (layer j)> by <input (layer i)>, same as weight matrices
def configurationGoodnessGradient(input, output):
    cases = input.shape[1]
    return output.transpose().dot(input)/cases


# #Logistic funtion
#
# print "expit"
# print expit(blah.weights[0])
#
# print "dot prod"
# print(blah.weights[0].dot([1, 1]))
#
# print "mat mult"
# print(blah.weights[0].dot(blah.weights[1]))
#
# print "Set weight"
# blur = DeepRBM([2, 2, 2])
# print(blur.weights)
# blur.setWeight(0, 0, 0, 0.5)
# blur.setWeight(0, 0, 1, 0.25)
# blur.setWeight(0, 1, 0, 0.5)
# blur.setWeight(0, 1, 1, 0.25)
# blur.setWeight(1, 0, 0, 0.5)
# blur.setWeight(1, 0, 1, 0.25)
# blur.setWeight(1, 1, 0, 0.5)
# blur.setWeight(1, 1, 1, 0.25)
# print(blur.weights)
#
# print "sampling"
# print(blur.sample(np.array([0.5, 0.5]), 0, 2))
# print(blur.sample(blur.sample(np.array([0.5, 0.5]), 0, 2), 2, 0))
#
# print "summing weights"
# blar = DeepRBM([2, 2, 2])
# bler = DeepRBM([2, 2, 2])
# print bler.weights
# print blar.weights
#
# print "Add to all"
# bler.addToAllWeights(blar.weights)
# print bler.weights
#
# print "Add single set"
# bler.addToWeights(np.array([[1,1],[1,1]]),1)
# print bler.weights
#
# print "Binarize"
# print binarize(np.array([0.5, 0.1, 0.9]))
#
# print "Pass forward"
# print passForward(np.array([[1, 1],[0,0],[0,1]]), np.array([[1, 1, 1, 1],[1,-2, 3, -4]]), bin = False)
#
# print "config goodness gradient"
# print configurationGoodnessGradient(np.array([[1.0, 1.0],[1.0,0.0]]), np.array([[1.0, 0.0, 1.0],[0.0,1.0, 1.0]]))
# print(np.array([[1.0, 0.0, 1.0],[0.0,1.0, 1.0]]).shape)




#---------------------------------------------------------
#may not need this
#def configurationGoodness(weights, intput, output):
#    return

# function G = configuration_goodness(rbm_w, visible_state, hidden_state)
# % <rbm_w> is a matrix of size <number of hidden units> by <number of visible units>
# % <visible_state> is a binary matrix of size <number of visible units> by <number
# %   of configurations that we're handling in parallel>.
# % <hidden_state> is a binary matrix of size <number of hidden units> by <number
# %   of configurations that we're handling in parallel>.
# % This returns a scalar: the mean over cases of the goodness (negative energy)
# %   of the described configurations.
#
#   % hidden_state
#   %       num cases
#   %       [h1c1 h1c2 h1c3 h1c4]
#   %num hid[h2c1 h2c2 h2c3 h2c4]
#
#   %rbm_w  num vis
#   %       [wh1v1 wh1v2 wh1v3]
#   %num hid[wh2v1 wh2v2 wh2v3]
#
#   % visible_state
#   %       num cases
#   %       [v1c1 v1c2 v1c3 v1c4]
#   %num vis[v2c1 v2c2 v2c3 v2c4]
#   %       [v3c1 v3c2 v3c3 v3c4]
#
#   G = mean(sum(hidden_state .* (rbm_w * visible_state), 1));
#
# end
