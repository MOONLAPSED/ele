from pydantic import BaseModel, Field, validator
from dataclasses import dataclass, field
import os
import subprocess
from src.lager import Lager  # capital "L"
import sys
import uuid

app = None  # Use the pydantic app from main
lager = None  # Use the lager from main


def hash():
    """hash retrieves the Git hash of the current commit and generates a random UUID for metadata."""
    try:
        uid = uuid.uuid4()  # Generate a random UUID variable for versioning and seeding
        git_hash = subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"]).decode().strip()
        return uid, git_hash

    except subprocess.CalledProcessError as e:
        if "fatal: not a git repository" in e.output.decode():
            lager.warning("No Git repository found. Skipping Git info.")
            return None
        else:
            raise  # Re-raise other Git errors for debugging


def runtime():
    """runtime sets the environment variables and runs the application."""
    global app, lager
    lager = Lager()
    lager.Lager.validate()  # Update and validate configuration

    try:
        # Validate and retrieve a branch logger for main.py
        ml = lager.Lager.branch_logger('main') # Retrieve a branch logger for main.py
        globals()['ml'] = ml  # Store in globals()
        return ml
    except:
        lager.Lager.error("Failed to retrieve Lager() branch.")
        pass
    finally:
        ml.info("passing lager object to main()")
        pass
    return ml

def main():
    """main is the entry point for the application."""
    global app, ml
    try:
        ml = runtime()
    except:
        print("Failed to retrieve Lager() branch.")
        sys.exit(1)
    finally:
        ml.info("passing lager object to main()")
    return ml


if __name__ == "__main__":
    try:
        main()
        ml.info("main achieved runtime")
    except ImportError:
        print("src not found, try reinstalling the package or running the setup.py script")
        sys.exit(1)
    except Exception as e:
        print(e)
        raise  # Re-raise the exception to halt execution
    finally:
        try:  # UFO and lit-llm git clone
            subprocess.run('git submodule init')
            subprocess.run('git submodule update --recursive')
        except Exception as e:
            print(e)
            pass
        sys.exit(0)
else:
    print("You have no src directory so please run /ele/setup.py directly")
    sys.exit(1)


