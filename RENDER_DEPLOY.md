# 🚀 Deploying EduAgent AI to Render

Follow these steps to get your AI Agent live on the internet using Render.

## 📋 Prerequisites
1.  A [GitHub](https://github.com/) account with this repository pushed.
2.  A [Render](https://render.com/) account.

## 🛠️ Step-by-Step Deployment

### 1. Create a New Web Service
- Log in to your Render Dashboard.
- Click **New** > **Web Service**.
- Connect your GitHub account and select your **EduAgent-AI** repository.

### 2. Configure Build & Start Commands
- **Name:** `eduagent-ai` (or any name you like)
- **Environment:** `Python 3`
- **Region:** Choose the one closest to you (e.g., Singapore or US East).
- **Branch:** `main`
- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  streamlit run app.py --server.port $PORT --server.address 0.0.0.0
  ```

### 3. Set Environment Variables
Render needs your API keys to function. Click on the **Advanced** tab or go to the **Environment** section after creating the service:
- `GROQ_API_KEY`: Your Groq API key.
- `PYTHON_VERSION`: `3.11.0` (Recommended for compatibility).

### 4. Deploy!
- Click **Create Web Service**. 
- Render will start building the app. It may take 2-4 minutes for the first deploy.
- Once finished, you will see a URL (e.g., `https://eduagent-ai.onrender.com`).

---

## ⚠️ Important Notes

### 1. Data Persistence (TinyDB)
Since we are using **TinyDB** (`data/db.json`), your data (user history, cached research) will be **deleted** every time Render restarts or redeploys the app.
> [!TIP]
> To keep data permanently, consider switching to **MongoDB Atlas** (Free tier) and updating your `database.py`.

### 2. Port Configuration
Streamlit by default uses port `8501`. Render expects the app to listen on the port provided by the `$PORT` environment variable. Our **Start Command** handles this automatically.

### 3. Rendering Speed
The first load might be slow while the Spline background fetches assets. This is normal.
