import torch
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, GPT2LMHeadModel, GPT2Tokenizer
import re


def convert_exp1(text):
    """this function converts thtanden, dann ist es klar verteilt und bleibt sauber. :)
Wenn wir das Gespräch online machen könnten, we experimental item into a prompt
    :text param: experimental item/sentence
    :output: prompt for model
    """
    text = text.replace(
        "XXX", ". Choose the more likely number:").replace("YYYY", "or")
    text = text+"?"
    return text


def process_stimuli(exp_stimuli):
    """
    Processes a stimuli file and extracts "thinks" and "announced" prompts in two sepetate datasets.
    :param convert_func: requires function to convert the prompts as needed.
    :param exp_stimuli: requires a string of experimental txt file
    :return: List of "thinks" and list of "announced" prompts.
    """
    thinks = []
    announced = []
    all_lines = []
    stimuli_exp1_file = open(exp_stimuli, 'r')
    # open file (from: https://osf.io/9eg34/)

    for l in stimuli_exp1_file.readlines():
        all_lines.append(l)

    for i in range(len(all_lines)//3):

        # in the file, there is always one "thinks" line followed by one "announced" line and one blank line
        line1 = all_lines.pop(0)
        # remove first part since it's an identifier
        text1 = " ".join(line1.split()[1:])
        # prompt1 = convert_func(text1)
        # thinks.append(prompt1)
        thinks.append(text1)

        line2 = all_lines.pop(0)
        text2 = " ".join(line2.split()[1:])
        # prompt2 = convert_func(text2)
        # announced.append(prompt2)
        announced.append(text2)

        all_lines.pop(0)

    return thinks, announced


def join_prompts(thinks, announced):

    for t, a in zip(thinks, announced):
        print(t, a)
        prompt = convert_exp1(t)
        print(prompt)
        return prompt



def process_stimuli_exp4(convert_func, exp_stimuli):
    """
    Processes a stimuli file for experiment 4.
    :param convert_func: requires function to convert the prompts as needed.
    :param exp_stimuli: requires a string of experimental txt file
    :return: List of "high", list of "mid", and list of "low" prompts.
    """
    high = []
    mid = []
    low = []
    all_lines = []
    stimuli_exp1_file = open(exp_stimuli, 'r')
    # open file (from: https://osf.io/9eg34/)

    for l in stimuli_exp1_file.readlines():
        all_lines.append(l)

    for i in range(len(all_lines)//4):

        # in the file, there is always one "high" line followed by one "mid" line, on "low" line, and one blank line
        line1 = all_lines.pop(0)
        # remove first part since its an identifier
        text1 = " ".join(line1.split()[1:])
        prompt1 = convert_func(text1)
        high.append(prompt1)

        line2 = all_lines.pop(0)
        text2 = " ".join(line2.split()[1:])
        prompt2 = convert_func(text2)
        mid.append(prompt2)

        line3 = all_lines.pop(0)
        text3 = " ".join(line3.split()[1:])
        prompt3 = convert_func(text3)
        low.append(prompt3)

        all_lines.pop(0)

    return high, mid, low