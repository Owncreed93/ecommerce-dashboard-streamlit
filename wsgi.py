"""WSGI configuration for deployment.

This module provides a template for deploying the application on platforms
like PythonAnywhere or other WSGI-compliant servers.
Note: For Streamlit, use the streamlit command directly.
"""

import os
import sys

# Path to the project root
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(os.path.join(path, "src"))

# Example for a Flask/FastAPI adapter (placeholder)
# from infrastructure.web.app import app as application
