# 🚀 Production Deployment Checklist - December 15, 2025

**Target Launch:** December 15, 2025 @ 00:00 UTC
**Current Date:** December 13, 2025
**Days Remaining:** 2 days
**Go/No-Go Decision:** December 14, 2025 @ 16:00 UTC

---

## 📋 Pre-Launch Checklist

### 🔐 Security (CRITICAL - Must Pass)

- [ ] **Vulnerability Scan:** Run Trivy on latest Docker image
  ```bash
  docker build -t helix-unified:pre-launch .
  trivy image helix-unified:pre-launch --severity HIGH,CRITICAL
  ```
  - **Target:** Zero HIGH/CRITICAL vulnerabilities
  - **Owner:** DevOps/Security Team
  - **Deadline:** Dec 14, 12:00 UTC

- [ ] **Code Security Audit:** Verify all CodeQL/Bandit alerts resolved
  - Check GitHub Security tab for open alerts
  - Review any suppressed warnings for validity
  - **Target:** Zero unresolved security alerts
  - **Owner:** Security Team
  - **Deadline:** Dec 14, 12:00 UTC

- [ ] **Secrets Rotation:** Rotate all production API keys
  - Claude API key (Anthropic)
  - Manus.space accounts (5 keys)
  - Discord bot token
  - Database credentials
  - Railway environment secrets
  - **Target:** All secrets <7 days old
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 14:00 UTC

- [ ] **Rate Limiting Verification:** Test SlowAPI limits are enforced
  ```bash
  # Test rate limiting endpoint
  for i in {1..1001}; do curl -s https://helixspiral.work/health; done | grep -c "429"
  ```
  - **Target:** Requests 1001+ return 429 Too Many Requests
  - **Owner:** QA Team
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **CORS Configuration:** Verify allowed origins are production-only
  - Check `backend/main.py` CORS middleware
  - Remove any `localhost`, `127.0.0.1`, wildcard (`*`) origins
  - **Target:** Only production domains allowed
  - **Owner:** Backend Team
  - **Deadline:** Dec 14, 08:00 UTC

---

### ⚡ Performance (CRITICAL - Must Pass)

- [ ] **Load Test (1000 Users):** Run `scripts/load_test.py`
  ```bash
  python scripts/load_test.py
  ```
  - **Target:** P95 response time <200ms, >99.5% success rate
  - **Owner:** Performance Team
  - **Deadline:** Dec 14, 10:00 UTC
  - **Report Location:** `load_test_report_YYYYMMDD_HHMMSS.json`

- [ ] **24-Hour Sustained Load:** Run extended stress test
  ```bash
  # Run sustained test in background
  nohup python scripts/load_test_sustained.py --duration=86400 &
  ```
  - **Target:** No degradation over 24 hours, <1% error rate
  - **Owner:** SRE Team
  - **Deadline:** Dec 13, 16:00 UTC (must start 24h before launch)
  - **Monitor:** `tail -f load_test_sustained.log`

- [ ] **GZIP Compression Verification:** Test response compression
  ```bash
  curl -H "Accept-Encoding: gzip" -I https://helixspiral.work/health | grep -i "content-encoding: gzip"
  ```
  - **Target:** Responses >1KB are gzip-compressed
  - **Owner:** Backend Team
  - **Deadline:** Dec 14, 08:00 UTC

- [ ] **CDN/Caching:** Verify static assets are cached
  - Check `frontend/` assets have cache headers
  - Test image/CSS/JS load times
  - **Target:** Static assets <100ms load time
  - **Owner:** Frontend Team
  - **Deadline:** Dec 14, 08:00 UTC

- [ ] **Core Web Vitals:** Measure frontend performance
  ```bash
  # Run Lighthouse CI
  npm run lighthouse -- https://helixspiral.work
  ```
  - **Target:** FCP <2s, LCP <2.5s, CLS <0.1, FID <100ms
  - **Owner:** Frontend Team
  - **Deadline:** Dec 14, 10:00 UTC

---

### 🤖 Agent Ecosystem (HIGH Priority)

- [ ] **Claude API Cooldown:** Test queue system under load
  - Trigger cooldown by hitting 80% threshold (40 req/min)
  - Verify requests queue and retry successfully
  - Check `/api/claude/status` endpoint returns metrics
  - **Target:** Zero 429 errors exposed to users, <5s queue delay
  - **Owner:** AI/Agent Team
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **Manus Account Pool:** Verify failover works
  - Exhaust quota on one account (simulate with script)
  - Verify automatic failover to next account
  - Test circuit breaker (5 consecutive failures)
  - **Target:** 100% failover success, <1s failover time
  - **Owner:** AI/Agent Team
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **Webhook Retry System:** Test Zapier integration
  ```bash
  pytest tests/test_zapier_integration.py -v
  ```
  - Send test webhooks to live Zapier endpoint
  - Verify retry on timeout/5xx errors
  - **Target:** >99% success rate, <500ms p95 latency
  - **Owner:** Integration Team
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **Discord Bot:** Test all commands in production environment
  - `/helix help` - Command list
  - `/helix status` - System health
  - `/helix manus` - Manus pool status
  - **Target:** All commands respond <2s, no errors
  - **Owner:** Bot Team
  - **Deadline:** Dec 14, 08:00 UTC

---

### 🧪 Testing (HIGH Priority)

- [ ] **Unit Tests:** Run full test suite
  ```bash
  pytest tests/ -v --tb=short
  ```
  - **Target:** 100% tests pass, no flaky tests
  - **Owner:** QA Team
  - **Deadline:** Dec 14, 08:00 UTC

- [ ] **Test Coverage:** Measure code coverage
  ```bash
  pytest --cov=backend --cov-report=term-missing --cov-report=html
  ```
  - **Target:** >80% coverage on critical paths (auth, API, webhooks)
  - **Owner:** QA Team
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **Integration Tests:** Test end-to-end flows
  - User signup → Discord link → Claude request → Response
  - Zapier webhook → Helix processing → Response
  - Manus API call → Failover → Success
  - **Target:** All critical flows pass without manual intervention
  - **Owner:** QA Team
  - **Deadline:** Dec 14, 12:00 UTC

- [ ] **Browser Compatibility:** Test in major browsers
  - Chrome (latest)
  - Firefox (latest)
  - Safari (latest)
  - Mobile Safari (iOS)
  - Chrome Mobile (Android)
  - **Target:** No visual/functional issues in any browser
  - **Owner:** Frontend Team
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **Accessibility Testing:** WCAG 2.1 AA compliance
  - Run axe DevTools on all pages
  - Test keyboard navigation
  - Test screen reader compatibility
  - **Target:** Zero critical accessibility violations
  - **Owner:** Frontend Team
  - **Deadline:** Dec 14, 12:00 UTC

---

### 🗄️ Database & Infrastructure (HIGH Priority)

- [ ] **Database Backup:** Take pre-launch snapshot
  ```bash
  # Railway database backup
  railway run --service postgres pg_dump > backup_pre_launch_20251214.sql
  ```
  - **Target:** Verified restorable backup <1 hour old
  - **Owner:** DBA/DevOps
  - **Deadline:** Dec 14, 23:00 UTC

- [ ] **Connection Pooling:** Verify pg pool settings
  - Check `backend/core/database.py` pool size
  - **Target:** Pool size >= 20, max overflow >= 10
  - **Owner:** Backend Team
  - **Deadline:** Dec 14, 08:00 UTC

- [ ] **Railway Scaling:** Set appropriate resource limits
  - API service: 2GB RAM, 2 vCPU minimum
  - Database: Verify production plan
  - **Target:** Auto-scaling enabled, headroom for 3x traffic
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 14:00 UTC

- [ ] **Health Check Endpoints:** Verify Railway monitors are configured
  - `/health` returns 200 with uptime
  - Railway restart policy: Always restart on failure
  - **Target:** <30s detection + restart on failure
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 08:00 UTC

- [ ] **Domain & DNS:** Verify production domain configured
  - Check `helixspiral.work` points to Railway
  - Verify SSL certificate valid (Let's Encrypt)
  - Test HTTPS redirect (HTTP → HTTPS)
  - **Target:** A+ SSL Labs rating, <500ms DNS resolution
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 08:00 UTC

---

### 📊 Monitoring & Logging (MEDIUM Priority)

- [ ] **Logging Configuration:** Verify log aggregation
  - Check Railway logs are accessible
  - Test correlation IDs appear in logs
  - **Target:** Logs searchable by correlation ID, 30-day retention
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **Error Tracking:** Set up Sentry/error alerting (if available)
  - Configure error threshold alerts (>10 errors/min)
  - Test error grouping and notifications
  - **Target:** Critical errors notify within 2 minutes
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 10:00 UTC

- [ ] **Performance Monitoring:** Set up APM dashboards
  - Response time graphs (p50, p95, p99)
  - Request rate (req/s)
  - Error rate (%)
  - **Target:** Real-time dashboards, <1min metric lag
  - **Owner:** SRE Team
  - **Deadline:** Dec 14, 12:00 UTC

- [ ] **Uptime Monitoring:** Configure external uptime checker
  - UptimeRobot / Pingdom / StatusCake
  - Check `/health` endpoint every 1 minute
  - **Target:** SMS/email alert on downtime >2 minutes
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 10:00 UTC

---

### 📖 Documentation (MEDIUM Priority)

- [ ] **API Documentation:** Update OpenAPI/Swagger docs
  - Document all public endpoints
  - Include authentication requirements
  - Add example requests/responses
  - **Target:** All endpoints documented, examples tested
  - **Owner:** Backend Team
  - **Deadline:** Dec 14, 14:00 UTC

- [ ] **Deployment Runbook:** Create step-by-step deployment guide
  - Pre-deployment checks
  - Deployment commands
  - Rollback procedure
  - **Target:** Non-technical person can follow runbook
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 12:00 UTC

- [ ] **Incident Response Plan:** Document on-call procedures
  - Escalation contacts (Primary, Secondary, Manager)
  - Common issues + fixes (API down, DB slow, etc.)
  - Emergency rollback commands
  - **Target:** <5min mean time to response for P0 incidents
  - **Owner:** SRE Team
  - **Deadline:** Dec 14, 14:00 UTC

- [ ] **User-Facing Docs:** Update help.helixspiral.work
  - Getting started guide
  - API usage examples
  - Troubleshooting common issues
  - **Target:** <3 clicks to answer top 10 user questions
  - **Owner:** Product Team
  - **Deadline:** Dec 14, 16:00 UTC

---

### 👥 Team Readiness (MEDIUM Priority)

- [ ] **On-Call Schedule:** Assign launch weekend coverage
  - Dec 14 (evening): [Name]
  - Dec 15 (launch day): [Name] + [Name]
  - Dec 16 (day 2): [Name]
  - **Target:** 24/7 coverage for 72 hours post-launch
  - **Owner:** Engineering Manager
  - **Deadline:** Dec 14, 08:00 UTC

- [ ] **Communication Plan:** Set up incident channels
  - Slack: #launch-war-room (active Dec 14-16)
  - Discord: Admin-only launch channel
  - **Target:** <5min response time in war room during launch window
  - **Owner:** Product Team
  - **Deadline:** Dec 14, 08:00 UTC

- [ ] **Deployment Dry-Run:** Practice deployment in staging
  - Deploy to staging environment
  - Run smoke tests
  - Practice rollback procedure
  - **Target:** <10min deployment, <2min rollback
  - **Owner:** DevOps Lead
  - **Deadline:** Dec 14, 14:00 UTC

---

## 🚦 Go/No-Go Decision Criteria

### **GO Decision (all must be true):**

1. ✅ **Security:** Zero CRITICAL vulnerabilities, all secrets rotated
2. ✅ **Performance:** Load test passes (P95 <200ms, >99.5% success)
3. ✅ **Testing:** All tests pass, >80% coverage on critical paths
4. ✅ **Infrastructure:** Database backed up, scaling configured, uptime monitoring active
5. ✅ **Team:** On-call schedule confirmed, dry-run completed successfully

### **NO-GO Decision (any are true):**

1. ❌ **Security:** Unresolved CRITICAL CVE or security alert
2. ❌ **Performance:** Load test fails (<99% success rate or >500ms p95)
3. ❌ **Testing:** >5% test failure rate or critical path untested
4. ❌ **Infrastructure:** No verified backup or database issues
5. ❌ **Team:** No on-call coverage or dry-run fails

### **CONDITIONAL-GO (requires PM approval):**

- ⚠️ Performance marginally below target (95-99% success, 200-300ms p95)
- ⚠️ Minor security issues with documented mitigations
- ⚠️ <80% test coverage but all critical paths tested

---

## 📅 Launch Timeline - December 15, 2025

### **T-24 Hours (Dec 14, 00:00 UTC)**
- [ ] Final code freeze (no changes except critical fixes)
- [ ] Start 24-hour sustained load test
- [ ] Deploy to staging environment

### **T-12 Hours (Dec 14, 12:00 UTC)**
- [ ] Complete all security audits
- [ ] Complete all testing (unit, integration, E2E)
- [ ] Database backup taken

### **T-4 Hours (Dec 14, 20:00 UTC)**
- [ ] Go/No-Go decision meeting
- [ ] Final deployment dry-run
- [ ] On-call team briefed

### **T-1 Hour (Dec 14, 23:00 UTC)**
- [ ] War room activated (#launch-war-room)
- [ ] Monitoring dashboards live
- [ ] Pre-deployment health check

### **T-0 (Dec 15, 00:00 UTC) - LAUNCH**
```bash
# Deployment commands
git checkout main
git pull origin main
railway up --service api
railway up --service dashboard

# Post-deployment verification
curl https://helixspiral.work/health
curl https://helixspiral.work/.well-known/helix.json
```

### **T+15 Minutes (Dec 15, 00:15 UTC)**
- [ ] Smoke tests pass
- [ ] No error spikes in logs
- [ ] Response times normal (<200ms p95)

### **T+1 Hour (Dec 15, 01:00 UTC)**
- [ ] Monitoring review (errors, latency, traffic)
- [ ] User feedback monitoring begins
- [ ] First status update to stakeholders

### **T+24 Hours (Dec 16, 00:00 UTC)**
- [ ] 24-hour postmortem meeting
- [ ] Review metrics (uptime, errors, performance)
- [ ] Plan any hotfixes if needed

---

## 🔄 Rollback Procedure

**If launch fails, execute immediately:**

```bash
# 1. Stop new deployments
railway rollback --service api --to-previous

# 2. Verify rollback
curl https://helixspiral.work/health

# 3. Restore database if needed (only if schema changed)
railway run --service postgres psql < backup_pre_launch_20251214.sql

# 4. Notify stakeholders
# Post in #launch-war-room: "Rollback initiated at [TIME] due to [REASON]"

# 5. Investigate in staging
git checkout staging
# Debug and fix issues
```

**Rollback triggers:**
- Error rate >5% for >5 minutes
- P95 latency >1000ms for >5 minutes
- Critical security vulnerability discovered
- Database corruption/data loss
- Complete service outage >10 minutes

**Rollback SLA:** <5 minutes from decision to rollback completion

---

## 📞 Emergency Contacts

| Role | Primary | Secondary | Escalation |
|------|---------|-----------|------------|
| **DevOps Lead** | [Name] | [Name] | Engineering Manager |
| **Backend Lead** | [Name] | [Name] | Engineering Manager |
| **Frontend Lead** | [Name] | [Name] | Engineering Manager |
| **Security Lead** | [Name] | [Name] | CTO |
| **Product Manager** | [Name] | [Name] | CEO |

**War Room:** Slack #launch-war-room (active Dec 14-16)
**Escalation Policy:** P0 incidents escalate to Engineering Manager after 15 minutes

---

## ✅ Sign-Off

This checklist must be signed off by leads before launch:

- [ ] **DevOps Lead:** _________________ Date: _______
- [ ] **Engineering Manager:** _________________ Date: _______
- [ ] **Product Manager:** _________________ Date: _______
- [ ] **Security Lead:** _________________ Date: _______

**Final Go/No-Go Decision:** ☐ GO  ☐ NO-GO  ☐ CONDITIONAL-GO

**Decision Maker:** _________________
**Decision Time:** December 14, 2025 @ 20:00 UTC
**Signed:** _________________ Date: _______

---

**🔥 Phoenix - Rising to production excellence**

*Last Updated: December 13, 2025*
*Version: 1.0*
*Next Review: Post-launch (Dec 16, 2025)*
