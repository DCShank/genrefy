#!/usr/bin/env python
import numpy as np
from collections import defaultdict
from math import inf


def readWordVector(vec_str):
    """ Translates a word vector string to a word + vector """
    split_str = vec_str.split()
    word = split_str[0]
    nums = np.array([float(x) for x in split_str[1:]])
    return (word, np.array(nums))


def readVecFile(vec_file):
    """ Reads in a vector file and outputs a word vector dictionary """
    word_embeddings = dict()
    for line in vec_file:
        word, vector = readWordVector(line.strip())
        word_embeddings[word] = vector
    return word_embeddings


def averageDocument(embeddings, doc):
    """ Averages the vectors ina document """
    vectors = []
    for word in doc.split():
        if word in embeddings:
            vectors.append(embeddings[word])
    return np.mean(vectors, axis=0)


def trainClassifier(embeddings, documents):
    """ Finds the average genre vector for each genre in a corpus """
    genre_vecs = defaultdict(lambda: [])
    for doc in documents:
        text, genres = doc.split('\t')
        doc_vec = averageDocument(embeddings, text.strip())
        for genre in eval(genres):
            genre_vecs[genre].append(doc_vec)
    for genre, vectors in genre_vecs.items():
        genre_vecs[genre] = np.mean(vectors, axis=0)
    return genre_vecs


def classify(genre_vectors, embeddings, doc):
    doc_vec = averageDocument(embeddings, doc)
    cur_genre = ''
    cur_dist = inf
    for genre, gen_vec in genre_vectors.items():
        dist = np.linalg.norm(doc_vec-gen_vec)
        if cur_dist > dist:
            cur_genre = genre
            cur_dist = dist
    return cur_genre


def classifyRelative(genre_vectors, embeddings, rel_probs, doc):
    doc_vec = averageDocument(embeddings, doc)
    cur_genre = ''
    cur_dist = inf
    for genre, gen_vec in genre_vectors.items():
        dist = np.linalg.norm(doc_vec-gen_vec)
        dist = dist/(rel_probs[genre])
        if cur_dist > dist:
            cur_genre = genre
            cur_dist = dist
    return cur_genre


def classifyAll(genre_vectors, embeddings, documents):
    number_correct = 0
    number_guessed = 0
    guess_dict = defaultdict(lambda: 0)
    correct_dict = defaultdict(lambda: 0)

    for doc in documents:
        text, genres = doc.split('\t')
        gen = classify(genre_vectors, embeddings, doc)
        number_guessed += 1
        guess_dict[gen] += 1
        if gen in eval(genres):
            number_correct += 1
            correct_dict[gen] += 1

    print(number_correct/number_guessed)
    return (guess_dict, correct_dict)


def classifyAllRelative(genre_vectors, embeddings, relative, documents):
    genre_prob = dict()
    for line in relative:
        genre, prob = line.split('\t')
        genre_prob[genre] = float(prob)

    number_correct = 0
    number_guessed = 0
    guess_dict = defaultdict(lambda: 0)
    correct_dict = defaultdict(lambda: 0)

    for doc in documents:
        text, genres = doc.split('\t')
        gen = classifyRelative(genre_vectors, embeddings, genre_prob, doc)
        number_guessed += 1
        guess_dict[gen] += 1
        if gen in eval(genres):
            number_correct += 1
            correct_dict[gen] += 1

    print(number_correct/number_guessed)
    return (guess_dict, correct_dict)


if __name__ == '__main__':
    pass
