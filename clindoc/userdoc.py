
from typing import List
import re


class MissingSection(Exception):
    pass


class Decorator:
    def __init__(self) -> None:
        pass

    def get_decorator(self):
        return self.decorator

    def is_required(self):
        return self.required

    def is_done(self):
        return self.done

    def __call__(self, section):
        raise NotImplementedError

    def to_md(self):
        raise NotImplementedError


class UserDoc:
    def __init__(self, file: str) -> None:
        self. file = file
        self.decorators: List[Decorator] = self.init_decorators()
        self._order = ["@title", "@description", "@usage", "@example",
                       "@dependencies", "@background", "@dev", "@author"]

    def parse_documentation(self):
        # print(self.file)
        



        start = re.search('\%\*', self.file)
        re.purge()
        end = re.search('\*\%', self.file)
        section = self.file[start.regs[0][1]:end.regs[0][0]]
        ident = re.findall("@\w+", section.strip())

        for index, d in enumerate(ident):
            for dcls in self.decorators:
                if dcls.get_decorator() == d:
                    if index >= len(ident) - 1:
                        start = re.search(d, section)
                        dcls(section[start.regs[0][1]:])
                    else:
                        start = re.search(d, section)
                        end = re.search(ident[index+1], section)
                        if start and end:
                            dcls(section[start.regs[0][1]:end.regs[0][0]])
                            section = section[end.regs[0][0]:]

    def init_decorators(self) -> List[Decorator]:
        ret = []
        ret.append(Title())
        ret.append(Description())
        ret.append(Usage())
        ret.append(Example())
        ret.append(Dependencies())
        ret.append(Background())
        ret.append(Dev())
        ret.append(Author())
        return ret

    def check_requirements(self):
        for d in self.decorators:
            if d.is_required() and not d.is_done():
                raise MissingSection(f"Missing section {d.get_decorator()}")

    def _find_d(self, dec):
        for d in self.decorators:
            if d.get_decorator() == dec:
                return d

        return None

    def build_md(self):
        ret = ""
        for k in self._order:
            d = self._find_d(k)
            if d.is_done():
                ret += d.to_md()
                ret += "\n"
        return ret


class Title(Decorator):
    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@title"
        self.required = True
        self.done = False

    def __call__(self, section):
        self.section = section.strip()
        self.done = True

    def to_md(self):
        return f"# {self.section}"


class Description(Decorator):
    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@description"
        self.required = True
        self.done = False

    def __call__(self, section):
        self.section = section.strip()
        self.done = True

    def to_md(self):
        return f"## Description \n{self.section}"


class Usage(Decorator):

    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@usage"
        self.required = True
        self.done = False

    def __call__(self, section):
        self.section = section.strip()
        self.done = True

    def to_md(self):
        return f'## Usage \n```bash \n{self.section} \n```'


class Example(Decorator):

    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@example"
        self.required = True
        self.done = False

    def __call__(self, section):
        self.section = section.strip()
        self.done = True

    def to_md(self):
        return f"## Example  \n ```prolog\n{self.section}\n```"


class Dependencies(Decorator):

    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@dependencies"
        self.required = False
        self.done = False

    def __call__(self, section):
        self.section = section.strip()
        self.done = True

    def to_md(self):
        return f"## Dependencies \n{self.section}"


class Background(Decorator):
    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@background"
        self.required = False
        self.done = False

    def __call__(self, section):
        self.section = section.strip()
        self.done = True

    def to_md(self):
        return f"## Background \n{self.section}"


class Dev(Decorator):
    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@dev"
        self.required = True
        self.done = False

    def __call__(self, section):
        self.section = section.strip()
        self.done = True

    def to_md(self):
        return f"### Dev \n{self.section}"


class Author(Decorator):
    def __init__(self) -> None:
        super().__init__()
        self.decorator = "@author"
        self.required = True
        self.done = False
        self.section = ""

    def __call__(self, section):
        self.section += section.strip() + "\n"
        self.done = True

    def to_md(self):
        return f"##Author(s) \n{self.section}"
