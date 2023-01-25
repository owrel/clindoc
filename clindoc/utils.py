import os

from typing import Dict 

def get_dir_path(path:str) -> str:
    """
    A helper function to get the absolute path of a directory.

    :param path: The path of the directory.
    :return: The absolute path of the directory.
    :raises ValueError: If the path is not a valid directory or does not exist.
    """
    if not os.path.exists(path):
        raise ValueError(f"{path} does not exist.")
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a directory.")
    
    return os.path.abspath(path)


def create_dir(path:str) -> None:
    """
    A helper function to create a directory if it does not exist.

    :param path: The path of the directory to create.
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path)
         
def path_from_source(source:str,path:str)->str:
    """
    A helper function to get the relative path of a file from a source folder.

    :param source: The source folder path.
    :param path: The path of the file.
    :return: The relative path of the file from the source folder.
    """
    return path.replace(source+'/','')
    

def format_parameters(parameters:Dict):
    """
    A helper function to format parameters for using in the code.
    
    `format_parameters` takes a dictionary of parameters as input and returns a modified version of the dictionary with a nested structure.
    If a key contains a period, the key is split into parts using the period as a delimiter. These parts are then used to create a nested structure within the output dictionary.

    :param parameters: The parameters to format.
    :return: The formatted parameters.
    :raises ValueError: If a parameter is found two times.
    """
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