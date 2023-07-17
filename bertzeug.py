from fitbert import FitBert

def convert_for_bert(text):
    text = text.replace("YYYY", "XXX")
    text = text.replace("__", "***mask***")
    list = text.split("XXX")
    for i in range(len(list)):
        list[i] = list[i].strip()
    prompt = list[0]
    options = list[1:]
    return prompt, options

def fitbert_ranking(sentence, alternatives, model):
    return model.rank(sentence, options=alternatives, with_prob=True)

fb = FitBert()

counts = [0,0] # [lower_count, higher_count], assuming that the lower comes first in the exercise
for p in range(1): # because there were 90 participants; in the original study, participants were treated separately
    for tq in low:
        result = fitbert_ranking(tq[0], tq[1], fb)
        print(result[0][0])
        print(tq[1][1])
        if result[0][0] == tq[1][0].strip(): # das besser oben implementieren
            counts[0]+=1
        elif result[0][0] == tq[1][1].strip():
            counts[1]+=1
