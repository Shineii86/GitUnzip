<div align="center">

[![GitUnzip Banner](https://raw.githubusercontent.com/Shineii86/GitUnzip/main/images/GitUnzip.png)](https://github.com/Shineii86/GitUnzip)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shineii86/GitUnzip/blob/main/notebooks/GitUnzip.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/GitUnzip?style=for-the-badge)](https://github.com/Shineii86/GitUnzip/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/GitUnzip?style=for-the-badge)](https://github.com/Shineii86/GitUnzip/fork)

**Upload archives (.zip, .tar.gz, .7z, .rar) from your phone, auto-create repos, get alerts, and share via QR codes — all from Google Colab. No PC required.**

</div>

---

> 🚀 **v2.0 — NOW MODULAR & MORE POWERFUL**
>
> GitUnzip bridges the gap between mobile file management and GitHub. Upload a zip from your phone, and it extracts everything and pushes to your repo with progress animations.

---

## 📖 Table of Contents

- [What is GitUnzip?](#-what-is-gitunzip)
- [🆕 What's New in v2.0](#-whats-new-in-v20)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Setup Guide](#-setup-guide)
- [Configuration Reference](#-configuration-reference)
- [Supported Formats](#-supported-formats)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License](#-license)
- [Credits](#-credits)

---

## 🎯 What is GitUnzip?

**GitUnzip** solves the mobile-to-GitHub workflow: you can't upload folders or unzip files directly from the GitHub mobile site.

- **Upload** a zip/tar/7z/rar from your phone
- **Extract** it with progress bars
- **Push** the entire codebase to your GitHub repo
- **Share** via QR code

No PC needed. No desktop Git clients. Just your phone and Google Colab.

---

## 🆕 What's New in v2.0

| Improvement | Description |
|-------------|-------------|
| 🏗️ **Modular Architecture** | Refactored into clean `gitunzip/` Python package |
| 📦 **.rar, .bz2, .xz Support** | Now handles 7 archive formats |
| 🤖 **Telegram Notifications** | Get upload alerts in Telegram |
| ✏️ **Custom Commit Messages** | Your own message instead of watermark |
| 🔒 **Private Repos** | Option to create private repositories |
| 🧹 **Junk Exclusion** | Auto-skips `__pycache__`, `.git`, `node_modules`, `.DS_Store` |
| 🛡️ **Path Traversal Protection** | Blocks malicious paths inside archives |
| 💣 **Zip Bomb Detection** | Rejects archives with >1GB uncompressed |
| ✅ **Archive Validation** | Integrity checks before extraction |
| 📊 **Processing Summary** | Stats and timing after upload |
| 🔀 **PR Link Generation** | Auto-generates PR link for new branches |
| 📝 **Better Error Handling** | Graceful failures with clear messages |

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Multi-format | `.zip`, `.tar.gz`, `.tgz`, `.7z`, `.rar`, `.bz2`, `.xz` |
| 2 | Auto-create repo | Creates repository if it doesn't exist |
| 3 | Private repos | Option to create private repos |
| 4 | Email notifications | Get alerted when upload completes |
| 5 | Telegram notifications | Get alerts in Telegram |
| 6 | Multiple archives | Upload several files at once |
| 7 | QR code sharing | Scan to open repo on another device |
| 8 | Progress bars | Visual feedback for every step |
| 9 | Custom commit message | Your own commit message |
| 10 | Junk exclusion | Skips `__pycache__`, `.git`, `node_modules`, etc. |
| 11 | Safe branching | Create new branch instead of overwriting |
| 12 | Path traversal protection | Blocks malicious archive paths |
| 13 | Zip bomb detection | Rejects archives >1GB uncompressed |
| 14 | Subdirectory target | Place files in a specific subdirectory |
| 15 | PR link generation | Auto-generates PR link for new branches |
| 16 | Processing summary | Shows stats and timing after upload |

---

## 📁 Project Structure

```
GitUnzip/
├── notebooks/
│   └── GitUnzip.ipynb         # Colab notebook (main entry point)
├── gitunzip/
│   ├── __init__.py             # Package metadata
│   ├── __main__.py             # CLI entry point
│   ├── config.py               # Configuration management
│   ├── archives.py             # Archive extraction (zip, tar, 7z, rar)
│   ├── github_ops.py           # GitHub repo operations
│   ├── notifications.py        # Email & Telegram notifiers
│   ├── qrcodes.py              # QR code generation
│   └── core.py                 # Main processing logic
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## 🛠️ Prerequisites

| Credential | Purpose | Where to Get It |
|------------|---------|-----------------|
| GitHub Account | Storage | [github.com](https://github.com) |
| GitHub PAT (Classic) | API access | [Settings → Tokens](https://github.com/settings/tokens) — check `repo` scope |

### Optional

| Credential | Purpose | Where to Get It |
|------------|---------|-----------------|
| Gmail App Password | Email alerts | [Google App Passwords](https://myaccount.google.com/apppasswords) |
| Telegram Bot Token | Telegram alerts | [@BotFather](https://t.me/botfather) |

---

## 📋 Setup Guide

### 1. Get Your GitHub Token

1. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token** → **Generate new token (classic)**
3. Name it `GitUnzip`, set expiration (30 days recommended)
4. Check **`repo`** scope
5. Click **Generate token** and **copy it immediately** (starts with `ghp_`)

> 🔒 Treat this token like a password. Never commit it or share it publicly.

### 2. Run in Colab

1. Click the **Open in Colab** badge at the top
2. Enter your GitHub username and token
3. Specify the target repository name
4. Run both cells
5. When prompted, select your archive file(s)
6. Watch the progress bars — your code will be on GitHub in seconds!

---

## ⚙️ Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `GITHUB_USERNAME` | string | — | Your GitHub username |
| `GITHUB_TOKEN` | string | — | GitHub PAT with `repo` scope |
| `REPO_NAME` | string | `my-uploaded-code` | Target repository (auto-created) |
| `BRANCH` | string | `main` | Target branch |
| `OVERWRITE_BRANCH` | bool | `True` | Force-push or create new branch |
| `TARGET_SUBDIR` | string | `""` | Subdirectory in repo |
| `PRIVATE_REPO` | bool | `False` | Create as private repo |
| `CUSTOM_COMMIT_MSG` | string | `""` | Custom commit message |
| `SEND_EMAIL` | bool | `False` | Enable email notifications |
| `EMAIL_TO` / `EMAIL_FROM` | string | — | Email addresses |
| `EMAIL_PASSWORD` | string | — | Gmail app password |
| `SMTP_SERVER` | string | `smtp.gmail.com` | SMTP server |
| `SMTP_PORT` | int | `465` | SMTP port |
| `TELEGRAM_BOT_TOKEN` | string | — | Telegram bot token |
| `TELEGRAM_CHAT_ID` | string | — | Telegram chat ID |

---

## 📦 Supported Formats

| Format | Extension | Library |
|--------|-----------|---------|
| ZIP | `.zip` | `zipfile` (stdlib) |
| Tarball | `.tar.gz`, `.tgz` | `tarfile` (stdlib) |
| Bzip2 | `.bz2` | `tarfile` (stdlib) |
| XZ | `.xz` | `tarfile` (stdlib) |
| 7-Zip | `.7z` | `py7zr` |
| RAR | `.rar` | `rarfile` |

---

## 🔬 How It Works

```
📱 Phone → 📤 Upload → 📂 Extract → 📋 Copy → 💾 Commit → 🚀 Push → 🔗 GitHub
```

1. **Upload**: Colab's `files.upload()` opens native file picker (works on iOS/Android)
2. **Validate**: Checks archive integrity and detects zip bombs
3. **Extract**: Extracts with junk file exclusion and path traversal protection
4. **Clone**: GitPython clones the target repo using your token
5. **Copy**: Files are recursively copied to the repo
6. **Commit**: Changes committed with your message or watermark
7. **Push**: Code pushed to GitHub (force-push optional)
8. **QR**: QR code generated for easy sharing
9. **Notify**: Email/Telegram notification sent
10. **Cleanup**: Temp files deleted

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Repository not found | Auto-created if missing. Ensure token has `repo` scope. |
| Authentication failed | Token is invalid or expired. Generate a new one. |
| Push failed | Try `OVERWRITE_BRANCH = False` to create a new branch. |
| Upload button doesn't appear | Re-run the configuration cell. |
| Extraction failed | Archive may be corrupted. Try re-downloading it. |
| Email not sending | Use App Password, not regular password. Enable 2FA. |
| Telegram not working | Verify token & chat ID. Send `/start` to bot first. |
| Large file fails | GitHub API limit: 100MB per file. |

---

## ❓ FAQ

**Is it free?** Yes — GitHub free repos + Colab free tier.

**What formats are supported?** `.zip`, `.tar.gz`, `.tgz`, `.7z`, `.rar`, `.bz2`, `.xz`

**Can I upload folders?** Zip them first, then upload the zip.

**Can I create private repos?** Yes — set `PRIVATE_REPO = True`.

**What files get excluded?** `__pycache__`, `.git`, `node_modules`, `.DS_Store`, `Thumbs.db`, `.env`, `*.pyc`, `*.swp`

**Can I use a custom commit message?** Yes — set `CUSTOM_COMMIT_MSG`.

**How do I get Telegram notifications?** Create a bot via [@BotFather](https://t.me/botfather), get your chat ID from [@userinfobot](https://t.me/userinfobot).

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file.

> [!WARNING]
> GitUnzip is for personal, legitimate use only. Respect GitHub's Terms of Service.

---

## 🙏 Credits

[Google Colab](https://colab.research.google.com/) · [GitHub](https://github.com) · [GitPython](https://gitpython.readthedocs.io/) · [tqdm](https://tqdm.github.io/) · [py7zr](https://pypi.org/project/py7zr/) · [qrcode](https://pypi.org/project/qrcode/)

---

<div align="center">

**Copyright [Shinei Nouzen](https://github.com/Shineii86) All Rights Reserved.**

*Made with ❤️ for mobile developers*

[![Telegram](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86)
[![Instagram](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a)
[![Gmail](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com)

⭐ [Star this repo](https://github.com/Shineii86/GitUnzip) · 🐛 [Report issue](https://github.com/Shineii86/GitUnzip/issues) · 🔧 [Contribute](https://github.com/Shineii86/GitUnzip/fork)

</div>
