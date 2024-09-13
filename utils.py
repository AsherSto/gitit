import subprocess

def change_directory(repo_name):
    target_directory = os.path.join("repos", repo_name)
    if not os.path.exists(target_directory):
        raise FileNotFoundError(f"The directory {target_directory} does not exist.")
    os.chdir(target_directory)

def spinupdockercontainer():
    subprocess.run(["docker", "run", "-it", "--rm", "-v", f"{os.getcwd()}:/workspace", "codercom/code-server"])

def spin_up_vscode(github_link, branch="main", docker=False):
    if not os.path.exists("repos"):
        os.makedirs("repos")
    subprocess.run(["git", "clone", "-b", branch, github_link, "repos/" + os.path.basename(github_link.rstrip(".git"))])

    repo_name = os.path.basename(github_link.rstrip(".git"))

    try:
        change_directory(repo_name)
    except FileNotFoundError as e:
        print(e)
        return

    # Detect the languages of the files inside the repository
    try:
        languages = detect_languages()
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
    if docker == False:
        for language, _ in languages:
            if language in extensions:
                for extension in extensions[language]:
                    subprocess.run(["code", "--install-extension", extension])

        subprocess.run(["code", "."])
    else:
        spinupdockercontainer()
        for language, _ in languages:
            if language in extensions:
                for extension in extensions[language]:
                    subprocess.run(["docker", "exec", "code-server", "code-server", "--install-extension", extension])
                    

        

import os

def detect_languages():
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

    detected_languages = sorted(language_count.items(), key=lambda item: item[1], reverse=True)
    print(f"Detected languages: {detected_languages}")
    return detected_languages
