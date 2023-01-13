import os

from typing import Dict 

def get_dir_path(path) -> str:
    if not os.path.exists(path):
        raise ValueError(f"{path} does not exist.")
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a directory.")
    
    return os.path.abspath(path)


def create_dir(path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
         
def path_from_source(source,path):
    return path.replace(source+'/','')
    

def format_parameters(parameters:Dict):
    ret = {}
    for key in parameters.keys():
        if '.' in key:
            splitted_part  = key.split('.')
            level = ret
            while splitted_part:
                current_key = splitted_part.pop(0)
                if splitted_part:
                    if not current_key in level:
                        level[current_key] = {}
                    level = level[current_key]
                else:
                    level[current_key] = parameters[key]
        else:
            if not key in ret:
                ret[key] = parameters[key]
            else:
                raise ValueError(f'{key} parameter found two time')

    return ret

        