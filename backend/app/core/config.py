import os

class Settings:
    EPHE_PATH: str = os.getenv("EPHE_PATH", "/app/ephe")

    # Optional AI
    HF_ENDPOINT_URL: str = os.getenv("HF_ENDPOINT_URL", "").strip()
    HF_TOKEN: str = os.getenv("HF_TOKEN", "").strip()
    HF_MODEL_NAME: str = os.getenv("HF_MODEL_NAME", "AstroMLab/AstroSage-8B")

settings = Settings()