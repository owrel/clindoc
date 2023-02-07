from __future__ import annotations
from clingo.ast import Location, Position
from typing import List

from .utils import parse_content_from_location


class Comment:
    def __init__(self, location:Location, large_comment:bool, content:str) -> None:
        self.location = location
        self.large_comment = large_comment
        self.content = content

    @classmethod
    def extract_comments(cls, file:List[str], filename=str) -> List[Comment]:
        in_comment = False 
        comments = []
        begin = None
        for idx_row,line in enumerate(file):
            for idx_column, char in enumerate(line):
                
                if char == "%" and not in_comment:
                    begin = Position(filename,idx_row,idx_column+1)
                    if idx_column < len(line) and line[idx_column+1] == '*':
                        in_comment = True
                    else:
                        location = Location(begin,Position(filename,idx_row,len(line)))
                        content = parse_content_from_location(file,location)
                        comments.append(Comment(location,False,content))
                        
                if char == '*' and in_comment:
                    if idx_column < len(line) and line[idx_column+1] == '%':
                        in_comment = False
                        
                        location = Location(begin,Position(filename,idx_row,idx_column-1))
                        content = parse_content_from_location(file,location)
                        comments.append(Comment(location, True, content))
                          
        return comments
    
    
    def __repr__(self) -> str:
        return self.content