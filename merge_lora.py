from peft import PeftModelForCausalLM, LoraModel
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel
from utils.model_registry import MODELS

def main():
    base_path = MODELS['llama-2-7b-chat'].path
    lora_path = 'Icebear-AI/Llama-2-7b-chat-arabic-lora'
    output_path = MODELS['llama-2-7b-chat-arabic-lora'].path
    
    tokenizer = AutoTokenizer.from_pretrained(base_path)
    base_model: PreTrainedModel = AutoModelForCausalLM.from_pretrained(
        base_path, device_map='auto', low_cpu_mem_usage=True, torch_dtype='auto',
    )
    
    peft_model: LoraModel = PeftModelForCausalLM.from_pretrained(
        base_model,
        lora_path,
    )
    
    merged_model: PreTrainedModel = peft_model.merge_and_unload(
        progressbar=True, safe_merge=True
    )
    
    merged_model.save_pretrained(
        output_path,
        max_shard_size='1GiB',
        save_peft_format=False,
    )
    tokenizer.save_pretrained(output_path)


if __name__ == '__main__':
    main()
