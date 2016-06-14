#!/usr/bin/env python3

import numpy as np
from neural_net import train_network, predict


def simple():
    X = np.array([
        [0.35, 0.9]
    ])

    y = np.array([
        [0.5]
    ])

    theta1 = np.array([
        [0.0, 0.0],
        [0.1, 0.4],
        [0.8, 0.6]
    ])

    theta2 = np.array([
        [0.0],
        [0.3],
        [0.9]
    ])

    thetas = [theta1, theta2]

    model = train_network(
        X,
        y,
        weights=thetas,
        stop_condition=lambda i, e: True
    )

    print('error before training:', predict(thetas, X) - y)
    print('error after training:', predict(model, X) - y)
    for l, w in enumerate(model):
        print('weights for layer %s:' % l)
        print(w)


if __name__ == '__main__':
    simple()
