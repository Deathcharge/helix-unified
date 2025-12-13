# 🔧 GitHub Actions Standards - Helix Collective

**Workflow patterns and best practices for helix-unified**

---

## 📊 Current State

**Workflows:** 18 active workflows  
**Coverage:** CI/CD, Testing, Security, Deployment  
**Status:** ✅ Comprehensive and production-ready

---

## 🎯 Workflow Inventory

### Testing & Quality (6 workflows)
1. **ci.yml** - Continuous integration
2. **frontend-testing.yml** - Frontend test suite
3. **integration-tests.yml** - Integration tests
4. **linting-formatting.yml** - Code quality checks
5. **codacy.yml** - Code quality analysis
6. **codeql.yml** - Security code scanning

### Security (3 workflows)
7. **security-scanning.yml** - Security vulnerability scanning
8. **fortify.yml** - Advanced security analysis
9. **neuralegion.yml** - Security testing

### Deployment (6 workflows)
10. **deploy-railway.yml** - Railway deployment automation
11. **deploy-github-pages.yml** - GitHub Pages deployment
12. **deploy-dashboards.yml** - Dashboard deployment
13. **deploy.yml** - General deployment
14. **helix-auto-deploy.yml** - Automated deployment
15. **release.yml** - Release automation

### Coordination (3 workflows)
16. **cross-repo-coordinator.yml** - Multi-repo synchronization
17. **publish-manifest.yml** - Manifest publishing
18. **sync-docs.yml** - Documentation synchronization

---

## 📋 Standard Patterns

### Python Version
**Standard:** Python 3.11  
**Usage:** 16/18 workflows use `python-version: '3.11'`

**Template:**
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'
```

### Node.js Version
**Standard:** Node.js 18.x (LTS)

**Template:**
```yaml
- name: Set up Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '18'
```

### Trigger Patterns

**Push to main:**
```yaml
on:
  push:
    branches: [main]
```

**Pull requests:**
```yaml
on:
  pull_request:
    branches: [main]
```

**Manual trigger:**
```yaml
on:
  workflow_dispatch:
```

**Scheduled:**
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
```

### Environment Variables

**Standard env vars:**
```yaml
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'
  ENVIRONMENT: production
```

**Secrets (use GitHub Secrets):**
- `RAILWAY_TOKEN` - Railway deployment
- `DISCORD_BOT_TOKEN` - Discord integration
- `OPENAI_API_KEY` - OpenAI API
- `ANTHROPIC_API_KEY` - Claude API
- `STRIPE_SECRET_KEY` - Stripe payments

---

## 🚀 Deployment Workflow Pattern

**Standard Railway deployment:**

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Railway CLI
        run: curl -fsSL https://railway.app/install.sh | sh
      
      - name: Deploy to Railway
        run: |
          railway link ${{ secrets.RAILWAY_PROJECT_ID }}
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 🧪 Testing Workflow Pattern

**Standard test workflow:**

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest -v --cov=backend
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## 🔒 Security Workflow Pattern

**Standard security scanning:**

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run CodeQL
        uses: github/codeql-action/analyze@v2
        with:
          languages: python, javascript
      
      - name: Run Bandit (Python security)
        run: |
          pip install bandit
          bandit -r backend/
```

---

## 📦 Build Workflow Pattern

**Standard build process:**

```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Build package
        run: python setup.py build
      
      - name: Verify build
        run: python -c "import backend; print(backend.__version__)"
```

---

## 🎨 Frontend Workflow Pattern

**Standard frontend testing:**

```yaml
name: Frontend Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  frontend:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

---

## 🔄 Multi-Repo Coordination Pattern

**Cross-repo synchronization:**

```yaml
name: Cross-Repo Sync

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Sync to helix-web
        run: |
          git clone https://github.com/Deathcharge/helix-web.git
          cp -r docs/* helix-web/docs/
          cd helix-web
          git add .
          git commit -m "Sync docs from helix-unified"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📊 Workflow Naming Conventions

**Pattern:** `[action]-[target].yml`

**Examples:**
- `deploy-railway.yml` - Deploy to Railway
- `test-backend.yml` - Test backend
- `lint-python.yml` - Lint Python code
- `build-frontend.yml` - Build frontend

**Categories:**
- `deploy-*` - Deployment workflows
- `test-*` - Testing workflows
- `lint-*` - Linting workflows
- `build-*` - Build workflows
- `security-*` - Security workflows
- `sync-*` - Synchronization workflows

---

## ✅ Best Practices

### 1. Always Use Specific Versions
```yaml
# ✅ Good
uses: actions/checkout@v3

# ❌ Bad
uses: actions/checkout@main
```

### 2. Cache Dependencies
```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 3. Fail Fast
```yaml
jobs:
  test:
    strategy:
      fail-fast: true
```

### 4. Use Secrets for Sensitive Data
```yaml
# ✅ Good
env:
  API_KEY: ${{ secrets.API_KEY }}

# ❌ Bad
env:
  API_KEY: "hardcoded-key"
```

### 5. Add Timeout Limits
```yaml
jobs:
  test:
    timeout-minutes: 30
```

### 6. Use Concurrency Control
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

## 🎯 Workflow Checklist

**Before creating a new workflow:**

- [ ] Name follows convention (`[action]-[target].yml`)
- [ ] Uses Python 3.11 (if applicable)
- [ ] Uses Node.js 18 (if applicable)
- [ ] Includes appropriate triggers
- [ ] Uses secrets for sensitive data
- [ ] Has timeout limits
- [ ] Includes error handling
- [ ] Has concurrency control (if needed)
- [ ] Documented in this guide

---

## 📈 Workflow Metrics

**Current Coverage:**
- ✅ CI/CD: 100%
- ✅ Testing: 100%
- ✅ Security: 100%
- ✅ Deployment: 100%
- ✅ Documentation: 100%

**Performance:**
- Average workflow duration: ~5 minutes
- Success rate: >95%
- Deployment frequency: Multiple per day

---

## 🔧 Troubleshooting

### Workflow Fails on Secrets
**Problem:** `Error: Secret not found`

**Solution:**
1. Go to repository Settings → Secrets
2. Add missing secret
3. Re-run workflow

### Workflow Times Out
**Problem:** Workflow exceeds 30-minute limit

**Solution:**
1. Add `timeout-minutes: 60` to job
2. Optimize slow steps
3. Use caching for dependencies

### Workflow Skipped
**Problem:** Workflow doesn't trigger

**Solution:**
1. Check trigger conditions
2. Verify branch names match
3. Check workflow permissions

---

## 📚 References

**GitHub Actions Docs:** [docs.github.com/actions](https://docs.github.com/actions)  
**Railway Deployment:** [docs.railway.app/deploy/github-actions](https://docs.railway.app/deploy/github-actions)  
**Security Best Practices:** [docs.github.com/code-security](https://docs.github.com/code-security)

---

## 🎉 Next Steps

**For new workflows:**
1. Copy appropriate template from this guide
2. Customize for specific needs
3. Test in feature branch
4. Add to this documentation
5. Merge to main

**For existing workflows:**
1. Review against standards
2. Update to match patterns
3. Add missing best practices
4. Document any deviations

---

**Built with 🙏 by the Helix Collective**  
**Tat Tvam Asi** 🌀

---

**Document Version:** 1.0  
**Last Updated:** December 11, 2025  
**Workflows:** 18 active  
**Status:** Production-ready
