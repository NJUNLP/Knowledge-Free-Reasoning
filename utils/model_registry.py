from collections import namedtuple

ModelDesc = namedtuple(
    'ModelDesc',
    ['path', 'default_template', 'prepend_metaspace', 'enable_flash_attn'],
    defaults=[None, None, None, True]
)

MODELS = {
    'llama-2-7b-chat': ModelDesc(
        path='meta-llama/Llama-2-7b-chat-hf',
        default_template='llama2',
        prepend_metaspace=True,
    ),
    'mistral-7b-instruct-v0.1': ModelDesc(
        path='mistralai/Mistral-7B-Instruct-v0.1',
        default_template='mistral',
        prepend_metaspace=True,
    ),
    'bloomz-7b1-mt': ModelDesc(
        path='bigscience/bloomz-7b1-mt',
        default_template='alpaca',
        prepend_metaspace=False,
        enable_flash_attn=False,
    ),
    'qwen1.5-7b-chat': ModelDesc(
        path='Qwen/Qwen1.5-7B-Chat',
        default_template='qwen',
        prepend_metaspace=False,
    ),
    
    'llama-2-7b-chat-arabic-lora': ModelDesc(
        path='merged_model/Icebear-AI_Llama-2-7b-chat-arabic-lora_merged',
        default_template='alpaca',
        prepend_metaspace=True,
    ),
    'sambalingo-arabic-base': ModelDesc(
        path='sambanovasystems/SambaLingo-Arabic-Base',
        default_template='sambalingo',
        prepend_metaspace=True,
    ),
    'sambalingo-arabic-chat': ModelDesc(
        path='sambanovasystems/SambaLingo-Arabic-Chat',
        default_template='sambalingo',
        prepend_metaspace=True,
    ),
    'dictalm-2': ModelDesc(
        path='dicta-il/dictalm2.0',
        default_template='dictalm2',
        prepend_metaspace=True,
    ),
    'dictalm-2-instruct': ModelDesc(
        path='dicta-il/dictalm2.0-instruct',
        default_template='dictalm2',
        prepend_metaspace=True,
    ),
}


def main():
    from sys import argv
    assert len(argv) == 3
    print(getattr(MODELS[argv[1]], argv[2]))


if __name__ == '__main__':
    main()
