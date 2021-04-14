import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    all_pages = corpus.keys()
    N = len(all_pages)

    linked_pages = corpus[page]
    n = len(linked_pages)

    # if a page has no links, pretend it has links to all pages in the corpus, including itself.
    if n == 0:
        linked_pages = all_pages
        n = N

    PD = dict()

    # loop over all pages in the corpus
    for this_page in all_pages:
        # calculate its probability and add it to the PD dictionary
        if this_page in linked_pages:
            PD[this_page] = damping_factor/n + (1-damping_factor)/N
        else:
            PD[this_page] = (1-damping_factor)/N

    return PD


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    samples = []

    # first iteration
    current_page = random.choice(all_pages)
    samples.append(current_page)

    for i in range(1, n):
        # get probability distrubution of all pages from the current_page
        PD = transition_model(corpus, current_page, damping_factor)

        # get random page given all pages and thier probability distribution
        current_page = random.choices(all_pages, weights=PD.values(), k=1)[0]

        # append this page to the samples list
        samples.append(current_page)

    # calculate ranks of each page and store its as a value to a dictionary
    ranks = dict()
    for page in all_pages:
        ranks[page] = samples.count(page)/n

    print("no of samples: " + str(n))
    print("Sum of sampled ranks: " +
          str(sum(ranks[p] for p in list(ranks.keys()))))
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # get all pages name and how many
    all_pages = list(corpus.keys())
    N = len(all_pages)

    # initiatize ranks values to be 1/N
    old_ranks = dict()
    for page in all_pages:
        old_ranks[page] = 1/N

    # iterate to solve the equation until solution converge
    new_ranks = dict()
    i = 1
    while True:
        i += 1
        # empty uncertainty list for each page
        e = []

        # calculate new ranks for all pages
        for page in all_pages:
            # calculate new rank for current page
            new_ranks[page] = PR(corpus, page, old_ranks, damping_factor)
            # append new uncertainity to the list
            e.append(abs(new_ranks[page] - old_ranks[page]))

        # update old ranks to be used in the next iteration
        old_ranks = new_ranks.copy()

        # check convergance criteria
        e = max(e)
        if e < 0.001:
            break

    print("no of iterations: " + str(i))
    print("Sum of iterate ranks: " +
          str(sum(new_ranks[p] for p in list(new_ranks.keys()))))
    return new_ranks


def PR(corpus, page, ranks, damping_factor):
    """
    Return page rank value using other pages' ranks exiting in the corpus

    Return an integer represent page rank
    """
    # get all pages that links to that page
    links = links_to(corpus, page)

    # claculate summation value in the equation
    s = 0
    for link in links:
        s = s + ranks[link] / NumLinks(corpus, link)

    page_rank = (1-damping_factor)/len(corpus.keys()) + damping_factor * s

    return page_rank


def NumLinks(corpus, page):
    """
    Return number of links in a given page in the corpus
    """
    n = len(corpus[page])
    # print(n)
    # if no links, interpret it as having links to all the pages including itself
    if n == 0:
        n = len(corpus.keys())

    return n


def links_to(corpus, page):
    """
    Return list of pages in given corpus which have link to given page
    """
    # intiatize an empty links list
    links = []

    # iterate over the corpus pages and thier links
    for p, l in corpus.items():
        # if page in the current links, append it to the list
        # if not and llinks
        #  is empty, interpret it as having links to
        # all the pages and append it to the list
        if page in l:
            links.append(p)
        elif not l:  # if empty
            links.append(p)

    return links


if __name__ == "__main__":
    main()
