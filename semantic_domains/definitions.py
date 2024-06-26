from dataclasses import dataclass, asdict
from typing import List, Dict, Callable


@dataclass
class SemanticDomainObject:
    @classmethod
    def get_field_parsing_exceptions(cls) -> Dict[str, Callable]:
        return {}

    @classmethod
    def from_dict(cls, kwargs):
        for field, transform in cls.get_field_parsing_exceptions().items():
            kwargs[field] = transform(kwargs[field])
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
    def get_field_parsing_exceptions(cls) -> Dict[str, Callable]:
        return {
            "questions": lambda questions: [Question.from_dict(q) for q in questions]
        }
