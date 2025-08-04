import subprocess

def get_git_commit_count():
    try:
        count = subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).strip().decode()
        return int(count)
    except Exception:
        return 0

def get_version():
    major = 1  # Manually set as needed
    minor = 0
    patch = 0
    build = get_git_commit_count()  # Auto-build number from commits

    patch += build // 100
    build = build % 100
    return f"v{major}.{patch}.{build}-beta"

VERSION = get_version()
