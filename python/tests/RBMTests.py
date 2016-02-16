import unittest
import numpy as np

from DeepRBM import *

class TestStringMethods(unittest.TestCase):

    def test_constructor(self):
        drbm = DeepRBM([5, 2, 3])
        self.assertEqual(len(drbm.weights), 2)
        self.assertEqual(drbm.weights[0].shape[0], 2)
        self.assertEqual(drbm.weights[0].shape[1], 5)
        self.assertEqual(drbm.weights[1].shape[0], 3)
        self.assertEqual(drbm.weights[1].shape[1], 2)


    def test_passForward(self):
        result = passForward(np.array([[1,1,1,1,1],[0,0,0,0,0]]), np.array([[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1]]), False)
        #should be 3 cases
        self.assertEqual(result.shape[0], 3)
        #should be 2 units
        self.assertEqual(result.shape[1], 2)
        self.assertAlmostEqual(result[0,0], 0.993307149, 5)
        self.assertAlmostEqual(result[0,1], 0.5, 5)
        self.assertAlmostEqual(result[1,0], 0.993307149, 5)
        self.assertAlmostEqual(result[1,1], 0.5, 5)
        self.assertAlmostEqual(result[2,0], 0.993307149, 5)
        self.assertAlmostEqual(result[2,1], 0.5, 5)

    def test_binarize(self):
        testdata = np.zeros((10000, 1000))
        testdata = binarize(testdata)
        self.assertEqual(np.mean(testdata), 0)

        testdata.fill(0.3)
        testdata = binarize(testdata)
        self.assertAlmostEqual(np.mean(testdata), 0.3, 2)

    def test_setWeights(self):
        rbm = DeepRBM([2, 3, 1])
        #wrong should throw error
        with self.assertRaises(ValueError):
            rbm.setWeights([np.array([0,0,0],[0,0,0]), np.array([0,0,0])])

        rbm.setWeights([np.array([0,0,0],[0,0,0]), np.array([0,0,0]).reshape((1, 3))])

    def test_setWeights(self):
        rbm = DeepRBM([2, 3, 1])
        with self.assertRaises(ValueError):
            rbm.setWeights([np.array([[0,0],[0,0],[0,0]]), np.array([[0],[0],[0]])])

        rbm.setWeights([np.array([[0,0],[0,0],[0,0]]), np.matrix([0,0,0])])

    def test_sample(self):
        rbm = DeepRBM([2, 3, 1])

        rbm.setWeights([np.array([[1,1],[1,1],[1,1]]), np.matrix([1,1,1])])

        result = rbm.sample(np.array([0,0]), 0, 2, False)
        self.assertAlmostEqual(result[0], 0.8175745, 4)

        result = rbm.sample(np.array([[0,0],[1,1],[0,1]]), 0, 2, False)
        self.assertAlmostEqual(result[0], 0.8175745, 4)
        self.assertAlmostEqual(result[1], 0.933540476818325, 4)
        self.assertAlmostEqual(result[2], 0.8996350, 4)


        result = rbm.sample(np.array([0]), 2, 0, False)
        self.assertAlmostEqual(result[0,0], 0.8175745, 4)
        self.assertAlmostEqual(result[0,1], 0.8175745, 4)




if __name__ == '__main__':
    unittest.main()