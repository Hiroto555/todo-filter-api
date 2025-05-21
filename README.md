# Todo Filter Application

This repository contains a FastAPI backend and a Next.js 14 frontend.

## Requirements
- Docker Compose

## Development

1. Generate frontend API client (requires Node packages installed):
   ```bash
   cd frontend
   npm install
   npm run generate
   ```
2. Start services:
   ```bash
   FRONT_ORIGIN=http://localhost:3000 docker compose up --build
   ```

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.
