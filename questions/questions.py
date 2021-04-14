import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    import os
    import re

    files = dict()

    for file in os.scandir(directory):
        if re.search(".txt$", file.name):
            with open(file.path, "r", encoding="utf8") as f:
                # re.sub(".txt$", "", file.name)
                files[file.name] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    import string

    #  tokenize the given document
    words = nltk.tokenize.word_tokenize(document)
    words = [word.lower() for word in words]

    # filter words from punctuations and stopwords
    loop_words = words.copy()
    for word in loop_words:
        if word in [char for char in string.punctuation] + nltk.corpus.stopwords.words("english"):
            words.remove(word)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    from math import log

    # number of documents
    TotalDocuments = len(documents)

    # create set of all words in all docs
    words = set()
    for words_list in documents.values():
        for word in words_list:
            words.add(word)

    # calculate how many doc containing each words, then calculate idfs
    nDocsContain = dict()
    idfs = dict()
    for word in words:
        nDocsContain[word] = 0
        for words_list in documents.values():
            if word in words_list:
                nDocsContain[word] += 1 
        idfs[word] = log(TotalDocuments/nDocsContain[word])

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # calculate term-frequency of each words in query
    tf = dict()
    for query_word in query:
        tf[query_word] = dict()
        for file_name in files:
            tf[query_word][file_name] = files[file_name].count(query_word)

    # claculate tf-idfs of each document
    tf_idfs = dict()
    for file_name in files:
        tf_idfs[file_name] = 0
        for query_word in query:
            tf_idfs[file_name] += tf[query_word][file_name] * idfs[query_word]
            
    #  create sorted list by tf_idfs
    sorted_tf_idfs = sorted(tf_idfs, key= lambda item: tf_idfs[item], reverse= True)

    # return list contains top n file names
    top_files_names = []
    for index in range(n):
        top_files_names.append(sorted_tf_idfs[index]) 

    return top_files_names
    

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # claculate idfs of each sentence
    sent_score = dict()
    for sentence in sentences:
        sent_score[sentence] = 0
        for query_word in query:
            if query_word in sentences[sentence]:
                sent_score[sentence] += idfs[query_word]

    # create sorted list of sentences
    sorted_sentences = sorted(sent_score, key= lambda item: sent_score[item], reverse= True)

    # re-order sentences with the same rank of idfs according to query term density
    loop_sentences = sorted_sentences.copy()
    for sentence1 in loop_sentences:
        for sentence2 in loop_sentences:
            if sentence1 != sentence2:
                if sent_score[sentence1] == sent_score[sentence2]:
                    qtd1 = query_term_density(sentence1, query, sentences)
                    qtd2 = query_term_density(sentence2, query, sentences)
                    index1 = sorted_sentences.index(sentence1)
                    index2 = sorted_sentences.index(sentence2)
                    if qtd1 > qtd2:
                        if index1 > index2:
                            sorted_sentences[index2], sorted_sentences[index1] = sorted_sentences[index1], sorted_sentences[index2]
                    elif qtd1 < qtd2:
                        if index1 < index2:
                            sorted_sentences[index2], sorted_sentences[index1] = sorted_sentences[index1], sorted_sentences[index2]

    # get list contains top n sentences
    top_sentences = []
    for index in range(n):
        top_sentences.append(sorted_sentences[index]) 

    return top_sentences

def query_term_density(sentence, query, sentences):
    """
    return query_term_density
    """
    freq = 0
    for sentence_word in sentences[sentence]:
        if sentence_word in query:
            freq =+ 1
    
    result = freq / len(sentences[sentence])

    return result


if __name__ == "__main__":
    main()
