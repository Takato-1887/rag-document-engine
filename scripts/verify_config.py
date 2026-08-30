"""
Quick smoke test to confirm .env loads and validates correctly.
Run manually after any .env or config.py change: python scripts/verify_config.py
"""

from src.config import settings

if __name__ == "__main__":
    print("Config loaded successfully:\n")
    for key, value in settings.model_dump().items():
        print(f"  {key}: {value}")
