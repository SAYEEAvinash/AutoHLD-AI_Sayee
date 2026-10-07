from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class DocumentChunk:
    chunk_id: str
    page: int
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Entity:
    name: str
    entity_type: str
    page: int
    evidence: str

@dataclass
class Relationship:
    source: str
    relation: str
    target: str
    page: int
    evidence: str
