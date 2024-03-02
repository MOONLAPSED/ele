import sys
import subprocess

from main import run as main_run, lager as main_lager  # Import the run function and lager from main.py
from setup import main

app = main()  # Use the pydantic app from setup.py
lager = main_lager  # Use the lager from main.py

@app.on_event("startup")
def run():
    try:
        pass
    except:
        pass
    finally:
        pass

@app.on_event("shutdown")
def stop():
    try:
        pass
    except:
        pass
    finally:
        pass

if __name__ == "__main__":
    main_run()  # Call the run function from main.py
