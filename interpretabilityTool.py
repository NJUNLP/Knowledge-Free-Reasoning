
import os,json,random
import matplotlib.pyplot as plt
import random
import seaborn as sns
import numpy as np

random.seed(0)

dataSetPathMap={"mkqa":"prepared_data/mkqa/mkqa-dev-first-1000/mkqa-test_{}.json","ambig":"prepared_data/ambig_qa/ambig-qa-validation-first-100/ambig-qa-validation-first-100_{}.json","boolq":"prepared_data/boolq/boolq-dev-first-100/boolq-dev-first-100_{}.json","arithmetic":"prepared_data/kfrd_arithmetic/Arithmetic{}_test.json","logical":"prepared_data/kfrd_logical/Logical{}_test.json","symbolic":"prepared_data/kfrd_symbolic/Symbolic{}_test.json"}

language_question_marks = {
    "de": "?",  # German
    "fr": "?",  # French
    "it": "?",  # Italian
    "ru": "?",  # Russian
    "pl": "?",  # Polish
    "ar": "؟",  # Arabic
    "he": "?",  # Hebrew
    "zh": "？",  # Chinese
    "ja": "？",  # Japanese
    "en": "?"   # English
}

questionContext = {
    "de": "\nWelche Option sollte ich wählen?",  # Which option should I choose? (German)
    "fr": "\nQuelle option devrais-je choisir ?",  # Which option should I choose? (French)
    "en": "\nWhich option should I choose?",  # Which option should I choose? (English)
    "it": "\nQuale opzione dovrei scegliere?",  # Which option should I choose? (Italian)
    "ru": "\nКакой вариант мне выбрать?",  # Which option should I choose? (Russian)
    "pl": "\nKtórą opcję powinienem wybrać?",  # Which option should I choose? (Polish)
    "ar": "\nأي خيار يجب أن أختار؟",  # Which option should I choose? (Arabic)
    "he": "\nאיזו אפשרות עליי לבחור?",  # Which option should I choose? (Hebrew)
    "zh": "\n请问我该选哪个选项？",  # Which option should I choose? (Chinese)
    "ja": "\nどのオプションを選べばいいですか？"  # Which option should I choose? (Japanese)
}


# Plotting results for each layer
def plotLayer(layerResult, dataSetName="test.png"):
    plotPath=dataSetName+".png"
    plt.figure(figsize=(12, 6))
    layer = range(len(layerResult))
        
    plt.plot(layer, layerResult, label=dataSetName)
    plt.xlabel('Layer Index')
    plt.ylabel('Ratio')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plotPath)


def decodeKFRD(lange,dataPath):
    language_data={}
    for lang in lange:
        tpath=dataPath.format(lang.upper())
        language_data[lang] = []
        with open(tpath, "r", encoding="utf-8") as f:
                datas =json.load(f)
                for data in datas:
                    # Put a question mark on all the topics
                    question = data["prompt"]+data["query"]+questionContext[lang]
                    language_data[lang].append(question)
    return language_data

def decodeKRD(lange,dataPath):
    language_data={}
    for lang in lange:
        language_data[lang] = []
        with open(dataPath.format(lang), "r", encoding="utf-8") as f:
            data=json.load(f)
            for line in data:
                if "mkqa" in dataPath:
                    result=line['input']
                else:
                    result=line['question']
                # If there is no question mark, add a question mark
                if result[-1]!=language_question_marks[lang]:
                    result+=language_question_marks[lang]
                language_data[lang].append(result)
    return language_data

def decodeALL(lange,dataPath,dataFlag=None):
    random.seed(0)
    if "boolq" in dataPath or "ambig" in dataPath or "mkqa" in dataPath:
        langeData = decodeKRD(lange,dataPath)
    else:
        langeData = decodeKFRD(lange,dataPath)
        randomIndex = random.sample(range(len(langeData['en'])), len(langeData['en']))
        for key in langeData.keys():
            langeData[key] = [langeData[key][i] for i in randomIndex]

    return langeData

