<div align="center">

<img src="https://raw.githubusercontent.com/Shineii86/GitUnzip/main/images/GitUnzip.png" width="200px" alt="GitUnzip">

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shineii86/GitUnzip/blob/main/notebooks/GitUnzip.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/GitUnzip?style=for-the-badge)](https://github.com/Shineii86/GitUnzip/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/GitUnzip?style=for-the-badge)](https://github.com/Shineii86/GitUnzip/fork)

**Upload a zip file from your phone, unzip it, and push the entire codebase to GitHub — all from Google Colab. No PC required.**

</div>

---

> ℹ️ **ABOUT THIS TOOL**
> - This notebook solves a common mobile limitation: GitHub's mobile app and website don't allow uploading folders or unzipping files.
> - Upload a zip file from your phone's storage, and this tool extracts it and pushes all contents to a GitHub repository.
> - You need a **GitHub Personal Access Token (classic)** with `repo` scope.
> - The target repository must already exist (create it first on GitHub).

---

## 🎯 What is This Tool?

**Mobile Zip to GitHub** bridges the gap between mobile file management and GitHub. If you've ever tried to upload a project folder from your phone to GitHub, you know it's impossible—the mobile interface only allows uploading individual files, not folders, and certainly doesn't unzip archives.

This tool lets you:
- **Upload a zip file** directly from your phone's storage.
- **Automatically unzip** it in the cloud.
- **Push the entire folder structure** to a GitHub repository.

Perfect for:
- Backing up code written on mobile IDEs.
- Sharing projects when you're away from your computer.
- Quickly pushing downloaded templates or starter kits to GitHub.

---

## ✨ Features

| Feature                      | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 📱 **Mobile‑Friendly**        | Upload zip directly from phone storage via Colab's file picker.             |
| 📂 **Preserves Structure**    | Maintains full folder hierarchy when unzipping and pushing.                 |
| 🌿 **Safe Branching**         | Option to create a new branch instead of overwriting existing code.         |
| 🔒 **Secure Authentication**  | Uses GitHub Personal Access Token — no password stored.                     |
| 🧹 **Automatic Cleanup**      | Temporary files are deleted after push.                                     |
| ⏰ **No Local Setup**          | Runs entirely in Google Colab's cloud environment.                          |

---

## 🛠️ Prerequisites

1. **A GitHub account**.
2. **A target repository** (must already exist on GitHub).
3. **A Personal Access Token (classic)** with `repo` scope.

### 🔑 How to Get a Personal Access Token

1. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
2. Click **Generate new token (classic)**.
3. Check the **`repo`** scope (this grants full control of private repositories).
4. Generate and **copy the token immediately** — you won't see it again.

> 🔒 **Security Note:** Treat this token like a password. Never commit it or share it publicly.

### 📁 Preparing Your Zip File

- Use any file manager app on your phone to zip a folder.
- Ensure the zip contains the files/folders you want to push to GitHub.
- The zip can contain nested folders — the structure will be preserved.

---

## 🚀 Quick Start

1. **Click the "Open in Colab" badge** above.
2. **Enter your GitHub username and token** in the configuration form.
3. **Specify the target repository name** (must already exist).
4. **Run the first cell** to install dependencies.
5. **Run the second cell** — it will prompt you to upload a zip file.
6. **Select your zip file** from your phone's storage.
7. **Wait for the process to complete** — you'll see a success message with a link to your repo.

---

## ⚙️ Configuration Options

| Parameter | Description | Example Value |
|-----------|-------------|---------------|
| `GITHUB_USERNAME` | Your GitHub username. | `"Shineii86"` |
| `GITHUB_TOKEN` | Personal Access Token (classic) with `repo` scope. | `"ghp_abc123..."` |
| `REPO_NAME` | Target repository name (must exist). | `"my-uploaded-code"` |
| `BRANCH` | Branch to push to (default: `main`). | `"main"` or `"develop"` |
| `COMMIT_MESSAGE` | Commit message for this upload. | `"📱 Upload code from mobile via Colab"` |
| `OVERWRITE_BRANCH` | If `True`, force‑push to the branch. If `False`, creates a new timestamped branch. | `True` |
| `TARGET_SUBDIR` | Subdirectory within repo to place files (leave blank for root). | `"src"` or `""` |

### 🧪 Example Configurations

**1. Push to main branch (overwrite):**
```
GITHUB_USERNAME = "octocat"
GITHUB_TOKEN = "ghp_..."
REPO_NAME = "my-project"
BRANCH = "main"
OVERWRITE_BRANCH = True
TARGET_SUBDIR = ""
```

**2. Create a new branch for review:**
```
GITHUB_USERNAME = "octocat"
GITHUB_TOKEN = "ghp_..."
REPO_NAME = "my-project"
BRANCH = "main"
OVERWRITE_BRANCH = False
TARGET_SUBDIR = "mobile-upload"
```

---

## 📊 Sample Output

```
📱 Mobile Zip to GitHub Uploader
User: Shineii86
Repo: my-uploaded-code
Branch: main
==================================================

📤 Please upload your zip file...
✅ Uploaded: project.zip (245760 bytes)

📂 Extracting to temporary directory...
✅ Extracted 47 files/folders

📥 Cloning repository Shineii86/my-uploaded-code...
✅ Repository cloned successfully

📋 Copying files to repository...
✅ Copied 47 files

💾 Committing changes...
✅ Committed with message: '📱 Upload code from mobile via Colab'

🚀 Pushing to GitHub (branch: main)...
✅ Push successful!

==================================================
✨ Success! Your code is now on GitHub.
📊 View it at: https://github.com/Shineii86/my-uploaded-code/tree/main
```

---

## 🔬 How It Works

1. **File Upload**: Colab's `files.upload()` opens a native file picker on your phone.
2. **Extraction**: Python's `zipfile` module extracts contents to a temporary directory.
3. **Repository Clone**: `GitPython` clones your target repository using the token for authentication.
4. **File Copy**: All extracted files are recursively copied into the cloned repo.
5. **Git Commit**: Changes are staged and committed with your custom message.
6. **Git Push**: The commit is pushed to the specified branch (force‑push optional).
7. **Cleanup**: All temporary directories and the uploaded zip are deleted.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Repository not found` | Ensure the repository name is correct and exists under your account. |
| `Authentication failed` | Your token is incorrect or expired. Generate a new one with `repo` scope. |
| `Push failed` | Try setting `OVERWRITE_BRANCH = False` to create a new branch. |
| `No changes detected` | The files in your zip are identical to what's already in the repo. |
| Upload hangs on large files | Be patient — large zips take longer. Consider splitting into smaller zips. |

---

## 📄 License & Disclaimer

This project is licensed under the **MIT License**.

> ℹ️ This tool is intended to help developers manage code from mobile devices. Always review the contents of your zip before pushing to public repositories.

---

### 🔗 Quick Links

- [Google Colab](https://colab.research.google.com/)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [GitPython Documentation](https://gitpython.readthedocs.io/)

---

## 💕 Loved My Work?

🚨 [Follow me on GitHub](https://github.com/Shineii86)

⭐ [Give a star to this project](https://github.com/Shineii86/GitUnzip)

<div align="center">

<a href="https://github.com/Shineii86/GitUnzip">
<img src="https://github.com/Shineii86/AniPay/blob/main/Source/Banner6.png" alt="Banner">
</a>
  
  *For inquiries or collaborations*
     
[![Telegram Badge](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86 "Contact on Telegram")
[![Instagram Badge](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a "Follow on Instagram")
[![Pinterest Badge](https://img.shields.io/badge/-Pinterest-E60023?style=flat&logo=Pinterest&logoColor=white)](https://pinterest.com/ikx7a "Follow on Pinterest")
[![Gmail Badge](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com "Send an Email")

  <sup><b>Copyright © 2026 <a href="https://telegram.me/Shineii86">Shinei Nouzen</a> All Rights Reserved</b></sup>

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/GitUnzip?style=for-the-badge)

</div>
