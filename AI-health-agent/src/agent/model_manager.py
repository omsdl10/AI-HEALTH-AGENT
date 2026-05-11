import groq
import streamlit as st
from enum import Enum
import logging
import time

logger = logging.getLogger(__name__)

class ModelTier(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary" 
    TERTIARY = "tertiary"
    FALLBACK = "fallback"

class ModelManager:
    """
    Manages AI model selection, fallback, and rate limits.
    Implements an agent-based approach for model management.
    """
    
    MODEL_CONFIG = {
        ModelTier.PRIMARY: {
            "provider": "groq",
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        ModelTier.SECONDARY: {
            "provider": "groq", 
            "model": "llama-3.1-8b-instant",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        ModelTier.TERTIARY: {
            "provider": "groq",
            "model": "openai/gpt-oss-120b",
            "max_tokens": 2000, 
            "temperature": 0.7
        },
        ModelTier.FALLBACK: {
            "provider": "groq",
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 2000,
            "temperature": 0.7
        }
    }
    
    def __init__(self):
        self.clients = {}
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize API clients for each provider."""
        try:
            api_key = st.secrets.get("GROQ_API_KEY", "")
            if not api_key:
                self.clients["groq_error"] = (
                    "GROQ_API_KEY is missing. Add it to .streamlit/secrets.toml, "
                    "then restart the app."
                )
                return
            self.clients["groq"] = groq.Groq(api_key=api_key)
        except Exception as e:
            self.clients["groq_error"] = (
                "Could not initialize Groq. Check .streamlit/secrets.toml and "
                f"restart the app. Details: {str(e)}"
            )
            logger.error(self.clients["groq_error"])

    def generate_analysis(self, data, system_prompt, retry_count=0):
        """
        Generate analysis using the best available model with automatic fallback.
        Implements agent-based decision making for model selection.
        """
        if "groq" not in self.clients:
            return {
                "success": False,
                "error": self.clients.get(
                    "groq_error",
                    "Groq is not configured. Add GROQ_API_KEY to .streamlit/secrets.toml.",
                ),
            }

        failures = []
        tiers = [
            ModelTier.PRIMARY,
            ModelTier.SECONDARY,
            ModelTier.TERTIARY,
            ModelTier.FALLBACK,
        ]

        for tier in tiers:
            result = self._try_model(data, system_prompt, tier)
            if result["success"]:
                return result
            failures.append(result["error"])

        return {
            "success": False,
            "error": "Analysis failed. " + " | ".join(failures[-3:]),
        }

    def _try_model(self, data, system_prompt, tier):
        """Try one configured model and return its result without recursive retries."""
        model_config = self.MODEL_CONFIG[tier]
        provider = model_config["provider"]
        model = model_config["model"]
            
        try:
            client = self.clients[provider]
            logger.info(f"Attempting generation with {provider} model: {model}")
            
            if provider == "groq":
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": str(data)}
                    ],
                    temperature=model_config["temperature"],
                    max_tokens=model_config["max_tokens"]
                )
                
                return {
                    "success": True,
                    "content": completion.choices[0].message.content,
                    "model_used": f"{provider}/{model}"
                }
                
        except Exception as e:
            error_message = str(e)
            logger.warning(f"Model {model} failed: {error_message}")
            
            # Check for rate limit errors
            if "rate limit" in error_message.lower() or "quota" in error_message.lower():
                # Wait briefly before retrying with a different model
                time.sleep(2)
            
            return {
                "success": False,
                "error": f"{model}: {error_message[:180]}",
            }
            
        return {"success": False, "error": f"{model}: no response returned"}
