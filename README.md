<div align="center">
  
<a href="https://github.com/Shineii86/GitUnzip">
<img src="https://raw.githubusercontent.com/Shineii86/GitUnzip/main/images/GitUnzip.png" width="200px" alt="GitUnzip">
</a>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shineii86/GitUnzip/blob/main/notebooks/GitUnzip.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/GitUnzip?style=for-the-badge)](https://github.com/Shineii86/GitUnzip/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/GitUnzip?style=for-the-badge)](https://github.com/Shineii86/GitUnzip/fork)

**Upload a zip file from your phone, watch it unzip with live progress bars, and push the entire codebase to GitHub — all from Google Colab.**

</div>

---

> ℹ️ **ABOUT THIS TOOL**
> - **GitUnzip** solves the mobile‑to‑GitHub workflow: you can't upload folders or unzip files directly from a phone browser.
> - Upload a zip, and this tool extracts it and pushes everything to your repository with beautiful progress animations.
> - You need a **GitHub Personal Access Token (classic)** with `repo` scope.

---

## 🎯 What is This Tool?

**GitUnzip** bridges the gap between mobile file management and GitHub. It provides a seamless, animated experience for uploading entire project folders from your phone to GitHub — something that's impossible through the GitHub mobile site alone.

### ✨ New in This Version

- **Live Progress Bars** – Watch real‑time progress for extraction, file copying, and push operations.
- **Cleaner UI** – Only essential fields are visible; the tool handles the rest.

---

## ✨ Features

| Feature                      | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 📱 **Mobile‑Friendly Upload** | Native file picker works on iOS and Android.                                |
| 📊 **Animated Progress**      | `tqdm` progress bars for extraction, copying, and pushing.                  |
| 🔒 **Automatic Watermark**    | Commits are signed with `📤 Uploaded By Shineii86/GitUnzip`.              |
| 🌿 **Safe Branching**         | Option to create a new branch instead of overwriting.                       |
| 🧹 **Automatic Cleanup**      | Temporary files are deleted after completion.                               |

---

## 🛠️ Prerequisites

1. **A GitHub account**.
2. **A target repository** (must already exist).
3. **A Personal Access Token (classic)** with `repo` scope.

### 🔑 How to Get a Personal Access Token

1. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
2. Click **Generate new token (classic)**.
3. Check the **`repo`** scope.
4. Generate and copy the token immediately.

---

## 🚀 Quick Start

1. **Click the "Open in Colab" badge** above.
2. **Enter your GitHub username and token**.
3. **Specify the target repository name**.
4. **Run both cells**.
5. When prompted, tap **"Choose Files"** and select your zip file.
6. Watch the progress bars animate — your code will be on GitHub in seconds!

---

## ⚙️ Configuration Options

| Parameter | Description | Example |
|-----------|-------------|---------|
| `GITHUB_USERNAME` | Your GitHub username. | `"Shineii86"` |
| `GITHUB_TOKEN` | Personal Access Token with `repo` scope. | `"ghp_abc123..."` |
| `REPO_NAME` | Target repository name (must exist). | `"my-uploaded-code"` |
| `BRANCH` | Branch to push to. | `"main"` |
| `OVERWRITE_BRANCH` | If `True`, force‑push; if `False`, creates a new timestamped branch. | `True` |
| `TARGET_SUBDIR` | Subdirectory within repo (leave blank for root). | `"src"` or `""` |

> [!NOTE]
>  The commit message is automatically set to `📤 Uploaded By Shineii86/GitUnzip` and cannot be changed — this ensures proper attribution.

---

## 📊 Sample Output (Animated)

```
📱 GitUnzip - Mobile to GitHub Uploader
User: Shineii86 | Repo: my-code | Branch: main
==================================================

📤 Please select your zip file...
   (Tap 'Choose Files' below — your phone's file picker will open)

✅ Uploaded: project.zip (2.45 MB)

📂 Extracting zip file...
Extracting: 100%|████████████| 47/47 [00:00<00:00, 156.32files/s]
✅ Extracted 47 files/folders

📥 Cloning repository Shineii86/my-code...
✅ Repository cloned

📋 Copying files to repository...
Copying: 100%|████████████| 47/47 [00:00<00:00, 210.45files/s]
✅ Copied 47 files

💾 Committing changes...
✅ Committed: '📤 Uploaded By [Shineii86/GitUnzip]'

🚀 Pushing to GitHub (branch: main)...
   This may take a moment...
Pushing: 100%|████████████| 100/100 [00:02<00:00, 41.23it/s]
✅ Push successful!

==================================================
✨ Success! Your code is now on GitHub.
📊 View it at: https://github.com/Shineii86/my-code/tree/main
```

---

## 🔬 How It Works

1. **Upload**: Colab's `files.upload()` opens a native file picker.
2. **Extract**: `zipfile` extracts contents while `tqdm` shows progress.
3. **Clone**: `GitPython` clones the target repo using your token.
4. **Copy**: Files are recursively copied with a progress bar.
5. **Commit**: Changes are committed with the watermark message.
6. **Push**: Code is pushed to GitHub (force‑push optional).
7. **Cleanup**: Temp files are deleted.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Repository not found` | Ensure the repo name is correct and exists. |
| `Authentication failed` | Token is invalid or lacks `repo` scope. |
| `Push failed` | Try setting `OVERWRITE_BRANCH = False`. |
| Upload button doesn't appear | Re‑run the configuration cell. |

---

## 📄 License & Disclaimer

This project is licensed under the **MIT License**.

---

### 🔗 Quick Links

- [Google Colab](https://colab.research.google.com/)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)

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
