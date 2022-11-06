import numpy as np

def get_exponential_rv(lmbda):
    u = np.random.uniform(0, 1)
    x = -(1 / lmbda) * np.log(1 - u)
    return x
