from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, GPT2LMHeadModel, GPT2Tokenizer
import pandas as pd
from postprocessing import extract_number


def generate(prompt, model, tokenizer):
    # if model == "T5":
    #     model = model_T5
    #     tokenizer = tokenizer_T5
    # else:
    #     model = model_GPT2
    #     tokenizer = tokenizer_GPT2
    # encode context the generation is conditioned on
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    # get output with standard parameters
    sample_output = model.generate(
        input_ids,        # context to continue
        do_sample=True,   # use sampling (not beam search (see below))
        # return maximally 50 words (including the input given)
        max_length=500,
        top_k=0,          # just sample one word
        top_p=1,          # consider all options
        temperature=0.7,   # soft-max temperature
        # output_scores=True
    )
    return tokenizer.decode(sample_output[0], skip_special_tokens=True)


def get_response(model, tokenizer, n_repetitions, prompts, condition='both sentences'):
    '''Reports the prompt, response and response classifiction (into low, high, both, neither) of the model for N trials
    :param condition:
    :param prompts:
    :param tokenizer:
    :param n_repetitions: number of participatants i.e. number of repeats for model
    :param model: LLM model to use
    :output: dataframe with results
    '''
    results = pd.DataFrame(columns=["Condition", "Prompt", "Response"])

    for i in range(n_repetitions):

        for p in prompts:

            response = generate(p, model, tokenizer)
            row = {"Condition": condition, "Prompt": p, "Response": response}
            print(p)
            results = pd.concat([results, pd.DataFrame([row])], ignore_index=True)
            print(response)

    return results

def get_counts(model, tokenizer, n_repetitions, condition1prompts, condition2prompts):
    """Counts the numbers in the model response.
    :param model: LLM model to use
    :param tokenizer: llm tokenizer to use
    :param n_repetitions: number of participants i.e. number of repeats for model
    :param condition1prompts: dataset with e.g. think sentences
    :param condition2prompts: dataset with e.g. announced sentences

    :output: condition1_counts and condition2_counts, in the format [counts of both numbers in answer, counts of low
    number, counts of high, counts of neither]
    """
    condition1_counts = [0, 0, 0, 0]
    condition2_counts = [0, 0, 0, 0]

    for p in range(n_repetitions):  # Number of participants in the "think" condition
        for tq in condition1prompts:
            response = generate(tq, model, tokenizer)
            result = extract_number(tq, response)
            if result == "both":
                condition1_counts[0] += 1
            elif result == "low":
                condition1_counts[1] += 1
            elif result == "high":
                condition1_counts[2] += 1
            else:
                condition1_counts[3] += 1

    for p in range(n_repetitions):  # Number of participants in the "announce" condition
        for aq in condition2prompts:
            response = generate(aq, model, tokenizer)
            result = extract_number(aq, response)
            if result == "both":
                condition2_counts[0] += 1
            elif result == "low":
                condition2_counts[1] += 1
            elif result == "high":
                condition2_counts[2] += 1
            else:
                condition2_counts[3] += 1

    return condition1_counts, condition2_counts