import subprocess
import os
import datetime

GIT_EXE = r"C:\Program Files\Git\cmd\git.exe"

def publish_to_github(repo_dir: str):
    """
    Commits and pushes updated briefing HTML files and index.html to GitHub.
    """
    if not os.path.exists(GIT_EXE):
        print("[-] Git executable not found. Skipping GitHub publish.")
        return False

    try:
        # Check if git is initialized
        if not os.path.exists(os.path.join(repo_dir, ".git")):
            print("[+] Initializing Git repository...")
            subprocess.run([GIT_EXE, "init"], cwd=repo_dir, check=True)
            subprocess.run([GIT_EXE, "config", "user.name", "meyrr007"], cwd=repo_dir, check=True)
            subprocess.run([GIT_EXE, "config", "user.email", "meyrr007@users.noreply.github.com"], cwd=repo_dir, check=True)
            subprocess.run([GIT_EXE, "branch", "-M", "main"], cwd=repo_dir, check=True)
            subprocess.run([GIT_EXE, "remote", "add", "origin", "https://github.com/meyrr007/daily-news-briefings.git"], cwd=repo_dir, check=True)
        else:
            # Ensure user info is configured
            subprocess.run([GIT_EXE, "config", "user.name", "meyrr007"], cwd=repo_dir)
            subprocess.run([GIT_EXE, "config", "user.email", "meyrr007@users.noreply.github.com"], cwd=repo_dir)

        # Git add, commit, push
        print("[+] Staging changes for GitHub...")
        subprocess.run([GIT_EXE, "add", "."], cwd=repo_dir, check=True)
        
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        commit_msg = f"Auto daily briefing update - {today_str}"
        
        subprocess.run([GIT_EXE, "commit", "-m", commit_msg], cwd=repo_dir, capture_output=True)
        
        print("[+] Pushing to GitHub repository...")
        res = subprocess.run([GIT_EXE, "push", "-u", "origin", "main"], cwd=repo_dir, capture_output=True, text=True)
        
        if res.returncode == 0:
            print("[+] Successfully published daily briefings to GitHub!")
            return True
        else:
            print(f"[!] Push status: {res.stdout.strip()} {res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[!] Error pushing to GitHub: {e}")
        return False
