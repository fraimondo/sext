import numpy as np

from rpy2.robjects.packages import importr
import rpy2.robjects as ro


def ttestBF(group1, group2):
    bf = importr('BayesFactor')
    fact = bf.ttestBF(x=ro.FloatVector(group1), y=ro.FloatVector(group2))
    return bf.extractBF(fact)[0][0]


def best(group1, group2):
    import pymc as pm
    group1 = np.random.normal(15, 2, 100)
    group2 = np.random.normal(15.3, 2, 100)

    # Generate Pooled Data
    pooled = np.concatenate((group1, group2))

    mu1 = pm.Normal("mu_1", mu=pooled.mean(), tau=1.0 / pooled.var() / 1000.0)
    mu2 = pm.Normal("mu_2", mu=pooled.mean(), tau=1.0 / pooled.var() / 1000.0)

    sig1 = pm.Uniform("sigma_1", lower=pooled.var() / 1000.0,
                      upper=pooled.var() * 1000)
    sig2 = pm.Uniform("sigma_2", lower=pooled.var() / 1000.0,
                      upper=pooled.var() * 1000)

    v = pm.Exponential("nu", beta=1.0 / 29)

    t1 = pm.NoncentralT("t_1", mu=mu1, lam=1.0 / sig1, nu=v, value=group1[:],
                        observed=True)
    t2 = pm.NoncentralT("t_2", mu=mu2, lam=1.0 / sig2, nu=v, value=group2[:],
                        observed=True)

    model = pm.Model([t1, mu1, sig1, t2, mu2, sig2, v])

    # Generate our MCMC object
    mcmc = pm.MCMC(model)

    mcmc.sample(40000, 10000, 2)

    mus1 = mcmc.trace('mu_1')[:]
    mus2 = mcmc.trace('mu_2')[:]
    sigmas1 = mcmc.trace('sigma_1')[:]
    sigmas2 = mcmc.trace('sigma_2')[:]
    nus = mcmc.trace('nu')[:]

    diff_mus = mus1 - mus2
    diff_sigmas = sigmas1 - sigmas2
    normality = np.log(nus)
    effect_size = (mus1 - mus2) / np.sqrt((sigmas1 ** 2 + sigmas2 ** 2) / 2.)

    print("mu_1", mus1.mean())
    print("mu_2", mus2.mean())
    # return p
