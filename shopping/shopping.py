import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    import datetime

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = True
        evidence = list()
        labels = list()
        for line in csv_reader:
            # skip headers
            if first_row:
                first_row = False
                continue
            # convert month into number
            month_name = line[10]
            try:
                datetime_object = datetime.datetime.strptime(month_name, "%b")
            except:
                datetime_object = datetime.datetime.strptime(month_name, "%B")
            month_number = datetime_object.month
            # convert visitor type into number
            VisitorType = 1 if line[15] == "Returning_Visitor" else 0
            # convert weekend into number
            Weekend = 1 if line[16] == "TRUE" else 0
            # append evidence and label
            evidence.append(
                [
                    int(line[0]),
                    float(line[1]),
                    int(line[2]),
                    float(line[3]),
                    int(line[4]),
                    float(line[5]),
                    float(line[6]),
                    float(line[7]),
                    float(line[8]),
                    float(line[9]),
                    month_number,
                    float(line[11]),
                    float(line[12]),
                    float(line[13]),
                    float(line[14]),
                    VisitorType,
                    Weekend
                ]
            )
            labels.append(1 if line[17] == "TRUE" else 0)

        return((evidence, labels))


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = sum(
        [1 for label, prediction in zip(labels, predictions) if (
            label == 1 and label == prediction)]
    ) / sum(
        [1 for label in labels if label == 1]
    )

    specificity = sum(
        [1 for label, prediction in zip(labels, predictions) if (
            label == 0 and label == prediction)]
    ) / sum(
        [1 for label in labels if label == 0]
    )

    return sensitivity, specificity


if __name__ == "__main__":
    main()
