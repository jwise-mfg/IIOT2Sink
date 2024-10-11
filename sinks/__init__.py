import os
import traceback
from importlib import util
from abc import ABC, abstractmethod
# Adapted from: https://gist.github.com/dorneanu/cce1cd6711969d581873a88e0257e312

class sinkadapters:
    # Base sink adapter resource class. Concrete resources will inherit from this one
    sinks = []

    # For every class that inherits from the current, and has an init
    # the class name will be added to sink adapters
    def __init_subclass__(cls, **kwargs):
        if "__init__" in str(cls):
            super().__init_subclass__(**kwargs)
            cls.sinks.append(cls)

    # Define the interface for an adapter
    @abstractmethod
    def start():
        pass

    @abstractmethod
    def write(timestamp, value, sinkparam, subscription):
        pass

# Load adapters

# Get current path
path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

# Module Loader
def load_module(path):
    spec = util.spec_from_file_location("__init__.py", path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Loop through each subfolder and try to load if it looks like a real adapter and has a config
for fname in os.listdir(dirpath):
    sinkpath = os.path.join(dirpath, fname)
    if os.path.isdir(sinkpath) and "__init__.py" in os.listdir(sinkpath) and "config.py" in os.listdir(sinkpath):
        try:
            module = load_module(os.path.join(sinkpath, "__init__.py"))
        except Exception:
            traceback.print_exc()