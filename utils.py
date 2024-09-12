import os
import subprocess

import os
import subprocess

def spin_up_vscode(github_link, branch="main"):
    subprocess.run(["git", "clone", "-b", branch, github_link])

    repo_name = os.path.basename(github_link.rstrip(".git"))

    os.chdir(repo_name)

    try:
        language = detect_language()
    except ValueError as e:
        print(e)
        return

    extensions = {
        "Python": ["ms-python.python", "ms-toolsai.jupyter", "ms-python.vscode-pylance", "ms-toolsai.jupyter-keymap", "ms-toolsai.jupyter-renderers", "ms-toolsai.jupyter-renderers-vscode"],
        "JavaScript": ["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"],
        "HTML": ["ritwickdey.liveserver", "formulahendry.auto-close-tag"],
        "Java": ["redhat.java", "vscjava.vscode-java-pack"],
        "C++": ["ms-vscode.cpptools", "twxs.cmake"],
        "C": ["ms-vscode.cpptools", "twxs.cmake"],
        # Add more languages and their extensions as needed
    }

    if language in extensions:
        for extension in extensions[language]:
            subprocess.run(["code", "--install-extension", extension])

    subprocess.run(["code", "."])

import os

def detect_language():
    language_extensions = {
        'Python': ['.py'],
        'JavaScript': ['.js'],
        'HTML': ['.html'],
        'Java': ['.java'],
        'C++': ['.cpp', '.h'],
        'C': ['.c'],
        'C#': ['.cs'],
        'Rust': ['.rs'],
        'Go': ['.go'],
        'Ruby': ['.rb'],
        # Add more languages and their extensions as needed
    }

    language_count = {}
    for root, dirs, files in os.walk("."):
        for file in files:
            extension = os.path.splitext(file)[1]
            for language, extensions in language_extensions.items():
                if extension in extensions:
                    language_count[language] = language_count.get(language, 0) + 1

    if not language_count:
        raise ValueError("No languages detected in the repository")

    detected_language = max(language_count, key=language_count.get)
    return detected_language
