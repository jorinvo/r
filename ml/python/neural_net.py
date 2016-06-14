#!/usr/bin/env python3

import numpy as np


def rounds1k(iteration, error):
    return iteration > 1000


def sigmuid(x):
    return 1 / (1 + np.exp(-x))


def random_weights(layers):
    return [np.random.random((layers[l] + 1, layers[l + 1])) - 0.5
            for l in range(len(layers) - 1)]


def add_bias(bias, X):
    return np.hstack((np.ones((len(X), 1)) * bias, X))


def split_batches(batch_size, X, y):
    indices = range(batch_size, len(X), batch_size)
    return list(zip( np.split(X, indices), np.split(y, indices)))


def forward_pass(nonlin, bias, weights, X):
    layer = X
    layers = [layer]
    for weight in weights:
        layer = nonlin(add_bias(bias, layer) @ weight)
        layers.append(layer)
    return layers


def backpropagation(bias, layers, weights, error):
    delta = error * layers[-1] * (1 - layers[-1])
    deltas = [delta]
    # go backwards through layers, skip last and first
    for l in range(len(layers) - 2, 0, -1):
        weight_no_bias = weights[l][1:, :]
        delta = (delta @ weight_no_bias.T) * layers[l] * (1 - layers[l])
        deltas.insert(0, delta)
    return [add_bias(bias, l).T @ d for l, d in zip(layers, deltas)]


def train_network(
    X,
    y,
    *,
    hidden_layers=[],
    learn_rate=1,
    stop_condition=rounds1k,
    batch_size=1,
    bias=1,
    nonlin=sigmuid,
    weights=None
):
    if not weights:
        weights = random_weights([X.shape[1]] + hidden_layers + [y.shape[1]])
    batches = split_batches(batch_size, X, y)
    iteration = 0
    while True:
        for batch_x, batch_y in batches:
            m = len(batch_x)
            layers = forward_pass(nonlin, bias, weights, batch_x)
            error = layers[-1] - batch_y
            changes = backpropagation(bias, layers, weights, error)
            weights = [w - (learn_rate / m) * c for w, c in zip(weights, changes)]
            if stop_condition(iteration, error):
                return weights
            iteration += 1


def predict(model, X, bias=1, nonlin=sigmuid):
    layer = X
    for weight in model:
        layer = nonlin(add_bias(bias, layer) @ weight)
    return layer