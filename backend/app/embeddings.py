"""Embedding provider contracts and test-friendly implementations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class EmbeddingProvider(ABC):
    """Interface for generating embeddings from ordered text inputs."""

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text."""


@dataclass(slots=True, frozen=True)
class FakeEmbeddingProvider(EmbeddingProvider):
    """Deterministic provider for tests and local wiring."""

    dimensions: int = 4

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if self.dimensions <= 0:
            raise ValueError("dimensions must be > 0")

        return [_embed_text_deterministically(text, dimensions=self.dimensions) for text in texts]


def _embed_text_deterministically(text: str, *, dimensions: int) -> list[float]:
    """Map text into a simple deterministic vector without external dependencies."""

    vector = [0.0] * dimensions
    for index, character in enumerate(text):
        slot = index % dimensions
        vector[slot] += float(ord(character))

    return vector
