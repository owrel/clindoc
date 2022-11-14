from .astprogram import ASTProgram
from typing import List, Dict


class MDMaker:
    def __init__(self,data, title: str, description: str, table: Dict, img: Dict = None, ) -> None:
        self.data = data
        self.title = title
        self.description = description
        self.table = table
        self.img = img

    def _create_table(self):
        ret = '|'
        mem = '|'
        for col_name in self.table['column_name']:
            ret += f" **{col_name.capitalize()}** |"
            mem += f"-{len(col_name)*'-'}-|"
        ret = ret[:-1]
        mem = mem[:-1]
        ret += '\n' + mem + '\n'


        for d in self.data:
            for property in self.table['property']:
                ret += f" {eval(f'd.{property}')} |"
            ret = ret[:-1] + '\n'
        
        return ret


    def generate_markdown(self):
        ret = f"## {self.title}\n"
        ret += f"{self.description}\n"
        if self.table:
            ret += self._create_table()
        
        if self.img:
            ret += f"![{self.img.title}({self.img.path})]"

        return ret




class ContributorDoc:
    def __init__(self, file: List[str], astprogram: ASTProgram) -> None:
        self.file = file
        self.astprogram = astprogram

    def build_doc(self) -> str:
        ret = ""
        ref_pool = {}
        for rule in self.astprogram.astlines:
            if rule.type in ref_pool:
                ref_pool[rule.type].append(rule)
            else:
                ref_pool[rule.type] = [rule]

        return ret

    
