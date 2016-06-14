#!/usr/bin/env python3

import numpy as np
from neural_net import train_network, predict


def xor():
    X = np.array([
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 1]
    ])

    y = np.array([
        [0],
        [1],
        [1],
        [0]
    ])

    np.random.seed(1)

    model = train_network(
        X,
        y,
        hidden_layers=[2],
        learn_rate=10,
        batch_size=len(X)
    )

    print('prediction after training:\n', predict(model, X))
    for l, w in enumerate(model):
        print('weights for layer %s:' % l)
        print(w)


if __name__ == '__main__':
    xor()
