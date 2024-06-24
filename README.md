# Large Language Models Are Cross-Lingual Knowledge-Free Reasoners

## Overview

This repository shares the code and data of our latest work "Large Language Models Are Cross-Lingual Knowledge-Free Reasoners".

In this work, we decompose the process of reasoning tasks into two separated parts: knowledge retrieval and knowledge-free reasoning, and analyze the cross-lingual transferability of them. With adapted and constructed knowledge-free reasoning datasets, we show that the knowledge-free reasoning capability can be nearly perfectly transferred across various source-target language directions despite the secondary impact of resource in some specific target languages, while cross-lingual knowledge retrieval significantly hinders the transfer. Moreover, by analyzing the hidden states and feed-forward network neuron activation during the reasoning tasks, we show that higher similarity of hidden representations and larger overlap of activated neurons could explain the better cross-lingual transferability of knowledge-free reasoning than knowledge retrieval. Thus, we hypothesize that knowledge-free reasoning embeds in some language-shared mechanism, while knowledge is stored separately in different languages. 

## Dataset
We provide our Syntactic Knowledge-Free Reasoning Dataset as described in the paper in this repository. Additionally, we also include other datasets we used, along with their respective training and test set splits.

All these datasets are stored in the `prepared_data` folder and are formatted according to the LLaMA-Factory data format.

## Model Evaluation

We leverage the LLaMA-Factory factory for fine-tuning for all the experiments described in the paper.
You can use the following scripts to reproduce the cross-lingual transfer evaluation described in our paper, including training adapter and prediction.
Please run these scripts in the root directory of the repository.

```bash
pip install -f requirements.txt
python merge_lora.py
vim train.sh # Modify GPU config, if necessary
bash train.sh
bash predict_main.sh
```

After finishing the model prediction, you will get the prediction results int the `eval/outputs` directory.
Then, you can use the notebook `eval_analysis.ipynb` to reproduce the pictures described in our paper.

## Interpretability
The interpretability experiment results can be reproduced by running `./interpretability.py`. You can select different datasets through the `dataSetPath` parameter. The output includes overall statistics and results for the top ten samples displayed in the command line, visualizations of metrics for each layer, and detailed results for all cases saved in a JSON file. 

Other optional parameters, such as `cosFlag` for setting the metric and `threshold` for setting the activation threshold, can be found in the code.

## Citation
If you find this repository helpful, feel free to cite our paper. The following citation information is obtained from Google Scholar. 
```bibtex
Stay tuned
```
