import numpy as np

def polynomial(X, M):
    phi = np.array([X ** i for i in range(M)]).T
    return phi

def identity(X, M):
    phi = np.array([X  for _ in range(M)]).T
    return phi

def gaussian(X, mu_list, sigma_list=[0.1]):
    f = lambda x, mu, sigma: np.exp(-0.5 * (x - mu) ** 2 / sigma ** 2)
    phi = []
    for x in X:
        phi_list = [x]
        for mu in mu_list:
            for sigma in sigma_list:
                phi_list.append(f(x, mu, sigma))
        phi.append(phi_list)
    phi = np.array(phi)
    return phi
    