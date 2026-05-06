import requests
from requests import RequestException
from config import get_settings

settings = get_settings()

class OllamaClient:
    """Client for interacting with a local Ollama server."""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def generate_completion(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            response = self.session.post(self._url("/v1/completions"), json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                if "completion" in data:
                    return data["completion"].strip()
                choices = data.get("choices")
                if isinstance(choices, list) and choices:
                    first_choice = choices[0]
                    if isinstance(first_choice, dict):
                        return (
                            first_choice.get("text")
                            or first_choice.get("message", {}).get("content", "")
                        ).strip()

            return str(data)
        except RequestException as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc
