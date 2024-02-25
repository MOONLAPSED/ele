# ele/__init__.py
from .src.lager import Lager

def entry_point():
    # ... 
    lager = Lager()
    globals()['lager'] = lager  # Store in globals()
    return lager 
