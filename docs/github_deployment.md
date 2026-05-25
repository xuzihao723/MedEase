# GitHub Deployment Guide

## Option A: Upload through GitHub Website

1. Create a new GitHub repository named:

```text
ai-medical-advice-comprehensibility
```

2. Upload the contents of this folder.

3. Do not upload local-only files such as:

```text
.env
__pycache__/
*.pyc
backend/logs/
backend/tmp_pyc/
```

The `.gitignore` file already excludes these files.

## Option B: Push with Git

Run these commands from this folder:

```powershell
git init
git add .
git commit -m "Initial public research prototype"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-medical-advice-comprehensibility.git
git push -u origin main
```

## GitHub Pages for the Frontend

The frontend is static and can be published with GitHub Pages.

Recommended setting:

```text
Settings -> Pages -> Deploy from branch -> main -> /frontend
```

If GitHub Pages does not support selecting `/frontend` directly in your repository settings, move the frontend files to `/docs` or use a small GitHub Actions workflow.

## Before Publishing

Check:

```powershell
git status
git ls-files
```

Make sure the repository does not include:

```text
backend/.env
raw medical data
private user records
large temporary files
API keys
```
