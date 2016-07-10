'''
Data folder structure:

    Must contain a directory for each category.
    Category directories must contain 'train' and 'test' directories.
    Each of them must only contain plain text files.

    Example:
        data
            politics
                train
                    doc1
                    doc2
                test
                    doc3
            economy
                train
                    doc4
                    doc5
                    doc6
                test
                    doc7

Types:

    data        = {category: [(doc_title, Counter({token: count}))]}
    model       = vocabulary, class_prior, condprob
    vocabulary  = set(token)
    class_prior = {category: float}
    condprop    = {token: float}    (conditional probability)
'''


import re
import os
import argparse
from collections import Counter, defaultdict
from math import log


def main():
    args = get_args()
    train_data = get_data('train', args.data_dir)
    model = train(train_data)
    test_data = get_data('test', args.data_dir)
    test_model(model, test_data, args.print_predictions)


def get_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'data_dir',
        type=str,
        help='Path to data folder'
    )
    parser.add_argument(
        '-p',
        '--print-predictions',
        action='store_true',
        help='Print out prediction for each document'
    )
    return parser.parse_args()


def get_data(base, data_dir):
    data = defaultdict(list)
    for category in os.listdir(data_dir):
        train_dir = os.path.join(data_dir, category, base)
        for path in os.listdir(train_dir):
            counter = Counter()
            with open(os.path.join(train_dir, path)) as f:
                for line in f:
                    counter.update(get_tokens(line))
            data[category].append((path, counter))
    return data


norm = re.compile('[^a-z0-9]+')


def get_tokens(s):
    return [norm.sub('', t.lower()) for t in s.split()]


def train(data):
    vocabulary = get_vocabulary(data)
    N = count_docs(data)
    B = len(vocabulary)
    class_prior = {c: len(data[c]) / N for c in data}

    print('Training:')
    print('{} docs and vocabulary size of {}'.format(N, len(vocabulary)))

    condprob = defaultdict(dict)
    for c, doc_list in data.items():
        print('- Category "{}" with {} docs'.format(c, len(doc_list)))
        class_counter = sum((counter for path, counter in doc_list), Counter())
        tokens_in_class = sum(class_counter.values()) + B
        for token in vocabulary:
            T_ct = class_counter[token]
            condprob[token][c] = (T_ct + 1) / tokens_in_class

    return vocabulary, class_prior, condprob


def get_vocabulary(data):
    vocabulary = set()
    for doc_list in data.values():
        for path, counter in doc_list:
            vocabulary.update(set(counter.keys()))
    return vocabulary


def count_docs(data):
    return sum(len(doc_list) for doc_list in data.values())


def test_model(model, test_data, print_predictions):
    correct_predictions = 0
    if print_predictions:
        print('document: prediction(actual)')
    for category, doc_list in test_data.items():
        for title, counter in doc_list:
            prediction = predict(*model, counter)
            if prediction == category:
                correct_predictions += 1
            if print_predictions:
                print('{}: {}({})'.format(title, prediction, category))
    print('Accuracy: ', round(correct_predictions / count_docs(test_data), 2))


def predict(vocabulary, class_prior, condprob, doc):
    scores = {}
    for c, prior in class_prior.items():
        condprobs = sum(log(condprob[t][c]) for t in doc if t in vocabulary)
        scores[c] = log(prior) + condprobs
    return max(scores, key=scores.get)


if __name__ == '__main__':
    main()
