# Donation Tracker

This React application tracks and combines donation amounts from Fallen Patriots and YouTube sources, updating every 5 minutes using GitHub Actions.

## Setup and Deployment

1. Create a new repository on GitHub

2. Initialize git and push to your repository:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/donation-tracker.git
git push -u origin main
```

3. Enable GitHub Actions:
   - Go to your repository's Settings
   - Navigate to Actions > General
   - Under "Workflow permissions", select "Read and write permissions"
   - Save the changes

4. Deploy to GitHub Pages:
   - Update the `homepage` field in `package.json` to match your repository:
     ```json
     "homepage": "https://YOUR_USERNAME.github.io/donation-tracker"
     ```
   - Run the deployment command:
     ```bash
     npm run deploy
     ```
   - Go to your repository's Settings > Pages
   - Set the source to "gh-pages" branch
   - Save the changes

## How It Works

1. GitHub Actions runs every 5 minutes to:
   - Scrape the latest donation amounts
   - Update the `data/donations.json` file
   - Commit and push the changes

2. The React frontend:
   - Reads the donation data from `data/donations.json`
   - Updates the display every minute
   - Shows individual and combined donation totals

## Features

- Automatic updates every 5 minutes via GitHub Actions
- Clean, responsive UI
- Shows individual and combined donation totals
- Displays last update time
- No backend server required
