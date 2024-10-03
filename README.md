# Large Language Models Are Cross-Lingual Knowledge-Free Reasoners

## Overview

This repository shares the code and data of our latest work [Large Language Models Are Cross-Lingual Knowledge-Free Reasoners](https://arxiv.org/abs/2406.16655).

In this work, we decompose the process of reasoning tasks into two separated parts: knowledge retrieval and knowledge-free reasoning, and analyze the cross-lingual transferability of them. With adapted and constructed knowledge-free reasoning datasets, we show that the knowledge-free reasoning capability can be nearly perfectly transferred across various source-target language directions despite the secondary impact of resource in some specific target languages, while cross-lingual knowledge retrieval significantly hinders the transfer. Moreover, by analyzing the hidden states and feed-forward network neuron activation during the reasoning tasks, we show that higher similarity of hidden representations and larger overlap of activated neurons could explain the better cross-lingual transferability of knowledge-free reasoning than knowledge retrieval. Thus, we hypothesize that knowledge-free reasoning embeds in some language-shared mechanism, while knowledge is stored separately in different languages. 

## Dataset
We provide our Syntactic Knowledge-Free Reasoning Dataset as described in the paper in this repository. Additionally, we also include other datasets we used, along with their respective training and test set splits.

All these datasets are stored in the `prepared_data` folder and are formatted according to the [LLaMA-Factory data format](https://github.com/hiyouga/LLaMA-Factory/blob/v0.8.2/data/README.md).

**DataGeneration**
------------------

This repository also provides tools for generating various reasoning datasets, including Arithmetic, Symbolic, and Logical reasoning tasks.

### Dataset Generation

* Use `./DataGeneration/genDataArithmeticAndSymbolic.py` to generate **Arithmetic** and **Symbolic reasoning** datasets.
* Use `./DataGeneration/genDataLogical.py` to generate **Logical reasoning** datasets.

The generated datasets will be located in `./DataGeneration/data`.

#### Customizing Dataset Sizes

You can modify the `TrainNum` and `TestNum` parameters in the respective scripts to adjust the number of training and test samples generated.

### Advanced Parameters

For more control over the dataset difficulty, you can adjust the following parameters in `./DataGeneration/dataTemplate.py`:

* **Arithmetic Reasoning Dataset:**
  * Modify `MAXNUM` to adjust the range of numbers used in arithmetic calculations (including the range of generated results).
* **Symbolic Reasoning Dataset:**
  * `STRLENMIN`: Set the minimum number of symbols to generate.
  * `STRLENMAX`: Set the maximum number of symbols to generate.
  * `SYMBOLICTURN`: Adjust the maximum number of turns for symbolic reasoning, where each turn generates the same number of cases.
* **Logical Reasoning Dataset:**
  * `CASENUM`: Adjust the number of propositions for logical reasoning cases.

## Model Evaluation

We leverage the [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) library for fine-tuning for all the experiments described in the paper.
You can use the following scripts to reproduce the cross-lingual transfer evaluation described in our paper, including training adapter and prediction.
Please run these scripts in the root directory of the repository.

```bash
pip install -r requirements.txt
python merge_lora.py
vim train.sh # Modify GPU config, if necessary
bash train.sh
bash predict_main.sh
```

After finishing the model prediction, you will get the prediction results in the `eval/outputs` directory.
Then, you can use the notebook `eval_analysis.ipynb` to reproduce the pictures described in our paper.

## Interpretability
The interpretability experiment results can be reproduced by running `./interpretability.py`. You can select different datasets through the `dataSetPath` parameter. The output includes overall statistics and results for the top ten samples displayed in the command line, visualizations of metrics for each layer, and detailed results for all cases saved in a JSON file. 

Other optional parameters, such as `cosFlag` for setting the metric and `threshold` for setting the activation threshold, can be found in the code.

## Citation
If you find this repository helpful, feel free to cite our paper.
```bibtex
@misc{hu2024large,
      title={Large Language Models Are Cross-Lingual Knowledge-Free Reasoners}, 
      author={Peng Hu and Sizhe Liu and Changjiang Gao and Xin Huang and Xue Han and Junlan Feng and Chao Deng and Shujian Huang},
      year={2024},
      eprint={2406.16655},
      archivePrefix={arXiv},
      primaryClass={id='cs.CL' full_name='Computation and Language' is_active=True alt_name='cmp-lg' in_archive='cs' is_general=False description='Covers natural language processing. Roughly includes material in ACM Subject Class I.2.7. Note that work on artificial languages (programming languages, logics, formal systems) that does not explicitly address natural-language issues broadly construed (natural-language processing, computational linguistics, speech, text retrieval, etc.) is not appropriate for this area.'}
}
```
