import os
import __main__
import inspect
import json
from typing import Union

main_source = inspect.getsource(__main__)

base_path = './'

def save_json(data: Union[list, dict], name: str, split: str = 'eval'):
    output_dir = os.path.join(base_path, split, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, name)
    json.dump(data, open(output_path + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(output_path + '.py', 'w', encoding='utf-8').write(main_source)
