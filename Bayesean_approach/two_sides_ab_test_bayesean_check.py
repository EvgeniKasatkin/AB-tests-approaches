#from matplotlib import use
#import pylab
from scipy.stats import beta, norm, uniform
import random
import numpy as np
import os



class BayesianExpectedError:
    def __init__(self, prior_params, samples_list, conversions_list):
        self.prior_params = prior_params
        self.samples_list = samples_list
        self.conversions_list = conversions_list

    def posterior_distributions(self):
        posterios = []
        length_of_prior_params = len(self.prior_params)
        for ind_ in range(length_of_prior_params):
            posterios.append(beta(self.prior_params[ind_][0] + self.conversions_list[ind_] - 1, self.prior_params[ind_][1] + self.samples_list[ind_] - self.conversions_list[ind_] - 1))
        return posterios


if __name__ == '__main__':
    prior_params = [(1,1), (1,1)]
    #Params of beta distributions B(1,1) for test and control group identicaly equal U(0,1)
    threshold = 0.01
    #Example of threshold
    xgrid_size = 1024
    #XGRID

    print("Input number of samples in Group A:")
    samples_a = input()
    print("Input number of samples in Group B:")
    samples_b = input()

    print("Input number of conversions in Group A:")
    conversions_a = input()
    print("Input number of conversions in Group B:")
    conversions_b = input()

    samples_list = np.array([int(samples_a), int(samples_b)])
    conversions_list = np.array([int(conversions_a), int(conversions_b)])

    posterios_distributions = BayesianExpectedError(prior_params, samples_list, conversions_list).posterior_distributions()

    x = np.mgrid[0:xgrid_size, 0:xgrid_size] / float(xgrid_size)
    pdf_arr = posterios_distributions[0].pdf(x[1]) * posterios_distributions[1].pdf(x[0])
    pdf_arr /= pdf_arr.sum()  # normalization

    prob_error = np.zeros(shape=x[0].shape)

    if (conversions_list[1] / float(samples_list[1])) > (conversions_list[0] / float(samples_list[0])):
        prob_error[np.where(x[1] > x[0])] = 1.0
    else:
        prob_error[np.where(x[0] > x[1])] = 1.0

    expected_error = np.maximum(abs(x[0] - x[1]), 0.0)

    expected_err_scalar = (expected_error * prob_error * pdf_arr).sum()

    if (expected_err_scalar < threshold):
        if (conversions_list[1] / float(samples_list[1])) > (conversions_list[0] / float(samples_list[0])):
            print("Probability that version B is larger. Mistake probably is: " + str((prob_error*pdf_arr).sum()))
            print("Expected error is " + str(expected_err_scalar))
        else:
            print("Probability that version A is larger. Mistake probably is: " + str((prob_error*pdf_arr).sum()))
            print("Expected error is " + str(expected_err_scalar))
    else:
        print("Probability that version B is larger is " + str((prob_error*pdf_arr).sum()))
        print("Continue test. Expected error was " + str(expected_err_scalar) + " > " + str(threshold))

