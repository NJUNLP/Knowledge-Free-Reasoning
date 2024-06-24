import json
from typing import Union
import torch
from tqdm import trange
from utils.save_output import save_json
from utils.model_registry import MODELS
import os
import re

model_name = os.environ.get('MODEL', 'mistral-7b-instruct-v0.1')
batch_size = int(os.environ.get('BATCH_SIZE', 1))

data_info_path = os.environ['DATA_INFO_PATH']

data_names = os.environ['DATA_NAME'].split()
allowed_tokens_data = os.environ.get('ALLOW_TOK', None)
if allowed_tokens_data is None:
    allowed_tokens_data = list('ABCD')
else:
    allowed_tokens_data = json.loads(allowed_tokens_data)
adapter_name = os.environ['ADAPTER']

template = MODELS[model_name].default_template

if adapter_name != 'none':
    adapter_base = os.environ['ADAPTER_BASE']
    
    join_model_name = f'{model_name}_{adapter_name}'
    adapter_path = f'{adapter_base}/{adapter_name}'
else:
    join_model_name = model_name
    adapter_path = None

model_dir = MODELS[model_name].path

import sys
sys.path.append('LLaMA-Factory/src')
from llmtuner import ChatModel
model = ChatModel({
    'model_name_or_path': model_dir,
    'adapter_name_or_path': adapter_path,
    'template': template,
    'max_new_tokens': 1,
    'do_sample': False,
    'flash_attn': torch.cuda.get_device_capability()[0] >= 8 and MODELS[model_name].enable_flash_attn,
})
    
def constrain_model(allowed_tokens):
    allowed_ids = model.engine.tokenizer.convert_tokens_to_ids(allowed_tokens)
    assert all(ids > 0 for ids in allowed_ids)
    print(f'{allowed_ids = }')
    from transformers.modeling_outputs import CausalLMOutputWithPast, CausalLMOutputWithCrossAttentions
    def choice_hook(
        model, args, output,
    ) -> Union[CausalLMOutputWithPast, CausalLMOutputWithCrossAttentions]:
        assert isinstance(output, Union[CausalLMOutputWithPast, CausalLMOutputWithCrossAttentions])
        logits = output.logits[:, -1:, :]
        tmp = torch.zeros_like(logits)
        tmp[:] = -float('inf')
        tmp[..., allowed_ids] = logits[..., allowed_ids]
        output.logits[:, -1:, :] = tmp
        return output
    model.engine.model.config.return_dict = True
    if hasattr(model.engine.model, 'choice_hook_handle'):
        model.engine.model.choice_hook_handle.remove()
    model.engine.model.choice_hook_handle = model.engine.model.register_forward_hook(choice_hook)


for data_name in data_names:
    if allowed_tokens_data is not None:
        allowed_tokens = allowed_tokens_data
        if isinstance(allowed_tokens, dict):
            lang = re.search(r'[A-Z]{2}', data_name).group(0).lower()
            allowed_tokens = allowed_tokens[lang]
        
        if adapter_name != 'none':
            assert MODELS[model_name].prepend_metaspace is not None
            if MODELS[model_name].prepend_metaspace:
                allowed_tokens = ['▁' + token for token in allowed_tokens]
        constrain_model(allowed_tokens)
    
    output_name = f'{data_name}_{join_model_name.replace("_", "-")}_{template.replace("_", "-")}'
    output_file = f'eval/outputs/{output_name}.json'

    print(f'{model_dir   = }')
    print(f'{output_name = }')
    print(f'{output_file = }')

    from utils.load_data import load_llama_factory_data
    testset = load_llama_factory_data(data_name)


    outputs = []
    correct_count = 0
    bar = trange(0, len(testset))
    for idx in bar:
        torch.cuda.empty_cache()
        example = testset[idx]
        messages = [
            {'role': 'user', 'content': example["instruction"] + '\n' + example["input"]}
        ]
        
        res = model.chat(messages)[0].response_text
        ans = res

        correct = ans == example['output']

        if correct:
            correct_count += 1

        if idx == 0 or os.environ.get('STEP_VERBOSE', False):
            print('--------')
            print(res)
            print(ans)
            print('--------')

        outputs.append((res, ans))
            
        bar.set_postfix({'Acc': correct_count / len(outputs) * 100})

    print(f'{len(testset) = }')
    print(f'{correct_count = }')
    print(f'accuracy = {correct_count / len(testset) * 100:.2f}%')
    save_json(outputs, output_name)
