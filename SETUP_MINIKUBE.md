# Minikube Setup Guide (EduAgent-AI)

## 0. Install Minikube (Windows)
If you don't have Minikube installed yet, follow these steps:

### Option A: Using Winget (Recommended)
Open a terminal (PowerShell or Command Prompt) and run:
```bash
winget install minikube
```

### Option B: Manual Download
1. Download the [Minikube Installer](https://storage.googleapis.com/minikube/releases/latest/minikube-installer.exe).
2. Run the installer and follow the prompts.

### Prerequisites
- **Virtualization**: Ensure virtualization is enabled in your BIOS/UEFI settings.
- **Alternative Drivers (If you don't have Docker Desktop)**:
  - **Hyper-V**: (Windows Pro/Enterprise) Run `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All` in Admin PowerShell.
  - **VirtualBox**: Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

### Docker Hub vs Docker Desktop
- **Docker Hub**: Online storage for your images (like GitHub for code).
- **Docker Desktop**: The engine that builds and runs containers on your PC.
- *Note*: If you don't have Docker Desktop, Minikube can create its own "internal" Docker engine using a Virtual Machine (VirtualBox or Hyper-V).

---

Follow these steps to deploy the Education React/Streamlit application onto a local Minikube cluster with zero-downtime rolling updates.

## 1. Start Minikube
Use the driver that matches what you have installed:

### If using Hyper-V:
```powershell
minikube start --driver=hyperv
```

### If using VirtualBox:
```powershell
minikube start --driver=virtualbox
```

## 2. Configure Environment Secrets
The application requires several secrets (API keys and DB URIs). 
1. Copy the example secrets file:
   ```bash
   cp k8s/secrets.yaml.example k8s/secrets.yaml
   ```
2. Edit `k8s/secrets.yaml` and provide the base64 encoded values for:
   - `GROQ_API_KEY`
   - `MONGO_URI`
   - `MONGO_DB_NAME`
   
   *Tip: Use `echo -n "your-value" | base64` to encode values.*

3. Apply the secrets:
   ```bash
   kubectl apply -f k8s/secrets.yaml
   ```

## 3. Build Docker Image locally
To use the local image in Minikube, point your terminal's Docker daemon to Minikube's:
```bash
# PowerShell (Admin might be required)
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Build the image
docker build -t eduagent-ai:latest .
```

## 4. Deploy to Kubernetes
Apply the optimized manifests:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## 5. Verify Rolling Updates
To test the "Zero-Downtime" feature, you can trigger a rollout restart and watch the pods transition:
```bash
# Watch pods in a separate terminal
kubectl get pods -w

# Trigger a rolling update
kubectl rollout restart deployment/eduagent-ai-deployment

# Check rollout status
kubectl rollout status deployment/eduagent-ai-deployment
```

## 6. Access the Application
```bash
minikube service eduagent-ai-service
```
