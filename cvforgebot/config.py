from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REDIS_DSN = os.getenv("REDIS_DSN", "redis://localhost:6379/0")

# LaTeX related settings
LATEX_OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"

# Create necessary directories if they don't exist
os.makedirs(LATEX_OUTPUT_DIR, exist_ok=True)