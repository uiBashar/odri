EduMateBD – AI Education Assistant (Bangla/English)

Monorepo layout:

- backend/ – FastAPI service with QA, Math solver, Quiz, Payments stubs
- mobile/ – Flutter app scaffold (Bangla/English toggle, theme)

Quickstart (Backend):

1) Python env
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt

2) Env
   cp backend/.env.example backend/.env
   export $(grep -v '^#' backend/.env | xargs) # or rely on dotenv

3) Run
   uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000

Health: GET http://localhost:8000/health

Endpoints:
- POST /api/qa/ask
- POST /api/math/solve
- POST /api/quiz/generate
- POST /api/payments/checkout
- POST /api/payments/webhook

Deploy:
- Dockerfile provided in backend/

Mobile (Flutter):
- See mobile/ for a minimal scaffold with language toggle and theme.

# Text To Image App

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/templates/tree/main/text-to-image-template)

![Text To Image Template Preview](https://imagedelivery.net/wSMYJvS3Xw-n339CbDyDIA/dddfe97e-e689-450b-d5a9-d49801da6a00/public)

<!-- dash-content-start -->

Generate images based on text prompts using [Workers AI](https://developers.cloudflare.com/workers-ai/). In this example, going to the website will generate an image from the prompt "cyberpunk cat" using the `@cf/stabilityai/stable-diffusion-xl-base-1.0` model. Be patient! Your image may take a few seconds to generate.

<!-- dash-content-end -->

## Getting Started

Outside of this repo, you can start a new project with this template using [C3](https://developers.cloudflare.com/pages/get-started/c3/) (the `create-cloudflare` CLI):

```bash
npm create cloudflare@latest -- --template=cloudflare/templates/text-to-image-template
```

A live public deployment of this template is available at [https://text-to-image-template.templates.workers.dev](https://text-to-image-template.templates.workers.dev)

## Setup Steps

1. Install the project dependencies with a package manager of your choice:
   ```bash
   npm install
   ```
2. Deploy the project!
   ```bash
   npx wrangler deploy
   ```
