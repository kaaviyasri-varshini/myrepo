# AI Study Buddy - Deployment Guide

## Quick Deploy to Render (Free Hosting)

1. **Push your code to GitHub:**
   - Create a new repository on GitHub
   - Push this code to your repository

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Environment:** Python 3

3. **Your app will be live at:** `https://your-app-name.onrender.com`

## Alternative: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect and deploy your Flask app

## Alternative: Deploy to Heroku

1. Install Heroku CLI
2. Run these commands:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## Features

- Student profile management
- AI-powered study assistance
- Personalized study planning
- Practice quizzes
- Exam preparation tools
- Performance analytics