import numpy as np;

#Holds the weights

# o o o o o o o o o
#/\/\/\/\//\\/\//\\
#o o  o o o o o o o
# \/  \/\/\/\/\/\/
#  o o o o o o o

#Need to be able to update all the weights based on a gradient

class DeepRBM:
    def __init__(self, model):
        #randomly initializa the model
        self.weights = []
        for i, count in enumerate(model):
            if i+1 < len(model):
                self.weights.append(np.random.randn(model[i],model[i+1]))
        self.model = model

    #Takes the input layer then samples adjacent layers from the input to the output layer
    def sample(self, input, layerIn, layerOut):
        while(layerIn != layerOut):
            if(layerIn<layerOut):
                #TODO randomly 1 or 0 based on input expit(input.dot(weights))
                input = expit(input.dot(self.weights[layerIn]))
                layerIn = layerIn + 1
            if(layerIn > layerOut):
                layerIn = layerIn - 1
                input = expit(input.dot(self.weights[layerIn].transpose()))
        return input

        print "unimplemented method called" % self.model

    # sets a weights from the given layer, from the given neuron,
    # to a given neuron in the next layer
    def setWeight(self, fromLayer, fromNeuron, toNeuron, value):
        self.weights[fromLayer][fromNeuron][toNeuron] = value;
        return;

    # weights is a python array of numpy 2d arrays
    def sumAllWeights(self, weights):
        for i, count in enumerate(self.weights):
            self.weights[i] = self.weights[i] + weights[i];

    # weights is a numpy 2d array of weights
    def sumWeights(self, weights, fromLayer):
        self.weights[fromLayer] = self.weights[fromLayer] + weights;



# function visible_probability = hidden_state_to_visible_probabilities(rbm_w, hidden_state)
# % <rbm_w> is a matrix of size <number of hidden units> by <number of visible units>
# % <hidden_state> is a binary matrix of size <number of hidden units> by <number
# %   of configurations that we're handling in parallel>.
# % The returned value is a matrix of size <number of visible units> by <number
# %  of configurations that we're handling in parallel>.
# % This takes in the (binary) states of the hidden units, and returns the
# %  activation probabilities of the visible units, conditional on those states.
#
#
#   %p(h=1)=logistic(sum(vw))
#   %rbm_w  num vis
#   %       [* * *]
#   %num hid[* * *]
#
#   % hidden_state
#   %       num cases
#   %       [* * * *]
#   %num hid[* * * *]
#
#
#   % visible_probability
#   %       num cases
#   %       [* * * *]
#   %num vis[* * * *]
#   %       [* * * *]
#
#   visible_probability = logistic(rbm_w.' * hidden_state);
#
# end

blah = DeepRBM([5, 2, 3])

print(blah.weights)
print(blah.weights[0])

#Logistic funtion
from scipy.special import expit
print "expit"
print expit(blah.weights[0])

print "dot prod"
print(blah.weights[0].dot([1, 1]))

print "mat mult"
print(blah.weights[0].dot(blah.weights[1]))

print "Set weight"
blur = DeepRBM([2, 2, 2])
print(blur.weights)
blur.setWeight(0, 0, 0, 0.5)
blur.setWeight(0, 0, 1, 0.25)
blur.setWeight(0, 1, 0, 0.5)
blur.setWeight(0, 1, 1, 0.25)
blur.setWeight(1, 0, 0, 0.5)
blur.setWeight(1, 0, 1, 0.25)
blur.setWeight(1, 1, 0, 0.5)
blur.setWeight(1, 1, 1, 0.25)
print(blur.weights)

print "sampling"
print(blur.sample(np.array([0.5, 0.5]), 0, 2))
print(blur.sample(blur.sample(np.array([0.5, 0.5]), 0, 2), 2, 0))

print "summing weights"
blar = DeepRBM([2, 2, 2])
bler = DeepRBM([2, 2, 2])

print bler.weights
print blar.weights

bler.sumAllWeights(blar.weights)

print bler.weights

bler.sumWeights(np.array([[1,1],[1,1]]),1)

print bler.weights




def cd1(weights, data):
    return
# function ret = cd1(rbm_w, visible_data)
# % <rbm_w> is a matrix of size <number of hidden units> by <number of visible units>
# % <visible_data> is a (possibly but not necessarily binary) matrix of size <number
# %   of visible units> by <number of data cases>
# % The returned value is the gradient approximation produced by CD-1. It's of the
# %  same shape as <rbm_w>.
#
#     visible_data = sample_bernoulli(visible_data);
#
#     hidden_state_0 = sample_bernoulli(visible_state_to_hidden_probabilities(rbm_w, visible_data));
#     grad_data = configuration_goodness_gradient(visible_data, hidden_state_0);
#
#     visible_state_1 = sample_bernoulli(hidden_state_to_visible_probabilities(rbm_w, hidden_state_0));
#     %hidden_state_1 = sample_bernoulli(visible_state_to_hidden_probabilities(rbm_w, visible_state_1));
#     hidden_state_1 = visible_state_to_hidden_probabilities(rbm_w, visible_state_1);
#     grad_model = configuration_goodness_gradient(visible_state_1, hidden_state_1);
#
#     ret = grad_data - grad_model;
#
# end

def configurationGoodness(weights, intput, output):
    return
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




def configurationGoodnessGradient(input, output):
    return
# function d_G_by_rbm_w = configuration_goodness_gradient(visible_state, hidden_state)
# % <visible_state> is a binary matrix of size <number of visible units> by
# %   <number of configurations that we're handling in parallel>.
# % <hidden_state> is a (possibly but not necessarily binary) matrix of size
# %   <number of hidden units> by <number of configurations that we're handling
# %   in parallel>.
# % You don't need the model parameters for this computation.
# % This returns the gradient of the mean configuration goodness (negative energy,
# %   as computed by function <configuration_goodness>) with respect to the model
# %   parameters. Thus, the returned value is of the same shape as the model
# %   parameters, which by the way are not provided to this function. Notice that
# %   we're talking about the mean over data cases (as opposed to the sum over
# %   data cases).
#
#   % hidden_state
#   %       num cases
#   %       [* * * *]
#   %num hid[* * * *]
#
#
#   % visible_state
#   %       num cases
#   %       [* * * *]
#   %num vis[* * * *]
#   %       [* * * *]
#
#   %d_G_by_rbm_w
#   %       num vis
#   %       [* * *]
#   %num hid[* * *]
#
#   num_cases = size(hidden_state, 2);
#
#   d_G_by_rbm_w = (hidden_state * (visible_state.')) ./ num_cases;
#
# end
