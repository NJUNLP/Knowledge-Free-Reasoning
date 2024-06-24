import os
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
import matplotlib.pyplot as plt
import json
import random
import torch.nn.functional as F
import matplotlib.pyplot as plt
import math
import peft
from peft import PeftModel,LoraModel,PeftModelForCausalLM
from interpretabilityTool import decodeALL,plotLayer,dataSetPathMap
import numpy as np
import argparse
import re

parser = argparse.ArgumentParser(description="Llama Activation Analysis")
parser.add_argument('--loraPath', type=str, default=None,help='Path to the Lora model')
parser.add_argument('--CosFlag', type=bool, default=False, help='Flag to calculate cosine similarity or activation overlap')
parser.add_argument('--meanStep', type=int, default=10, help='Step size for averaging')
parser.add_argument('--threshold', type=float, default=0.4, help='Threshold for activation')
parser.add_argument('--modelPath', type=str, default="meta-llama/Llama-2-7b-chat-hf", help='Llama-2-7b-chat-hf model path')
parser.add_argument('--outPath', type=str, default="test.json", help='Results for different confidence intervals, The summation will be output on the command line, and the results of the different layers will be output as images')
parser.add_argument('--dataSetPath', type=str, default="ambig", help='Select the dataset to use, optionally mkqa, ambig, boolq, arithmetic, logical, symbolic')


args = parser.parse_args()

# Getting command line arguments
loraPath = args.loraPath
CosFlag = args.CosFlag
meanStep = args.meanStep
threshold = args.threshold
modelPath = args.modelPath
outPath = args.outPath
dataSetPath = dataSetPathMap[args.dataSetPath]
lange=["de", "fr", "en","it", "ru", "pl", "ar", "he", "zh", "ja"] 


# Storing the output of each layer
layer_activations = {}

# Defining Hooks
def get_activation(layer_name: str):
    def hook(model, input, output):
        layer_activations[layer_name] = output[0][-1].detach()
    return hook

def get_cos(layer_name):
    def hook(model, input, output):
        layer_activations[layer_name] = output[0][0][-1].detach()
    return hook

# Apply the hook function to the specified position, the position is selected depending on the model used.
def getAct():
    for name, layer in model.named_modules():
        if "act_fn" in name:
            layer.register_forward_hook(get_activation(name))

pattern = re.compile(r'^model\.layers\.\d+$')
def getHidden():
    for name, layer in model.named_modules():        
        if pattern.match(name):
            layer.register_forward_hook(get_cos(name))



def cosine_similarity_activations(activations):
    # Calculate the cosine similarity of each layer
    similarities = {}
    for loci in range(len(activations)):
        for layer_name, base_activation in activations[loci].items():
            sim_scores = []
            for locj in range(len(activations)):
                if loci==locj:
                    continue
                sim_score = F.cosine_similarity(base_activation, activations[locj][layer_name], dim=0)
                sim_scores.append(sim_score.mean().item()) 
            if layer_name not in similarities:
                similarities[layer_name] = [sum(sim_scores)/len(sim_scores)]
            else:
                similarities[layer_name].append(sum(sim_scores)/len(sim_scores))

    for layer_name in similarities.keys():
        similarities[layer_name]=sum(similarities[layer_name])/len(similarities[layer_name])

    return similarities.values(),sum(similarities.values())/len(similarities.values())

def analyze_inputs_cos(inputs, model, tokenizer):
    activations_per_input = []
    # Getting Hidden Layer Representations for Different Languages
    for input in inputs:
        layer_activations.clear()
        input_tensor = tokenizer(input, return_tensors="pt").to(device)
        with torch.no_grad():
            model(**input_tensor) 
        
        current_activations = {name:activation for name, activation in layer_activations.items()}
        activations_per_input.append(current_activations)
    
    # Calculate the cosine similarity of hidden layer representations in different languages
    if len(inputs) > 1:
        return cosine_similarity_activations(activations_per_input)
    return {}

def analyze_inputs(inputs):
    activations_per_input = []
    # Acquisition of activated neurons for different language samples
    for input in inputs:
        layer_activations.clear() 
        input_tensor = tokenizer(input, return_tensors="pt").to(device)
        with torch.no_grad():
            model(**input_tensor) 
        current_activations = {}
        for name, activation in layer_activations.items():
            abs_activation = torch.abs(activation)
            current_activations[name] = (abs_activation > threshold).to('cpu') 

        activations_per_input.append(current_activations)

    # Analysing overlaps
    overlap_count = {}
    total_count = {}
    avg_activated_count = {}
    for layer_name in activations_per_input[0].keys():
        all_positions = [activations[layer_name] for activations in activations_per_input]
        overlap = torch.stack(all_positions).sum(dim=0) == len(inputs)  # Calculate the position that is active in all inputs
        overlap_count[layer_name] = overlap.sum().item()
        total_count[layer_name] = all_positions[0].numel()
        #  Calculate the average total number of activations per layer across all inputs
        activated_counts = [pos.sum().item() for pos in all_positions] 
        avg_activated_count[layer_name] = sum(activated_counts)/len(activated_counts) 

    overlap_ratios = [
        overlap_count[layer_name] / avg_activated_count[layer_name] if avg_activated_count[layer_name] > 0 else 0 
        for layer_name in overlap_count
    ]
    
    avg_overlap_ratio = sum(overlap_ratios) / len(overlap_ratios)
    
    # Total overlap rate and overlap rate per layer
    return overlap_ratios, avg_overlap_ratio

# Calculate the results for the entire dataset and save and sum the results
def analyze_inputs_for_languages(language_data, model, tokenizer,dataSetName="test"):
    sumrate=0
    SumLayerRate=[]

    if os.path.exists(outPath):
        with open(outPath, "r") as f:
            resultALL = json.load(f)
    else:
        resultALL={}
    if CosFlag:
        resultALL[dataSetName]={"layer":[],"rate":[]}
    else:
        if resultALL.get(dataSetName) is None:
            resultALL[dataSetName]={}
        resultALL[dataSetName][threshold]={"layer":[],"rate":[]}


    print("\n\n\nruning:"+dataSetName)

    for loc in range(len(language_data['en'])):
        inputs = [language_data[lang][loc] for lang in language_data]
        if CosFlag:
            layer_rate, rate = analyze_inputs_cos(inputs, model, tokenizer)
        else:
            layer_rate, rate = analyze_inputs(inputs)

        if loc==0:
            SumLayerRate=layer_rate
        else:
            SumLayerRate = [i + j for i, j in zip(SumLayerRate, layer_rate)]

        if loc<10:
            print(f"Location {loc},Average rate: {rate:.3f}")

        sumrate+=rate
        if CosFlag:
            resultALL[dataSetName]["layer"].append(list(layer_rate))
            resultALL[dataSetName]["rate"].append(rate)
        else:
            resultALL[dataSetName][threshold]["layer"].append(list(layer_rate))
            resultALL[dataSetName][threshold]["rate"].append(rate)

        if loc % meanStep==meanStep-1:
            if CosFlag:
                outStr="Overlap:" + "{:.3f}".format(sumrate / meanStep) +" "+dataSetName+" threshold: "+str(threshold)+"\n"
            else:
                outStr="Cos:" + "{:.3f}".format(sumrate / meanStep) +" "+ dataSetName+ "\n"
            meanSumLayerRate = [x / meanStep for x in SumLayerRate]
            plotLayer(meanSumLayerRate,dataSetName)
            print(outStr)
            break
    with open(outPath, "w") as f:
        json.dump(resultALL, f)



model = LlamaForCausalLM.from_pretrained(modelPath)
tokenizer = LlamaTokenizer.from_pretrained(modelPath)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device}")
if loraPath is not None:
    peft_model = PeftModelForCausalLM.from_pretrained(model, loraPath)
    model = peft_model.merge_and_unload(progressbar=True, safe_merge=True)
model=model.to(device)
model.eval()
if CosFlag:
    getHidden()
else:
    getAct()
language_data = decodeALL(lange,dataSetPath)

analyze_inputs_for_languages(language_data, model, tokenizer,dataSetName=dataSetPath.split("/")[-1])