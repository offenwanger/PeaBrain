import numpy as np
from DeepRBM import *
import time

def trainRBMs(rbm, cases, batchSize, numberItterations, learningRate =0.5, momentumMultiplier = 0.9, LD1=0):
    for layer in range(len(rbm.weights)):
        momentumSpeed = np.zeros(rbm.weights[layer].shape);
        batchIndex = 0;
        i=0;

        notificationMarker = 100
        timeMarker = time.time();

        while (i < numberItterations):
            miniBatch = rbm.sample(getMiniBatch(cases, batchIndex, batchSize), 0, layer)
            batchIndex += batchSize
            if(batchIndex > cases.shape[0]):
                batchIndex -= cases.shape[0]

            gradient = cd1(rbm.weights[layer], miniBatch);
            if(LD1 != 0):
                gradient = gradient + LD1*getLD1Penalty(rbm.weights[layer])
            momentumSpeed = momentumMultiplier * momentumSpeed + gradient;
            rbm.weights[layer] = rbm.weights[layer] + momentumSpeed * learningRate;
            i += 1
            if(i == notificationMarker):
                print "Trained for "+str(i)+" itterations, time taken = "+str(time.time() - timeMarker)+"s";
                timeMarker = time.time()
                notificationMarker += 100;

        print "Finished Training From Layer "+str(layer)
    return rbm


def getMiniBatch(cases, start, size):
    #3 cases, 5 units in each

    #      1 2 3 4 5
    #    1 o o o o o
    #    2 o o o o o
    #    3 o o o o o

    if(size > cases.shape[0]):
        return cases;
    if(start + size < cases.shape[0]):
        return cases[start:start+size,:]

    return np.concatenate((cases[start:,:], cases[:start+size-cases.shape[0]]), axis=0)

def getLD1Penalty(weights):
   #weights -> matrix with 1 for negative numbers and 0 for positive
   #*2, now is mat with 2 for negative numbers,
   #-1, now 1 for negative and -1 for positive.
   return (weights < 0).astype(float)*2 - 1;


# function model = optimize(model_shape, training_data, learning_rate, n_iterations)
# % This trains a model that's defined by a single matrix of weights.
# % <model_shape> is the shape of the array of weights.
# % <gradient_function> is a function that takes parameters <model> and <data> and returns the gradient (or approximate gradient in the case of CD-1) of the function that we're maximizing. Note the contrast with the loss function that we saw in PA3, which we were minimizing. The returned gradient is an array of the same shape as the provided <model> parameter.
# % This uses mini-batches of size 100, momentum of 0.9, no weight decay, and no early stopping.
# % This returns the matrix of weights of the trained model.
#     model = (a4_rand(model_shape, prod(model_shape)) * 2 - 1) * 0.1;
#     momentum_speed = zeros(model_shape);
#     mini_batch_size = 100;
#     start_of_next_mini_batch = 1;
#     for iteration_number = 1:n_iterations,
#         mini_batch = extract_mini_batch(training_data, start_of_next_mini_batch, mini_batch_size);
#         start_of_next_mini_batch = mod(start_of_next_mini_batch + mini_batch_size, size(training_data.inputs, 2));
#         gradient = cd1(model, mini_batch);
#         momentum_speed = 0.9 * momentum_speed + gradient;
#         model = model + momentum_speed * learning_rate;
#     end
# end


