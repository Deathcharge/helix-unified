.PHONY: help install test lint format clean docker-up docker-down deploy health

# Default target
help:
	@echo "🌀 Helix Unified - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install all dependencies"
	@echo "  make install-hooks  Install pre-commit hooks"
	@echo ""
	@echo "Development:"
	@echo "  make dev            Start backend dev server"
	@echo "  make dev-frontend   Start frontend dev server"
	@echo "  make dev-dashboard  Start Streamlit dashboard"
	@echo "  make docker-up      Start PostgreSQL + Redis (docker-compose)"
	@echo "  make docker-down    Stop docker services"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run all tests"
	@echo "  make test-watch     Run tests in watch mode"
	@echo "  make test-cov       Run tests with coverage report"
	@echo "  make test-integration  Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run all linters"
	@echo "  make format         Auto-format code (black + isort)"
	@echo "  make type-check     Run mypy type checker"
	@echo "  make security       Run security scans (bandit + pip-audit)"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy         Deploy to Railway (git push)"
	@echo "  make health         Check all service health"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove cache and temp files"

# ============================================================================
# SETUP
# ============================================================================

install:
	@echo "📦 Installing backend dependencies..."
	pip install -r requirements-backend.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "📦 Installing dev dependencies..."
	pip install pre-commit pytest-watch black isort flake8 mypy bandit pip-audit
	@echo "✅ All dependencies installed!"

install-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install
	@echo "✅ Pre-commit hooks installed!"

# ============================================================================
# DEVELOPMENT
# ============================================================================

dev:
	@echo "🚀 Starting backend dev server..."
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "🚀 Starting frontend dev server..."
	@echo "Frontend: http://localhost:3000"
	cd frontend && npm run dev

dev-dashboard:
	@echo "📊 Starting Streamlit dashboard..."
	@echo "Dashboard: http://localhost:8501"
	cd dashboard && streamlit run streamlit_app.py

docker-up:
	@echo "🐳 Starting PostgreSQL + Redis..."
	docker-compose up -d
	@echo "✅ Docker services started!"
	@echo "PostgreSQL: localhost:5432"
	@echo "Redis: localhost:6379"

docker-down:
	@echo "🐳 Stopping Docker services..."
	docker-compose down
	@echo "✅ Docker services stopped!"

# ============================================================================
# TESTING
# ============================================================================

test:
	@echo "🧪 Running all tests..."
	pytest tests/ -v --cov=backend --cov-report=term-missing

test-watch:
	@echo "👀 Running tests in watch mode..."
	pytest-watch tests/ -- -v

test-cov:
	@echo "📊 Running tests with coverage report..."
	pytest tests/ -v --cov=backend --cov-report=html --cov-report=term-missing
	@echo "✅ Coverage report: htmlcov/index.html"

test-integration:
	@echo "🔗 Running integration tests only..."
	pytest tests/ -v -m integration

test-unit:
	@echo "⚡ Running unit tests only..."
	pytest tests/ -v -m unit

# ============================================================================
# CODE QUALITY
# ============================================================================

lint:
	@echo "🔍 Running all linters..."
	@echo "→ Flake8..."
	flake8 backend/ --count --max-complexity=10 --max-line-length=100 --statistics --exclude=backend/refactor_commands.py
	@echo "→ MyPy..."
	mypy backend/ --config-file=mypy.ini --show-error-codes --pretty || true
	@echo "✅ Linting complete!"

format:
	@echo "✨ Auto-formatting code..."
	black backend/ tests/ --line-length=100
	isort backend/ tests/ --profile=black
	@echo "✅ Code formatted!"

type-check:
	@echo "🔍 Running type checker..."
	mypy backend/ --config-file=mypy.ini --show-error-codes --pretty

security:
	@echo "🔒 Running security scans..."
	@echo "→ Bandit (SAST)..."
	bandit -r backend/ -ll
	@echo "→ pip-audit (dependencies)..."
	pip-audit --desc -r requirements-backend.txt --skip-editable
	@echo "✅ Security scans complete!"

# ============================================================================
# DEPLOYMENT
# ============================================================================

deploy:
	@echo "🚀 Deploying to Railway..."
	@echo "Current branch: $$(git branch --show-current)"
	@read -p "Push to Railway? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		git push origin $$(git branch --show-current); \
		echo "✅ Deployed! Check Railway dashboard."; \
	else \
		echo "❌ Deployment cancelled."; \
	fi

health:
	@echo "🏥 Checking service health..."
	@echo "→ Backend API..."
	@curl -s http://localhost:8000/health | jq '.' || echo "❌ Backend not responding"
	@echo ""
	@echo "→ Dashboard..."
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:8501 || echo "❌ Dashboard not responding"
	@echo ""
	@echo "→ PostgreSQL..."
	@docker ps | grep postgres || echo "❌ PostgreSQL not running"
	@echo "→ Redis..."
	@docker ps | grep redis || echo "❌ Redis not running"

# ============================================================================
# CLEANUP
# ============================================================================

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# ============================================================================
# ALIASES
# ============================================================================

t: test
tc: test-cov
l: lint
f: format
d: dev
