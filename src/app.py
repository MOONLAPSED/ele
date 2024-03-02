import sys
import subprocess

from main import run as main_run, lager as main_lager  # Import the run function and lager from main.py
from setup import main
from pydantic import BaseModel, Field, validator

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


# +--------------------+

@dataclass
class SetupConfig:
    project_root: str
    log_dir: str
    log_file: str
    sts: frozenset  




class BasedModel(BaseModel):
    required_date: date = Field(default_factory=datetime.now().date)
    required_int: int = Field(0, ge=0)  # Set default value here
    state: int = Field(0)  # New field to hold the state value
    def __init__(self):
        super().__init__()
        try:
            self.required_int = int(os.getenv("REQUIRED_INT", default=0))
            self.state = int(os.getenv("STATE", default=0))  # Load 'state' from .env file
            self.required_date = datetime.now().date()
        except Exception as e:
            if e.__traceback__:
                __log_error(f"Error initializing BasedModel: {e}", exc_info=True)
                raise  # Re-raise the exception to halt execution
            else:
                __log_error(f"Error initializing BasedModel: {e}")
                raise  # Re-raise the exception to halt execution
        finally:  # default path with no exceptions
            try:
                # Call other methods or classes to get the required values
                project_root, log_dir, log_file, sts = __mainpath()
                appsettings = BasedModel()
                appsettings.project_root = project_root
                appsettings.log_dir = log_dir
                appsettings.log_file = log_file
                appsettings.sts = sts
                
            except Exception as e:
                if e.__traceback__:
                    __log_error(f"Error initializing BasedModel: {e}", exc_info=True)
                    raise  # Re-raise the exception to halt execution
                else:
                    __log_error(f"Error initializing BasedModel: {e}")
                    raise  # Re-raise the exception to halt execution


def ValidateAppsettings(appsettings):
    """Validate the appsettings"""
    try:
        project_root, log_file, log_dir, sts = appsettings

        if not os.path.exists(project_root):
            raise ValueError(f"Project root {project_root} does not exist")

        # Additional validation logic for other fields if needed

        return True  # Return True if all validations pass

    except Exception as e:
        __log_error(f"Error validating appsettings: {e}")
        return False  # Return False if any validation fails

def BasedSettings() -> tuple:
    appsettings = main()  # wrapper for app / main()
    if ValidateAppsettings(appsettings):  # wrapper for validate_appsettings()
        print("Appsettings are valid")
        based_model = BasedModel()
        based_model.project_root = appsettings.project_root
        based_model.log_dir = appsettings.log_dir
        based_model.log_file = appsettings.log_file
        based_model.sts = appsettings.sts
        return based_model, appsettings

def BasedApp():
    BasedSettings()
    based_app = BasedSettings()[0]
    if based_app.project_root == BasedSettings()[1].project_root:
        return based_app
    else:
        return 1





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
