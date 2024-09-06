import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 🌐 Smoobu API Configuration
API_BASE_URL = os.getenv("SMOOBU_API_BASE_URL", "https://login.smoobu.com/api")
API_KEY = os.getenv("SMOOBU_API_KEY")

# ⏱️ Caching and Rate Limiting Configuration
CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", 300))  # 5 minutes default
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 5))  # 5 requests per second default

# 💡 Note: Ensure that sensitive information like API_KEY is not committed to version control.
#    Consider using a separate .env file for local development and secure environment variables for production.
