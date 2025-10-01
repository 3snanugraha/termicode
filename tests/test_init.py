"""Test initialization"""
from dotenv import load_dotenv
import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load env
load_dotenv()

print(f"HF_TOKEN loaded: {'Yes' if os.environ.get('HF_TOKEN') else 'No'}")

# Test AI Client
try:
    from src.ai_client import AIClient
    client = AIClient()
    print("[OK] AIClient initialized")
except Exception as e:
    print(f"[ERROR] AIClient error: {e}")
    import traceback
    traceback.print_exc()

# Test Assistant
try:
    from src.assistant import CodingAssistant
    assistant = CodingAssistant()
    print("[OK] CodingAssistant initialized")
except Exception as e:
    print(f"[ERROR] CodingAssistant error: {e}")
    import traceback
    traceback.print_exc()
