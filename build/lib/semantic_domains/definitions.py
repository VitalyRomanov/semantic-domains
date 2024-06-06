from dataclasses import dataclass, asdict
from typing import List


class SemanticDomainObject:
    @classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)
    
    def to_dict(self, excluded_fields=None):
        dict_ = asdict(self)

        if excluded_fields is None:
            excluded_fields = []

        for field_name in list(dict_.keys()):
            if field_name in excluded_fields:
                dict_.pop(field_name)
        
        return dict_
    
    def copy_replace(self, **kwargs):
        values = asdict(self)
        values.update(kwargs)
        return self.__class__(**values)
    

@dataclass
class Question(SemanticDomainObject):
    num: int
    text: str
    words: List[str]


@dataclass
class Domain(SemanticDomainObject):
    code: str
    title: str
    description: str
    questions: List[Question]

    @classmethod
    def from_dict(cls, kwargs):
        kwargs["questions"] = [Question.from_dict(q) for q in kwargs["questions"]]
        return cls(**kwargs)
