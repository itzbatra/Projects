# FinGuard 360

A secure, full-stack personal finance dashboard demo — built as a portfolio/co-op project scaffold.

This version includes:
- Modular Flask backend with blueprints (auth, accounts, transactions, admin, audit)
- Refresh tokens, JWT access tokens, rate limiting, CORS, and secure headers
- Report generation using ReportLab and S3 upload stub using boto3
- Frontend: Vite + React with Tailwind starter + Admin panel skeleton
- Docker + docker-compose for local dev
- GitHub Actions: CI and a deploy template (ECS/RDS placeholders)
- Basic pytest tests for auth flows

## Quick start (local)

1. Install Docker & Docker Compose.
2. From repo root:
   ```
   docker-compose up --build
   ```
3. Initialize the backend DB and seed data:
   ```
   docker-compose run --rm backend flask init-db
   docker-compose run --rm backend python backend/scripts/seed_mock_data.py
   ```
4. Backend API: http://localhost:5000/api
   Frontend: http://localhost:5173

## Security notes
- Set secure `SECRET_KEY`, `JWT_SECRET`, and AWS credentials via environment variables in production.
- Use HTTPS in production; configure TLS on load balancer.
- Harden CORS and CSP in production.

Author: Priyanshu Batra
