from fitbert import FitBert
from scipy.stats import ttest_rel
def read_for_bert_1(filename):
    """
    Function to read the input file for the first experiment (stimuli_Exp1.txt). This requires not the original file,
    but one where the trailing blank line is removed.

    :param filename: the input file, containing the prompts and alternatives
    :return: raw prompts for two conditions (in the order: thinks - announces) as strings
    """
    # for experiment 1, the data (stimuli_Exp1.txt) contains two conditions, with the marked one coming second
    cond1 = []
    cond2 = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            # since lines come always in triplets (cond1, cond2, blank) we can use % to distinguish the conditions
            # only the second half of each line is kept, since the first just is an identifier
            if i % 3 == 0:
                cond1.append(lines[i].split("\t")[1])
            elif i % 3 == 1:
                cond2.append(lines[i].split("\t")[1])
    return cond1, cond2

def read_for_bert_2_and_3(filename):
    """
    Function to read the input file for the second or third experiment (stimuli_Exp2.txt resp. stimuli_Exp3.txt).

    :param filename: the input file, containing the prompts and alternatives
    :return: raw prompts for two conditions (in the order: ask - blue resp. me - everyone) as strings
    """

    # for experiments 2 and 3, the data (stimuli_Exp2.txt, stimuli_Exp3.txt) contains two conditions, with the marked
    # one coming first; hence, the code is the same as in read_for_bert_1, but with inverting the order of conditions
    cond1 = []
    cond2 = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            # since lines come always in triplets (cond2, cond1, blank) we can use % to distinguish the conditions
            # only the second half of each line is kept, since the first just is an identifier
            if i % 3 == 0:
                cond2.append(lines[i].split("\t")[1])
            elif i % 3 == 1:
                cond1.append(lines[i].split("\t")[1])
    return cond1, cond2

def read_for_bert_4(filename):
    """
    Function to read the input file for the fourth experiment (stimuli_Exp4.txt).

    :param filename: the input file, containing the prompts and alternatives
    :return: raw prompts for three conditions (in the order: low - mid - high) as strings
    """

    # for experiments 4, the data (stimuli_Exp4.txt) contains three conditions, with the most marked one coming first
    # again, we invert the order
    cond1 = []
    cond2 = []
    cond3 = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            # since lines come always in quadruplets (cond3, cond2, cond1, blank) we can use % to distinguish
            # only the second half of each line is kept, since the first just is an identifier
            if i % 4 == 0:
                cond3.append(lines[i].split("\t")[1])
            elif i % 4 == 1:
                cond2.append(lines[i].split("\t")[1])
            elif i % 4 == 2:
                cond1.append(lines[i].split("\t")[1])
    return cond1, cond2, cond3

def convert_for_bert(text):
    """
    Function to convert the raw input (a single string) such that it can be used for the experiment, i.e., by
    separating the prompt from the numbers to choose from, and by masking the blank.

    :param text: the input string
    :return prompt: the prompt itself
    :return options: a list of alternatives (numbers)
    """

    # in the input text, YYYY and XXX are used to separate the options from the prompt
    text = text.replace("YYYY", "XXX")
    text = text.replace("__", "***mask***")
    # separate prompt from options and return them separately
    list = text.split("XXX")
    for i in range(len(list)):
        list[i] = list[i].strip()
    prompt = list[0]
    options = list[1:]
    return prompt, options

def get_probabilities(sentence, alternatives, model):
    """
    Function to get the probabilities for the lower and higher number for a prompt.

    :param sentence: the prompt
    :param alternatives: the options (numbers)
    :param model: the model
    :return: the probabilities for the two options, in the order: lower - higher
    """

    # get the ranking
    ranking = model.rank(sentence, options=alternatives, with_prob=True)
    # the ranking lists the probabilities by their rank, but we want a sorting by lower vs. higher number
    if int(ranking[0][0]) < int(ranking[0][1]):
        # if the ranking is already correct (i.e. [lower, higher]) we keep it as it is and return the probabilities
        return ranking[1]
    else:
        # else we invert them
        return [ranking[1][1], ranking[1][0]]

def compare_choice(cond1, cond2):
    """
    Function to get the relative amount of times the lower number is chosen for either condition.

    :param cond1: raw prompts for the less marked condition as a list of strings
    :param cond2: raw prompts for the more marked condition as a list of strings
    :return: the relative frequency of choosing the lower number for each condition
    """
    lower = 0
    for instance in cond1:
        conv1 = convert_for_bert(instance)
        alternatives_cond1 = [conv1[1][0], conv1[1][1]]
        probabilities_cond1 = get_probabilities(conv1[0], alternatives_cond1, fb)
        if probabilities_cond1[0] > probabilities_cond1[1]:
            lower += 1
    ratio_cond1 = lower / len(cond1)

    lower = 0
    for instance in cond2:
        conv2 = convert_for_bert(instance)
        alternatives_cond2 = [conv2[1][0], conv2[1][1]]
        probabilities_cond2 = get_probabilities(conv2[0], alternatives_cond2, fb)
        if probabilities_cond2[0] > probabilities_cond2[1]:
            lower += 1
    ratio_cond2 = lower / len(cond2)

    return ratio_cond1, ratio_cond2

def apply_ttest(cond1, cond2):
    """
    Function to apply a paired t-test.

    :param cond1: raw prompts for the less marked condition as a list of strings
    :param cond2: raw prompts for the more marked condition as a list of strings
    :return: t-test statistics for the null hypothesis that higher numbers are not more likely for the more marked
    than for the less marked condition
    """
    ratios_cond1 = []
    ratios_cond2 = []

    for instance in cond1:
        conv1 = convert_for_bert(instance)
        alternatives_cond1 = [conv1[1][0], conv1[1][1]]
        probabilities_cond1 = get_probabilities(conv1[0], alternatives_cond1, fb)
        ratios_cond1.append(probabilities_cond1[0]/probabilities_cond1[1]) # ratio lower/higher

    for instance in cond2:
        conv2 = convert_for_bert(instance)
        alternatives_cond2 = [conv2[1][0], conv2[1][1]]
        probabilities_cond2 = get_probabilities(conv2[0], alternatives_cond2, fb)
        ratios_cond2.append(probabilities_cond2[0]/probabilities_cond2[1])

    result = ttest_rel(ratios_cond1, ratios_cond2, alternative='greater')
    return result


# initialize the model
fb = FitBert()

# get and print the results for experiment 1
cond1, cond2 = read_for_bert_1("stimuli_Exp1.txt")
print(compare_choice(cond1, cond2))
print(apply_ttest(cond1, cond2))

# get and print the results for experiment 2
cond1, cond2 = read_for_bert_2_and_3("stimuli_Exp2.txt")
print(compare_choice(cond1, cond2))
print(apply_ttest(cond1, cond2))

# get and print the results for experiment 3
cond1, cond2 = read_for_bert_2_and_3("stimuli_Exp3.txt")
print(compare_choice(cond1, cond2))
print(apply_ttest(cond1, cond2))

# get and print the results for experiment 4 by comparing pairs of conditions
cond1, cond2, cond3 = read_for_bert_4("stimuli_Exp4.txt")
print(compare_choice(cond1, cond2))
print(apply_ttest(cond1, cond2))
print(compare_choice(cond2, cond3))
print(apply_ttest(cond2, cond3))
print(compare_choice(cond1, cond3))
print(apply_ttest(cond1, cond3))