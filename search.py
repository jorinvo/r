import re
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from collections import Counter, defaultdict
from math import log10
from bs4 import BeautifulSoup
import numpy as np


teleportation = 0.05
target_delta = 0.04

seed = [
    'https://jorin.me/'
]

stop_words = [
    'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
    'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
    'that', 'the', 'this', 'to', 'we'
]

queries = [
    ['python'],
    ['zip'],
    ['git'],
    ['go', 'ruby']
]


def main():
    # doing all the calculations
    frontier = crawl(seed)
    link_structure = create_link_structure(frontier)
    ranks = page_rank(link_structure)
    rank = best_rank(ranks, link_structure)
    N = len(link_structure)
    index = create_index(link_structure)
    weighted_index = weight_index(index, N)
    norm_index = normalize_index(weighted_index)

    # pretty print results
    print()
    print('Index size:', len(index))
    print('Interations for PageRank:', len(ranks))
    print()
    print_combined_search(norm_index, N, rank)


# Crawler

def crawl(urls, frontier={}, bases=None):
    '''
    Takes a list of urls as argument and crawls them recursivly until
    no new url can be found.

    Returns a dict with urls as keys and
    tuples (name, content, links) as values.
    Links is a list of urls.
    '''
    def norm(urls):
        return [u.rstrip('/') for u in urls]

    if not bases:
        bases = [urlparse(url).netloc for url in urls]
    for url in norm(urls):
        if url in frontier:
            continue
        page = parse(download(url), url, bases)
        print('crawled %s with %s links' % (url, len(page[2])))
        frontier[url] = page
        crawl(page[2], frontier, bases)
    return frontier


def download(url):
    return urlopen(url)


def parse(html, url, bases):
    '''
    Takes an html string and a url as arguments.

    Returns a tuple (name, content, links) parsed from the html.
    '''
    soup = BeautifulSoup(html, 'lxml')

    content = soup.body.get_text().strip()

    links = [urljoin(url, link.get('href')) for link in soup.findAll('a')]
    links = [link for link in links if urlparse(link).netloc in bases]
    return soup.title.string, content, links


def create_link_structure(frontier):
    '''
    Takes the frontier dict.

    Returns a sorted list of tuples (name, content, links).
    links are formatted as names.
    '''
    return sorted([(url, page[1], page[2]) for url, page in frontier.items()])


# PageRank

def page_rank(link_structure):
    '''
    Returns a matrix with documents as columns
    and values for each round as rows.

    Number of rows depends on how long it takes to reach the target_delta.
    '''
    N = len(link_structure)
    transition_matrix = create_transition_matrix(link_structure)
    ranks_in_steps = [[1 / N] * N]
    while True:
        possibilities = ranks_in_steps[-1] * transition_matrix
        delta = get_delta(possibilities, ranks_in_steps[-1])
        ranks_in_steps.append(np.squeeze(np.asarray(possibilities)))
        if delta <= target_delta:
            return ranks_in_steps


def create_transition_matrix(link_structure):
    '''
    Returns a matrix with document names as rows
    and document links as columns.

    Each cell contains the propability for a document
    to transition to a link.
    '''
    links = [links for name, content, links in link_structure]
    names = get_names(link_structure)
    N = len(link_structure)
    m = np.matrix([[weight_link(N, n, l) for n in names] for l in links])
    return teleport(N, m)


def weight_link(N, name, links):
    if not links:
        return 1 / N
    if name in links:
        return 1 / len(links)
    else:
        return 0


def teleport(N, m):
    return m * (1 - teleportation) + teleportation / N


def get_delta(a, b):
    return np.abs(a - b).sum()


def best_rank(ranks, link_structure):
    '''
    Returns a dict with document names as keys
    and their ranks as values.
    '''
    return dict(zip(get_names(link_structure), ranks[-1]))


def get_names(link_structure):
    return [name for name, content, links in link_structure]


# Index

def create_index(link_structure):
    '''
    Returns the index as a dict with terms as keys
    and lists tuples(name, count) as values.

    Count says how many times the term occured in the document.
    '''
    index = defaultdict(list)
    for name, content, links in link_structure:
        counts = count_terms(content)
        for term, count in counts.items():
            index[term].append((name, count))
    return index


def count_terms(content):
    '''
    content is a text string.

    Returns a Counter with terms as keys
    and their occurence as values.
    '''
    return Counter(get_terms(content))


normalize = re.compile('[^a-z0-9]+')


def get_terms(s):
    '''
    Get a list of terms from a string.
    Terms are lower case and all special characters are removed.
    '''
    normalized = [normalize.sub('', t.lower()) for t in s.split()]
    return [t for t in normalized if t not in stop_words]


def weight_index(index, N):
    '''
    Takes an index as first argument
    and the total number of documents as second argument.

    Returns a new index with tf_idf weights instead of simple counts.
    '''
    weighted_index = defaultdict(list)
    for term in index:
        docs = index[term]
        df = len(docs)
        for name, count in docs:
            weight = tf_idf(count, N, df)
            weighted_index[term].append((name, weight))
    return weighted_index


def tf_idf(tf, N, df):
    return wtf(tf) * idf(N, df)


def wtf(tf):
    return 1 + log10(tf)


def idf(N, df):
    return log10(N / df)


def normalize_index(index):
    '''
    Takes an index as argument.

    Returns a new index with normalized weights.
    '''
    lengths = doc_lengths(index)
    norm_index = defaultdict(list)
    for term in index:
        for name, weight in index[term]:
            norm_index[term].append((name, weight / lengths[name]))
    return norm_index


def doc_lengths(index):
    '''
    Returns a dict with document names as keys
    and vector lengths as values.

    The length is calculated using the vector of weights
    for the terms in the document.
    '''
    doc_vectors = defaultdict(list)
    for docs in index.values():
        for name, weight in docs:
            doc_vectors[name].append(weight)
    return {name: np.linalg.norm(doc) for name, doc in doc_vectors.items()}


# Search & Scoring

def cosine_score(index, N, query):
    '''
    query is a list of terms.

    Returns a sorted list of tuples (name, score).

    Score is calculated using the cosinus distance
    between document and query.
    '''
    scores = defaultdict(int)
    qw = {t: tf_idf(1, N, len(index[t])) for t in query if t in index}
    query_len = np.linalg.norm(qw.values())
    for term in qw:
        query_weight = qw[term] / query_len
        for name, weight in index[term]:
            scores[name] += weight * query_weight
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def combined_search(index, N, rank, query):
    '''
    Returns a sorted list of tuples (name, score).

    Score is the product of the cosinus score and the PageRank.
    '''
    scores = cosine_score(index, N, query)
    combined = [(doc, score * rank[doc]) for doc, score in scores]
    return sorted(combined, key=lambda x: x[1], reverse=True)


def print_combined_search(index, N, rank):
    print('Search results:\n')
    for query in queries:
        print(' '.join(query))
        for name, score in combined_search(index, N, rank, query):
            print('%.6f   %s' % (score, name))


if __name__ == "__main__":
    main()
