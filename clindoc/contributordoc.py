from .astprogram import ASTProgram, ASTLineType, Symbol, ASTLine, ASTType
from typing import List, Dict


class DifferentLengthBetweenPropertiesAndNames(Exception):
    pass


class MDHelper:
    def str_symbols_signature(define: List[Symbol]):
        define = set([d.get_signature() for d in define])
        ret = ""
        for d in define:
            ret += d + ' '

        ret = ret[:-1]
        return ret

    def str_symbols(define: List[Symbol]):
        ret = ""
        for d in define:
            ret += d.name + ' '

        ret = ret[:-1]
        return ret


class MDMaker:
    def __init__(self, data: List[ASTLine], title: str, description: str, table: Dict, img: Dict = None, ) -> None:
        self.data = data
        self.title = title
        self.description = description
        self.table = table
        self.img = img

    def _create_table(self):

        if len(self.table['column_names']) != len(self.table['properties']):
            raise DifferentLengthBetweenPropertiesAndNames(
                f"Error while generating tables, size of names and properties are different: {len(self.table['column_names'])} != {len(self.table['properties'])}")

        ret = '\n|'
        mem = '|'
        for col_name in self.table['column_names']:
            ret += f" **{col_name.capitalize()}** |"
            mem += f"---{len(col_name)*'-'}---|"

        ret += '\n' + mem + '\n'

        for d in self.data:
            ret +='|'
            for prop in self.table['properties']:
                ret += f" {prop(d)} |"
            ret += '\n'

        return ret

    def generate_markdown(self):
        ret = ""

        if self.title:
            ret += f"## {self.title}\n"

        if self.description:
            ret += f"{self.description}\n"

        if self.table:
            ret += self._create_table()

        if self.img:
            ret += f"![{self.img.title}({self.img.path})]"

        return ret +"\n"

    def factory(pool: Dict):
        ret = []
        
        for key in pool:
            if key == ASTLineType.Rule:
                column_name = ['Signature', 'Depends', 'Location', 'Doc']
                properties = [
                    lambda al: MDHelper.str_symbols_signature(al.define),
                    lambda al: MDHelper.str_symbols_signature(al.dependencies),
                    lambda al: f"Line; {al.ast.location.begin.line}",
                    lambda al: al.comments
                ]
                ret.append(MDMaker(pool[key], 'Rules', 'Showing all rules', {
                           'column_names': column_name, 'properties': properties}))

            elif key == ASTLineType.Fact:
                column_name = ['Signature',  'Location', 'Doc']
                properties = [
                    lambda al: MDHelper.str_symbols_signature(al.define),
                    lambda al: f"Line; {al.ast.location.begin.line}",
                    lambda al: al.comments
                ]
                ret.append(MDMaker(pool[key], 'Facts', 'Showing all facts', {
                           'column_names': column_name, 'properties': properties}))

            elif key == ASTLineType.Constraint:
                column_name = ['Signature','Dependencies',  'Location', 'Doc']
                properties = [
                    lambda al: f"constraint#{al.id}",
                    lambda al: MDHelper.str_symbols_signature(al.dependencies),
                    lambda al: f"Line; {al.ast.location.begin.line}",
                    lambda al: al.comments
                ]
                ret.append(MDMaker(pool[key], 'Constraints', 'Showing all constraints ', {
                           'column_names': column_name, 'properties': properties}))

            elif key == ASTLineType.Input:
                column_name = ['Signature',  'Location', 'Doc']
                properties = [
                    lambda al: f"{al.ast.name}/{al.ast.arity}",
                    lambda al: f"Line; {al.ast.location.begin.line}",
                    lambda al: al.comments
                ]
                ret.append(MDMaker(pool[key], 'Inputs', 'Showing all inputs ', {
                           'column_names': column_name, 'properties': properties}))
            elif key == ASTLineType.Output:
                column_name = ['Signature',  'Location', 'Doc']
                properties = [
                    lambda al: al.get_output_signature(),
                    lambda al: f"Line; {al.ast.location.begin.line}",
                    lambda al: al.comments
                ]
                ret.append(MDMaker(pool[key], 'Outputs', 'Showing all outputs ', {
                           'column_names': column_name, 'properties': properties}))

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
        print(ref_pool)
        mds = MDMaker.factory(ref_pool)

        for md in mds:
            ret += md.generate_markdown()

        return ret
