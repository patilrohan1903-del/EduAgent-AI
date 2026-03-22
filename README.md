# 🎓 EduAgent AI

A powerful **Autonomous Education Agent** that generates comprehensive mini-courses on any topic. 
It performs deep internet research, summarizes key concepts, finds relevant YouTube videos, and generates interactive quizzes.

## 🚀 Tech Stack & Why?

| Component | Technology | Why we used it? |
| :--- | :--- | :--- |
| **Frontend** | [Streamlit](https://streamlit.io/) | Fastest way to build data/AI apps. It bundles Frontend (HTML/CSS) & Backend (Python) in one. |
| **LLM (Brain)** | [Groq](https://groq.com/) | Extremely fast inference (Llama 3 70B), perfect for real-time agents. |
| **Orchestration** | [LangChain](https://langchain.com/) | Manages the flow between Researcher, Writer, and Quiz agents. |
| **Search** | [DuckDuckGo](https://duckduckgo.com/) | Free, privacy-focused search API for fetching real-time web data and videos. |
| **Database** | [MongoDB](https://www.mongodb.com/) | Stores user profiles, chat history, and flexible JSON content (Articles/Quizzes). |

---

## 🛠️ Installation & Setup (Local)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/education-agent.git
cd education-agent
```

### 2. Create Virtual Environment
It's best practice to keep dependencies isolated.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory and add your API keys:
```ini
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=mongodb://localhost:27017/  # Or your MongoDB Atlas URI
```

---

## ▶️ How to Run

Since this is a Streamlit app, **Frontend and Backend run together** with one command.

### Run the App
```bash
streamlit run app.py
```
This will open the app in your browser (usually `http://localhost:8501`).

### Run Backend Only (CLI Mode)
If you want to test the logic without the UI:
```bash
python main.py "Machine Learning"
```

---

## 🌍 Deployment Guide

To make this website live on the internet, you can use **Streamlit Cloud** (Easiest) or **Render/Railway**.

### Option 1: Streamlit Community Cloud (Recommended)
1.  Push your code to **GitHub**.
2.  Go to [share.streamlit.io](https://share.streamlit.io/) and login.
3.  Click **"New App"** and select your repository.
4.  **Main file path:** `app.py`
5.  **Advanced Settings:** Add your `GROQ_API_KEY` and `MONGO_URI` in the "Secrets" section.
6.  Click **Deploy**. 🚀

### Option 2: Render / Railway
If you deploy on a custom server, use these commands:

*   **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

## 🐳 Docker & Kubernetes Deployment

We provide a production-ready setup for Docker and Kubernetes to deploy on AWS or any cloud provider.

### 1. Docker
Build the image locally:
```bash
docker build -t eduagent-ai .
```
Run the container:
```bash
docker run -p 8501:8501 --env-file .env eduagent-ai
```

### 2. Kubernetes
Deploy to your cluster:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
> [!IMPORTANT]
> Ensure you create your secrets first! See `k8s/secrets.yaml.example` for details.

### 3. GitHub Actions (CI/CD)
The project includes a `deploy.yml` workflow. To use it:
1.  Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2.  Add the following secrets:
    - `DOCKERHUB_USERNAME`: Your Docker Hub username.
    - `DOCKERHUB_TOKEN`: Your Docker Hub personal access token.
    - `KUBECONFIG`: The contents of your `~/.kube/config` file.
    - `GROQ_API_KEY`: Your API key.
    - `MONGO_URI`: Your MongoDB connection string.
    - `MONGO_DB_NAME`: Your MongoDB database name.

---

---

## 📱 Mobile Responsiveness
The app is designed to be **fully responsive**.
*   **Desktop:** Wide layout, glassmorphism cards.
*   **Mobile:** Auto-adjusts padding, text size, and input width for easy typing.

---
*Built with ❤️ by EduAgent Team*


tere maaa kiii jay hoooo 