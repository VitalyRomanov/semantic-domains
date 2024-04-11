from dataclasses import field, dataclass, asdict
from typing import List


@dataclass
class WordUsageExample:
    text: str
    source: str = ""


@dataclass
class Word:
    text: str
    source: str = ""
    usage_examples: List[WordUsageExample] = field(default_factory=list)
    

@dataclass
class Question:
    num: int
    text: str
    words: List[Word]
    source: str = ""


@dataclass
class Domain:
    code: str
    title: str
    description: str
    questions: List[Question]
    source: str = ""
    subdomains: List["Domain"] = field(default_factory=list)

    def copy_replace(self, **kwargs):
        values = asdict(self)
        values.update(kwargs)
        return self.__class__(**values)
    

    def to_dict(self):
        return asdict(self)
