import sys
import os
from unittest.mock import MagicMock

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock streamlit before importing app
st_mock = MagicMock()
st_mock.secrets = {"OPENROUTER_API_KEY": "fake_key"}
# Ensure st.button returns False so main logic doesn't run on import
st_mock.button.return_value = False
sys.modules["streamlit"] = st_mock
