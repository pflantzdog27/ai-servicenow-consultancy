import os
from functools import lru_cache
from typing import Optional, List, Tuple

import numpy as np
from openai import OpenAI, OpenAIError


class SemanticCache:
    """Very small in-memory semantic cache using OpenAI embeddings."""

    def __init__(self, threshold: float = 0.9):
        self.threshold = threshold
        self._store: List[Tuple[np.ndarray, str]] = []
        api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=api_key) if api_key else None

    def _embed(self, text: str) -> Optional[np.ndarray]:
        if not self._client:
            return None
        resp = self._client.embeddings.create(
            model="text-embedding-3-small",
            input=[text]
        )
        return np.array(resp.data[0].embedding, dtype=float)

    def get(self, text: str) -> Optional[str]:
        if not self._store:
            return None
        vec = self._embed(text)
        if vec is None:
            return None
        best_score = 0.0
        best_val = None
        for emb, val in self._store:
            score = float(np.dot(vec, emb) / (np.linalg.norm(vec) * np.linalg.norm(emb)))
            if score > best_score:
                best_score = score
                best_val = val
        if best_score >= self.threshold:
            return best_val
        return None

    def set(self, text: str, value: str) -> None:
        vec = self._embed(text)
        if vec is None:
            return
        self._store.append((vec, value))


class AIGateway:
    """Simple gateway that routes requests to appropriate models."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)
        self.cache = SemanticCache()

    def _select_model(self, complexity: str) -> str:
        if complexity == "simple":
            return "gpt-3.5-turbo"
        if complexity == "advanced":
            return "gpt-4o"
        return "gpt-4-turbo"

    def generate_config(self, requirements: str, complexity: str = "medium") -> str:
        model = self._select_model(complexity)
        prompt = (
            "Generate ServiceNow configuration code from these requirements:\n" + requirements
        )
        cached = self.cache.get(f"{model}:{prompt}")
        if cached:
            return cached
        try:
            resp = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert ServiceNow developer."},
                    {"role": "user", "content": prompt},
                ],
            )
        except OpenAIError as exc:
            raise RuntimeError(f"Model call failed: {exc}")
        content = resp.choices[0].message.content
        self.cache.set(f"{model}:{prompt}", content)
        return content


_gateway: Optional[AIGateway] = None


def get_ai_gateway() -> AIGateway:
    global _gateway
    if _gateway is None:
        _gateway = AIGateway()
    return _gateway
