import os

from clingo.ast import Location
from typing import Dict, List

def get_dir_filename(filename:str) -> str:
    """
    A helper function to get the absolute filename of a directory.

    :param filename: The filename of the directory.
    :return: The absolute filename of the directory.
    """
    
    return os.path.abspath(filename)


def create_dir(filename:str) -> None:
    """
    A helper function to create a directory if it does not exist.

    :param filename: The filename of the directory to create.
    :return: None
    """
    if not os.path.exists(filename):
        os.makedirs(filename)
         
def filename_from_source(source:str,filename:str)->str:
    """
    A helper function to get the relative filename of a file from a source folder.

    :param source: The source folder filename.
    :param filename: The filename of the file.
    :return: The relative filename of the file from the source folder.
    """
    return filename.replace(source+'/','')
    

def format_parameters(parameters:Dict):
    """
    A helper function to format parameters for using in the code.
    
    `format_parameters` takes a dictionary of parameters as input and returns a modified version of the dictionary with a nested structure.
    If a key contains a period, the key is split into parts using the period as a delimiter.
    These parts are then used to create a nested structure within the output dictionary.

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


def parse_content_from_location(file:List[str], location:Location) -> str:
    """
    A helper function to extract element of a file given a Location object.
    
    :param file: List of str representing a file
    :param location: location object to delimit the parsing
    :returns: a string corresponding at the extraction
    """
    
    if location.begin.line != location.end.line:
        parsed_list = file[location.begin.line:location.end.line]
        parsed_list[0] = parsed_list[0][location.begin.column:]
        parsed_list[-1] = parsed_list[-1][:location.end.column]
    else:
        parsed_list = [file[location.begin.line]]
        parsed_list[0] = parsed_list[0][location.begin.column:location.end.column]
        
    
    ret = ""
    for l in parsed_list:
        ret += l
    
    return ret
    