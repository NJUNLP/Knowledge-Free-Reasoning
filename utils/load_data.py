import json
from pathlib import Path


def load_llama_factory_data(
    data_name: str,
    data_info_path: str = 'prepared_data/dataset_info.json'
) -> list[dict[str, object]]:
    data_info_path: Path = Path(data_info_path)
    MAPPING = {
        'prompt': 'instruction',
        'query': 'input',
        'response': 'output',
    }
    dataset_info = json.load(open(data_info_path))[data_name]
    
    dataset = json.load(open(data_info_path.parent / dataset_info['file_name']))
    if 'columns' in dataset_info:
        for example in dataset:
            for k, v in dataset_info['columns'].items():
                if v != '':
                    example[MAPPING[k]] = example[v]
    return dataset
