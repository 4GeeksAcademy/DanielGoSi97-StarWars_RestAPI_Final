import sys
import os

# Esto añade la carpeta src al camino de búsqueda de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app

if __name__ == "__main__":
    app.run()