import numpy as np
import csv
import os
import codecs
import argparse
from bayesian import BayesianModel
from functions import *
from matplotlib import pyplot as plt

def get_config():
	parser = argparse.ArgumentParser(description='Bayesian Curve Fitting Model')
	parser.add_argument('-f', '--file', help='the historical csv file to be loaded for fitting.')
	parser.add_argument('-bf', '--basic_function', default="gaussian", help='the basic function used for fitting. [polynomial|identity|gaussian] (default:gaussian)')
	parser.add_argument('-d', '--degree',type=int, default=32, help='the degree of basic function. (default:32)')
	# Parse args.
	args = parser.parse_args()
	return args

def load_data(file):
    with codecs.open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        column = {}
        for h in headers:
            column[h] = []
        for row in reader:
            for h, v in zip(headers, row):
                column[h].append(v.replace('\ufeff', ''))
    t = column['open']
    return np.arange(len(t)), np.array(t, dtype=np.float64)

def plot(X_original, t_original, t_predicted, train_limit):
    x1 = X_original[:train_limit]
    y1 = t_original[:train_limit]
    x2 = X_original[:train_limit+1]
    y2 = t_predicted
    x3 = X_original[train_limit:train_limit+1]
    y3 = t_original[train_limit:train_limit+1]
    # l1 = plt.plot(x1,y1,'b-',label='true')
    # l2 = plt.plot(x2,y2,'r-',label='predicted')
    plt.plot(x1,y1,'bo-',label='true')
    plt.plot(x2,y2,'r+-',label='predicted')
    plt.plot(x3,y3,'bo-')
    plt.title('Bayesian Curve Fitting')
    plt.xlabel('day')
    plt.ylabel('open')
    plt.legend()
    plt.show()

def performance(t_original, t_predicted):
    t_original = t_original[:len(t_predicted)]
    MAE = np.mean(np.abs(t_predicted - t_original))
    MRE = np.mean(np.abs(t_predicted - t_original) / np.abs(t_original))
    print(f"MAE:{MAE}\nMRE:{MRE}")
    return MAE, MRE


if __name__ == '__main__':
    args = get_config()
    if args.file is None or not os.path.isfile(args.file):
        print('Please provide the data file. (Use --help for help)')
        exit(1)
    X_original, t_original = load_data(args.file)
    train_limit = 100
    X = X_original / (train_limit + 1)
    X_test = X[:train_limit+1]
    X = X[:train_limit]
    t = t_original[:train_limit]
    M = args.degree
    if args.basic_function == "polynomial":
        phi = polynomial(X, M)
        phi_test = polynomial(X_test, M)
    elif args.basic_function == "identity":
        phi = identity(X, M)
        phi_test = identity(X_test, M)
    elif args.basic_function == "gaussian":
        mu_list = np.linspace(0, 1, M)
        sigma_list = [0.1**i for i in range(1, 5)]
        phi = gaussian(X, mu_list, sigma_list)
        phi_test = gaussian(X_test, mu_list, sigma_list)
    else:
        raise RuntimeError('NotImplemented')
    model = BayesianModel()
    model.fit(phi, t, verbose=True)
    t_predicted, t_var = model.predict(phi_test)
    performance(t_original, t_predicted)
    plot(X_original, t_original, t_predicted, train_limit)