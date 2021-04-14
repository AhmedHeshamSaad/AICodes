import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # import math
    # assess how many genes every person has in that state
    gene = dict()
    for person_name in people.keys():
        if person_name not in one_gene | two_genes:
            gene[person_name] = 0
        elif person_name in one_gene:
            gene[person_name] = 1
        elif person_name in two_genes:
            gene[person_name] = 2

    # calculate probability of carrying such number of genes and having trait for each person
    # P = []
    JP = 1
    for person_name in people.keys():
        if not people[person_name]["mother"] or not people[person_name]["father"]:
            if gene[person_name] == 0:
                P_gene = PROBS["gene"][0]
            elif gene[person_name] == 1:
                P_gene = PROBS["gene"][1]
            elif gene[person_name] == 2:
                P_gene = PROBS["gene"][2]
        else:
            notmother = (gene[people[person_name]["mother"]] == 0) * (1 - PROBS["mutation"]) + 0.5 * (
                gene[people[person_name]["mother"]] == 1) + (gene[people[person_name]["mother"]] == 2) * PROBS["mutation"]

            notfather = (gene[people[person_name]["father"]] == 0) * (1 - PROBS["mutation"]) + 0.5 * (
                gene[people[person_name]["father"]] == 1) + (gene[people[person_name]["father"]] == 2) * PROBS["mutation"]

            if gene[person_name] == 0:
                # probability of having no gene given his ..
                P_gene = notmother * notfather
            elif gene[person_name] == 1:
                # probability of having 1 gene ..
                P_gene = (1-notmother) * notfather + notmother * (1-notfather)
            elif gene[person_name] == 2:
                # probability of having 2 genes
                P_gene = (1-notmother) * (1-notfather)

        # probability of trait or not
        P_trait = PROBS["trait"][gene[person_name]][person_name in have_trait]

        # P.append(P_gene * P_trait)
        JP = JP * P_gene * P_trait

    # JP = math.prod(P)
    return JP


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person_name in probabilities.keys():
        if person_name not in one_gene | two_genes:
            probabilities[person_name]["gene"][0] += p
            probabilities[person_name]["trait"][person_name in have_trait] += p
        elif person_name in one_gene:
            probabilities[person_name]["gene"][1] += p
            probabilities[person_name]["trait"][person_name in have_trait] += p
        elif person_name in two_genes:
            probabilities[person_name]["gene"][2] += p
            probabilities[person_name]["trait"][person_name in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person_name in probabilities.keys():
        ng = 1 / sum(probabilities[person_name]["gene"].values())
        nt = 1 / sum(probabilities[person_name]["trait"].values())

        probabilities[person_name]["gene"][0] *= ng
        probabilities[person_name]["gene"][1] *= ng
        probabilities[person_name]["gene"][2] *= ng

        probabilities[person_name]["trait"][True] *= nt
        probabilities[person_name]["trait"][False] *= nt


if __name__ == "__main__":
    main()
