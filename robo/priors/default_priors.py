'''
Created on Oct 14, 2015

@author: Aaron Klein
'''
import numpy as np
import scipy.stats as sps

from robo.priors.base_prior import BasePrior


class TophatPrior(BasePrior):

    def __init__(self, l_bound, u_bound):
        """
        Tophat prior as it used in the original spearmint code.

        Parameters
        ----------
        l_bound : float
            Lower bound of the prior. Note the log scale.
	u_bound : float
            Upper bound of the prior. Note the log scale.


	"""
        self.min = l_bound
        self.max = u_bound
        if not (self.max > self.min):
            raise Exception("Upper bound of Tophat prior must be greater \
            than the lower bound!")

    def lnprob(self, theta):
        """
        Returns the log probability of theta. Note: theta should
        be on a log scale.

        Parameters
        ----------
        theta : (D,) numpy array
            A hyperparameter configuration in log space.

        Returns
        -------
        float
            The log probabilty of theta
        """
    
        if np.any(theta < self.min) or np.any(theta > self.max):
            return -np.inf
        else:
            return 0

    def sample_from_prior(self, n_samples):
        """
        Returns N samples from the prior.

        Parameters
        ----------
        n_samples : int
            The number of samples that will be drawn.

        Returns
        -------
        (N, D) np.array
            The samples from the prior.
        """
 
	p0 = self.min + np.random.rand(n_samples) * (self.max - self.min)
        return p0[:, np.newaxis]

    def gradient(self, theta):
        """
        Computes the gradient of the prior with
        respect to theta.

        Parameters
        ----------
        theta : (D,) numpy array
            Hyperparameter configuration in log space

        Returns
        -------
        (D) np.array

            The gradient of the prior at theta.
        """ 
	if np.any(theta < self.min) or np.any(theta > self.max):
            return -np.inf
        else:
            return 0

class HorseshoePrior(BasePrior):

    def __init__(self, scale=0.1):
	"""
        Horseshoe Prior as it is used in spearmint

	Parameters
        ----------
        scale: float
            Scaling parameter. See below how it is influenced
	    the distribution.
	"""
        self.scale = scale

    def lnprob(self, theta):
        """
        Returns the log probability of theta. Note: theta should
        be on a log scale.

        Parameters
        ----------
        theta : (D,) numpy array
            A hyperparameter configuration in log space.

        Returns
        -------
        float
            The log probabilty of theta
        """
	# We computed it exactly as in the original spearmint code
	if np.any(theta == 0.0):
            return np.inf
        return np.log(np.log(1 + 3.0 * (self.scale / np.exp(theta)) ** 2))

    def sample_from_prior(self, n_samples):
        """
        Returns N samples from the prior.

        Parameters
        ----------
        n_samples : int
            The number of samples that will be drawn.

        Returns
        -------
        (N, D) np.array
            The samples from the prior.
        """
 
        lamda = np.abs(np.random.standard_cauchy(size=n_samples))

        p0 = np.log(np.abs(np.random.randn() * lamda * self.scale))
        return p0[:, np.newaxis]

    def gradient(self, theta):
        """
        Computes the gradient of the prior with
        respect to theta.

        Parameters
        ----------
        theta : (D,) numpy array
            Hyperparameter configuration in log space

        Returns
        -------
        (D) np.array
            The gradient of the prior at theta.
        """ 
	pass


class LognormalPrior(BasePrior):
    def __init__(self, sigma, mean=0):
	"""
        Log normal prior

	Parameters
        ----------
        sigma: float
            Specifies the standard deviation of the normal
	    distribution.
	mean: float
	    Specifies the mean of the normal distribution
	"""
 
	self.sigma = sigma
        self.mean = mean

    def lnprob(self, theta):
        """
        Returns the log probability of theta. Note: theta should
        be on a log scale.

        Parameters
        ----------
        theta : (D,) numpy array
            A hyperparameter configuration in log space.

        Returns
        -------
        float
            The log probabilty of theta
        """
 
	return sps.lognorm.logpdf(theta, self.sigma, loc=self.mean)

    def sample_from_prior(self, n_samples):
        """
        Returns N samples from the prior.

        Parameters
        ----------
        n_samples : int
            The number of samples that will be drawn.

        Returns
        -------
        (N, D) np.array
            The samples from the prior.
        """
    
        p0 = np.random.lognormal(mean=self.mean,
                                   sigma=self.sigma,
                                   size=n_samples)
        return p0[:, np.newaxis]

    def gradient(self, theta):
        """
        Computes the gradient of the prior with
        respect to theta.

        Parameters
        ----------
        theta : (D,) numpy array
            Hyperparameter configuration in log space

        Returns
        -------
        (D) np.array
            The gradient of the prior at theta.
        """ 
	pass