# tfl-job-bot

Simple personal job checker that runs hourly with GitHub Actions and sends ntfy alerts.

## Quick safe setup (beginner-friendly)

1. Rotate the previously exposed ntfy topic before using this project again.
2. In GitHub, go to this repository's **Settings → Secrets and variables → Actions**.
3. Create a repository secret named `NTFY_TOPIC` with your new ntfy topic value.
4. Never commit `.env` files or real credentials (the included `.gitignore` helps protect this).
5. Open the **Actions** tab, select **24/7 Hourly Rail Job Checker**, and use **Run workflow** to test manually.
6. This project is intended to use only free standard GitHub-hosted Actions usage.