import torch
import pandas as pd


def extract_number(question, response):
    """This function defines whether the lower or higher or both or neither number
    of the question is present in the model response
    """
    # this is still very rough and could be modified to reduce the risk of missing out some instances (e.g. by
    # excluding more irrelevant punctuation marks, or including number word representations)
    qs = question.replace("?", "").split()
    low = qs[-3]
    high = qs[-1]
    has_low = False
    has_high = False
    rs = response.replace(".", "").replace(",", "").split()
    for i in rs:
        if i == low:
            has_low = True
        if i == high:
            has_high = True

    if has_low and has_high:
        return "both"
    elif has_low:
        return "low"
    elif has_high:
        return "high"
    else:
        return "neither"


def count_string_occurrences(dataframe, column_name):
    # Get the counts of each string in the specified column
    string_counts = dataframe[column_name].value_counts()

    # Create a dictionary to store the string counts
    counts = {}

    # Iterate over the unique strings and their counts
    for string, count in string_counts.items():
        counts[string] = count

    return counts
