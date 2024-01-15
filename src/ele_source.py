#!/usr/bin/env python
# init and re-init module and source all the files in the src folder
import subprocess
import json
import sys

def normpath(value):
    """
    Convert string to absolute normpath.

    @param value: some string to be converted
    @type value: str

    @return: absolute normpath
    @rtype: str

    Example:

    ```
    user_home_directory = "~/Documents"
    expanded_path = os.path.expanduser(user_home_directory)
    print(expanded_path)
    ```

    Output:

    ```
    /home/user/Documents
    ```

    """
    if not isinstance(value, str):
        raise TypeError('Input must be a string')

    head, tail = os.path.split(value)

    if not head and not os.path.isfile(value):
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, tail)
            if os.path.isfile(exe_file):
                value = exe_file
                break
        else:
            raise FileNotFoundError('File not found in any directories in PATH')

    value = os.path.expanduser(value)
    value = os.path.normpath(value)

    return value

def main():
    """
    Main function.

    @return: None
    @rtype: NoneType
    """
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Launch a python script")
    parser.add_argument("script", help="script to be launched")
    parser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    script = normpath(args.script)  # The provided script path is normalized using the normpath function. Normalization resolves redundant separators and up-level references (e.g., "../"), producing a canonicalized absolute pathname.

    if not os.path.isfile(script):
        raise FileNotFoundError("File not found")

    logging.debug("script: %s", script)

    sys.path.insert(0, os.path.dirname(script))  # Adds the directory containing the specified script to the beginning of the Python path (sys.path). 

    if os.path.splitext(script)[1] == ".py":
        import importlib.util
        spec = importlib.util.spec_from_file_location("__main__", script)  # If the file type is .py, it uses importlib to load and execute the script as the __main__ module.
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        raise NotImplementedError("File type not supported")
