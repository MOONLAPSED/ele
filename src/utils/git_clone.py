import subprocess
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class GitModuleManager:
    def find_gitmodules_path(self) -> str:
        """
        Finds the path of the .gitmodules file.

        Returns:
            str: The path of the .gitmodules file.
        """
        gitmodules_path = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip() + '/.gitmodules'
        print("gitmodules_path:", gitmodules_path)  # Debug-style print
        return gitmodules_path

    def readgitmodules(self, gitmodules_path: str) -> Tuple[str, List[str]]:
        """
        Reads the .gitmodules file and extracts the repository URLs.

        Args:
            gitmodules_path (str): The path of the .gitmodules file.

        Returns:
            Tuple[str, List[str]]: A tuple containing the gitmodules_path and a list of repository URLs.
        """
        # Read the .gitmodules file
        with open(gitmodules_path, 'r') as file:
            gitmodules_content = file.read()

        # Extract the repository URLs from the .gitmodules file
        repo_urls = [line.split('\t')[1].strip() for line in gitmodules_content.split('\n') if line.startswith('url = ')]
        for i, line in enumerate(gitmodules_content.split('\n')):
            if line.startswith('[submodule "'):
                path_line = gitmodules_content.split('\n')[i+1]
                url_line = gitmodules_content.split('\n')[i+2]
                url = url_line.split('=')[1].strip()
                repo_urls.append(url)

        # Clone the repositories
        for repo_url in repo_urls:
            subprocess.run(['git', 'clone', repo_url])

        return gitmodules_path, repo_urls

    def clone_gitmodules(self):
        """
        Clones the repositories specified in the .gitmodules file.
        """
        # Invoke the find_gitmodules_path() method
        gitmodules_path = self.find_gitmodules_path()

        # Invoke the readgitmodules(gitmodules_path) method
        gitmodules_path, repo_urls = self.readgitmodules(gitmodules_path)
        print("Repository URLs:")
        for url in repo_urls:
            print(url)
    
    def clone_repositories(self, repo_urls: List[str], target_dir: str):
        """
        Clones the repositories specified in the repo_urls list into the target directory.

        Args:
            repo_urls (List[str]): A list of repository URLs to clone.
            target_dir (str): The target directory to clone the repositories into.
        """
        for repo_url in repo_urls:
            subprocess.run(['git', 'clone', repo_url, target_dir])


if __name__ == '__main__':
    # Create an instance of the GitModuleManager class
    git_manager = GitModuleManager()

    # Specify the repository URLs to clone
    repo_urls = [
        'https://github.com/MOONLAPSED/cognos.git',
        # 'https://github.com/user/repo2.git',
        # 'https://github.com/user/repo3.git'
    ]

    # Invoke the clone_repositories() method with the repo_urls list
    git_manager.clone_repositories(repo_urls)

    # Create an instance of the GitModuleManager class
    git_manager = GitModuleManager()

    # Invoke the clone_repositories() method
    git_manager.clone_repositories()
