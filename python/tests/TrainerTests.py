import unittest
import numpy as np

from Trainer import *

class TestStringMethods(unittest.TestCase):

    def test_getMiniBatch(self):
        batch = getMiniBatch(np.array([[1,1,1,1],[2,2,2,2],[3,1,1,1],[4,1,1,1],[5,1,1,1]]),1,3)
        self.assertEqual(batch.shape[0], 3)
        self.assertEqual(batch[0,0], 2)
        self.assertEqual(batch[2,0], 4)

        batch = getMiniBatch(np.array([[1,1,1,1],[2,2,2,2],[3,1,1,1],[4,1,1,1],[5,1,1,1]]),3,4)
        self.assertEqual(batch.shape[0], 4)
        self.assertEqual(batch[0,0], 4)
        self.assertEqual(batch[2,0], 1)
        self.assertEqual(batch[3,0], 2)

    def test_trainRBM(self):
        rbm = DeepRBM([2, 2, 2])
        cases = np.array([[1, 1],[1, 1],[1, 1],[1, 1],[1, 1],[1, 1],[1, 1],[1, 1],[1, 1],[1, 1]])
        rbm = trainRBMs(rbm,cases,4,1000)

        print(rbm.weights)

        self.assertAlmostEqual(rbm.sample(rbm.sample(np.array([1,1]), 0, 2, False), 2, 0, False)[0], 1, 4)

    def test_LD1(self):
        rbm = np.ones((2, 3));
        rbm[:,2] = [-1,-1];
        penalty = getLD1Penalty(rbm);
        self.assertEqual(-1, penalty[0,0])
        self.assertEqual(-1, penalty[1,0])
        self.assertEqual(-1, penalty[0,1])
        self.assertEqual(-1, penalty[1,1])
        self.assertEqual(1, penalty[0,2])
        self.assertEqual(1, penalty[1,2])



if __name__ == '__main__':
    unittest.main()