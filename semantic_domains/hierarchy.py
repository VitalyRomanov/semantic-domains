from copy import copy
import json
from pathlib import Path
from typing import Dict, Generator, List, Optional, Type, Union

from semantic_domains.definitions import Domain, Question
from semantic_domains.rwc_parser import DomainType


class DomainNode:
    subdomains: Dict[int, 'DomainNode']
    content: Optional[Domain]
    parent: Optional["DomainNode"]

    def __init__(self, parent: Optional["DomainNode"] = None):
        self.subdomains = {}
        self.content = None
        self.parent = parent

    def domain_code(self, code: str) -> List[int]:
        return [int(part) for part in code.split(".")]

    def insert(self, domain: Domain, code_parts: Optional[List[int]] = None) -> None:
        if code_parts is None:
            code_parts = self.domain_code(domain.code)
        
        if len(code_parts) == 0:
            assert self.content is None
            self.content = domain
        else:
            current_code, remaining = code_parts[0], code_parts[1:]
            if current_code not in self.subdomains:
                self.subdomains[current_code] = DomainNode(parent=self)
            self.subdomains[current_code].insert(domain, remaining)

    def __repr__(self) -> str:
        parts = []
        parent_ref = self
        while parent_ref is not None and  parent_ref.content is not None:
            parts.insert(0, parent_ref.content.title)
            parent_ref = parent_ref.parent
        path = "  /  ".join(str(part) for part in parts)
        return f"{self.__class__.__name__}({path if self.content else None})"
    
    def __iter__(self):
        for node in self.traverse(max_depth=10):
            if node.content is not None:
                yield node.content
        return map(
            lambda domain_node: domain_node.content, 
            (node for node in self.traverse(max_depth=10) if node.content is not None)
        )
    
    def iterate_domains(self):
        return self.traverse(max_depth=10)  # 10 is greater than maximum depth
    
    def traverse(self, max_depth: int = 5) -> Generator["DomainNode", None, None]:
        for node in self.subdomains.values(): 
            yield node
            if max_depth > 0:
                yield from node.traverse(max_depth=max_depth - 1)

    def get_content_property(self, prop: str) -> str:
        if self.content is not None:
            return getattr(self.content, prop)
        else:
            return str(None)

    @property
    def code(self) -> str:
        return self.get_content_property("code")
    
    @property
    def title(self) -> str:
        return self.get_content_property("title")
        
    @property
    def description(self) -> str:
        return self.get_content_property("description")
        
    @property
    def questions(self) -> List[Question]:
        if self.content is not None:
            return self.content.questions
        else:
            return []

    def __getitem__(self, key: Union[str, list[int]]) -> Domain:
        """
        Get Domain using domain code.
        """
        if isinstance(key, str):
            key = self.domain_code(key)
        else:
            key = copy(key)
        
        if len(key) == 0:
            content = self.content
            assert content is not None
            return content
        else:
            descend = key.pop(0)
            content = self.subdomains[descend][key]
            return content
        

def assemble_hierarchy(domains: List[DomainType]) -> DomainNode:
    root = DomainNode()
    
    for domain in domains:
        root.insert(domain)

    return root


def read_domains_from_json(json_path: Union[str, Path], alternative_domain_class: Optional[Type[DomainType]] = None) -> List[DomainType]:
    with open(json_path, "r") as f:
        data = json.load(f)

    if alternative_domain_class is None:
        domain_class = Domain
    else:
        domain_class = alternative_domain_class

    domains = [domain_class.from_dict(domain) for domain in data["domains"]]
    return domains  # type: ignore[return-value]


def read_domain_hierarchy(json_path: Union[str, Path], as_hierarchy: bool = False, alternative_domain_class: Optional[Type[DomainType]] = None) -> DomainNode:
    domains = read_domains_from_json(json_path, alternative_domain_class=alternative_domain_class)
    return assemble_hierarchy(domains)
    