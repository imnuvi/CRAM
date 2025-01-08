from .parser import FileParser
from .writer import FileWriter
from importlib.metadata import version

__all__ = ['FileParser', 'FileWriter']
__version__ = version(__name__) 
