import os
import math
import hashlib
from abc import ABC, abstractmethod
from typing import List
from app.config import settings

class BaseEmbeddingProvider(ABC):
    @property
    @abstractmethod
    def dimension(self) -> int:
        pass

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass

class MockEmbeddingProvider(BaseEmbeddingProvider):
    """
    Deterministic pseudo-embedding provider for offline development and testing.
    Generates unit-normalized vector embeddings based on SHA-256 text hashing.
    """
    def __init__(self, target_dim: int = 384):
        self._dim = target_dim

    @property
    def dimension(self) -> int:
        return self._dim

    def embed_text(self, text: str) -> List[float]:
        if not text:
            text = "empty"
        vec = []
        for i in range(self._dim):
            h = hashlib.sha256(f"{text}:{i}".encode('utf-8')).hexdigest()
            # Convert hash slice to float between -1.0 and 1.0
            val = (int(h[:8], 16) / 0xffffffff) * 2.0 - 1.0
            vec.append(val)
        
        # Normalize vector to unit length
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """
    OpenAI Embedding Provider abstraction.
    """
    def __init__(self, model_name: str = "text-embedding-3-small", dim: int = 1536):
        self._model_name = model_name
        self._dim = dim
        self.api_key = os.getenv("OPENAI_API_KEY")

    @property
    def dimension(self) -> int:
        return self._dim

    def embed_text(self, text: str) -> List[float]:
        if not self.api_key or self.api_key == "mock_key":
            # Fallback to mock embedding if API key is missing
            return MockEmbeddingProvider(self._dim).embed_text(text)
        try:
            import httpx
            url = "https://api.openai.com/v1/embeddings"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {"input": text, "model": self._model_name}
            resp = httpx.post(url, json=payload, headers=headers, timeout=10.0)
            resp.raise_for_status()
            return resp.json()["data"][0]["embedding"]
        except Exception:
            return MockEmbeddingProvider(self._dim).embed_text(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

def get_embedding_provider() -> BaseEmbeddingProvider:
    provider_type = os.getenv("EMBEDDING_PROVIDER", settings.EMBEDDING_PROVIDER).lower()
    if provider_type == "openai":
        return OpenAIEmbeddingProvider()
    return MockEmbeddingProvider(target_dim=384)
