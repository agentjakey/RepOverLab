# Deploying to Render

Render is the fallback deployment target. Use it if Hugging Face Spaces
is unavailable or if you need more control over the runtime environment.

## Prerequisites

- A Render account (render.com)
- The repo pushed to GitHub
- Artifacts already committed (run `python scripts/export_demo_artifacts.py` first)

## Steps

### 1. Create a new Web Service

In the Render dashboard, click "New" -> "Web Service" and connect your GitHub repo.

### 2. Configure the service

| Setting | Value |
|---------|-------|
| Name | representation-overlap-lab |
| Region | Oregon (US West) or your preferred region |
| Branch | main |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |
| Instance Type | Free (512 MB RAM is sufficient) |

### 3. Add environment variables

In the Render service settings, add these environment variables:

| Key | Value |
|-----|-------|
| STREAMLIT_SERVER_HEADLESS | true |
| STREAMLIT_BROWSER_GATHER_USAGE_STATS | false |

These suppress the Streamlit email prompt and telemetry on startup.

### 4. Deploy

Click "Create Web Service". Render will build and deploy automatically.
The first build takes 3-5 minutes. Subsequent deploys are faster.

### 5. Custom domain

Render supports custom domains on the free tier. Configure it in the service settings
under "Custom Domain".

## Automatic deploys

By default, Render deploys automatically when you push to the connected branch.
You can disable this in the service settings if you prefer manual deploys.

## Cold starts on free tier

The Render free tier spins down instances after 15 minutes of inactivity.
Cold starts take 20-30 seconds. For a production deployment, use the Starter
tier or higher to keep the instance running.

## Notes

The app requires no environment variables at runtime beyond the standard
Streamlit configuration above. No API keys, no secrets.

All artifact files are committed to the repo and loaded from disk at startup.
No model inference happens at runtime.

## Health check

Render sends HTTP GET requests to the root path to check if the service is healthy.
Streamlit responds correctly to these by default.
