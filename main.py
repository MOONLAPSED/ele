# assume setup.py is in the same directory as src and src/__init__.py
# assume setup.py has invoked ele/src/lager.py and cognic/src/__init__.py
# assume setup.py has invoked ele/main.py (this script)
import sys
import os
import time
import subprocess
from src.lager import run

def runtime():
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"]).decode().strip()
        git_tag = subprocess.check_output(["git", "describe", "--tags", "--exact-match", git_hash, "2>/dev/null"]).decode().strip()
        print(f"git_hash: {git_hash} | git_tag: {git_tag}")
        return git_hash, git_tag

    except subprocess.CalledProcessError as e:
        if "fatal: not a git repository" in e.output.decode():
            print("No Git repository detected in this directory.")
            return None, None  # Return None to indicate absence of Git info
        else:
            raise  # Re-raise other Git errors for debugging

def main():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # is there adequate permission to expand the path?
    except Exception as e:
        print(e)
    finally:
        sys.path.extend([
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
            os.path.abspath(os.path.dirname(__file__))
        ])
        # ... pre-git initialization
        return 0

if __name__ == "__main__":
    try:
        root = None
        branch = None

        rt = runtime()
        if rt is not None:  # Check if Git info was retrieved
            git_hash, git_tag = rt
        else:
            git_hash, git_tag = None, None

        if rt is None:
            if input("No Git repository found. Initialize a new one? (y/n): ").lower() == 'y':
                # ... Git initialization code ... 
                branch.info(f"|{branch}-__main__-|")
            else:
                print("Git initialization skipped")
        
        # ...
        main()
        root, branch = run()
        # ...
            # ...
                # ...
    except ImportError:
        print("src not found, try reinstalling the package or running the setup.py script")
        sys.exit(1)
    except Exception as e:
        print(e)
    finally:
        # ...
        if rt is None:
            stdout=subprocess.PIPE
            stderr=subprocess.PIPE
            if "fatal: not a git repository" in stdout or "fatal: not a git repository" in stderr:
                print("fatal: not a git repository, now is your chance to ctrl+c because Ima chargin mah lazor!")
                # git init functionality
                subprocess.run("git init", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run("git add .", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run("git commit -m 'initial commit'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run("git tag", "v0.0.1", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # ...
                print("last chance to ctrl+c"); time.sleep(1)
                print("git init, commit, tag complete... Ima firin mah lazor!")
                # git push functionality -- this is dangerous code I need to heavily test: TODO
            # subprocess.run("git remote add origin https://github.com/MOONLAPSED/ele.git", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # subprocess.run("git push -u origin master", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            else: # this is the default case
                # async.wait loop for runtime's return value
                # ...                
                pass
    # ...
    sys.exit(0)
else:
    print("You have no src directory so please run /ele/setup.py directly")
    sys.exit(1)