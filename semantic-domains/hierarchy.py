from copy import copy
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

from definitions import Domain, Question


class DomainNode:
    subdomains: Dict[int, 'DomainNode']
    content: Optional[Domain]
    parent: "DomainNode"

    def __init__(self, parent=None):
        self.subdomains = {}
        self.content = None
        self.parent = parent

    def domain_code(self, code: str) -> List[int]:
        return [int(part) for part in code.split(".")]

    def insert(self, domain: Domain, code_parts: List[int] = None) -> None:
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
    
    def __iter__(self) -> Iterable["DomainNode"]:
        return self.traverse(return_domain=False)
    
    def iterate_domains(self) -> Iterable[Domain]:
        return self.traverse(return_domain=True)
    
    def traverse(self, max_depth: int = 5, return_domain: bool = False) -> Iterable["DomainNode"]:
        for node in self.subdomains.values(): 
            yield node.content if return_domain else node
            if max_depth > 0:
                yield from node.traverse(max_depth=max_depth - 1)

    def get_content_property(self, prop: str) -> Union[str, None]:
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
            return self.content
        else:
            descend = key.pop(0)
            return self.subdomains[descend][key]
        

def assemble_hierarchy(domains: List[Domain]) -> DomainNode:
    root = DomainNode()
    
    for domain in domains:
        root.insert(domain)

    return root


def read_domains_from_json(json_path: Union[str, Path], as_hierarchy: bool = False) -> Union[List[Domain], DomainNode]:
    with open(json_path, "r") as f:
        data = json.load(f)
    domains = [Domain.from_dict(domain) for domain in data["domains"]]
    if as_hierarchy:
        return assemble_hierarchy(domains)
    return domains
