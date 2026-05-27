# Deploying to Hugging Face Spaces

Hugging Face Spaces supports Streamlit applications natively. This is the
recommended deployment target for Representation Overlap Lab.

## Prerequisites

- A Hugging Face account
- Git installed locally
- The artifacts already generated (run `python scripts/export_demo_artifacts.py` first)

## Steps

### 1. Create a Space

Go to huggingface.co/new-space and configure:

- **Owner**: your username
- **Space name**: `representation-overlap-lab`
- **License**: MIT
- **SDK**: Streamlit
- **Hardware**: CPU Basic (free tier is sufficient - no model runs at runtime)
- **Visibility**: Public

### 2. Add the Space metadata to README.md

The Hugging Face Spaces system reads the README.md YAML frontmatter. Add this
block at the top of README.md before deploying:

```yaml
---
title: Representation Overlap Lab
emoji: 
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: true
license: mit
---
```

### 3. Push to the Space

```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/representation-overlap-lab
git push space main
```

If you have 2FA enabled on Hugging Face, use a personal access token as your password.

### 4. Verify the build

The Space will build automatically. Watch the build log in the Spaces UI.
Build time is typically 2-4 minutes for the first build (installing dependencies).

The app should load in under 5 seconds once built, because all artifacts are
pre-committed to the repo and no model download happens at runtime.

### 5. Updating

To push updates:

```bash
git push space main
```

### Notes on the artifacts

The .npy and .csv files in artifacts/ are committed to the repo.
They are small enough (< 2 MB for synthetic, < 500 KB for real 95-concept embeddings)
that this is fine for a Spaces deployment.

If you regenerate artifacts (with or without `--synthetic`), commit the updated
artifact files before pushing to the Space.

### Environment variables

No environment variables are required. The app uses no external APIs or secrets.

### Spaces-specific limitations

- Cold start: After a period of inactivity, Spaces may take 20-30 seconds to wake up.
- Memory: CPU Basic tier provides 16 GB RAM, which is more than sufficient.
- Storage: Spaces provides ephemeral storage. All persistent state must be in the repo.

### Custom domain

Hugging Face Spaces Pro supports custom domains. Configure this in the Space settings
after deployment.
