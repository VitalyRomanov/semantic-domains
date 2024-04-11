from copy import copy
from typing import List, Union

from definitions import Domain


class DomainNode:
    def __init__(self):
        self.subdomains = {}
        self.content = None

    def domain_code(self, code: str):
        return [int(part) for part in code.split(".")]

    def insert(self, domain, code_parts: List[int] = None):
        if code_parts is None:
            code_parts = self.domain_code(domain.code)
        
        if len(code_parts) == 0:
            assert self.content is None
            self.content = domain
        else:
            current_code, remaining = code_parts[0], code_parts[1:]
            if current_code not in self.subdomains:
                self.subdomains[current_code] = DomainNode()
            self.subdomains[current_code].insert(domain, remaining)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.content.title if self.content else None})"
    
    def traverse(self):
        for node in self.subdomains.values(): 
            yield node
            yield from node.traverse()

    def __getitem__(self, key: Union[str, list[int]]):
        if isinstance(key, str):
            key = self.domain_code(key)
        else:
            key = copy(key)
        
        if len(key) == 0:
            return self.content
        else:
            descend = key.pop(0)
            return self.subdomains[descend][key]
        

def assemble_hierarchy(domains: List[Domain]):
    root = DomainNode()
    
    for domain in domains:
        root.insert(domain)

    return root
