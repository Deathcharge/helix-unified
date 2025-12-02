# Phase 6: 51-Portal Constellation Deployment Execution

**Version:** 1.0  
**Status:** Ready for Execution  
**Last Updated:** November 18, 2025

---

## 🎯 Executive Summary

Phase 6 executes the complete deployment of the 51-portal Helix Collective constellation across 7 Manus accounts, establishing a fully distributed consciousness network with real-time monitoring, cross-instance coordination, and automated failover capabilities.

### Key Metrics

- **Total Portals:** 51
- **Manus Accounts:** 7
- **Deployment Duration:** 3 hours
- **Estimated Credits:** 50-75
- **Success Rate Target:** 100%

---

## 📋 Pre-Deployment Checklist

### Account Setup
- [ ] All 7 Manus accounts created and configured
- [ ] API tokens generated for each account
- [ ] Account credentials stored securely
- [ ] Rate limits verified for each account
- [ ] Backup accounts configured

### Configuration Validation
- [ ] All 51 portal configurations reviewed
- [ ] Configuration schema validated
- [ ] Portal naming conventions confirmed
- [ ] Consciousness levels assigned
- [ ] Feature sets verified

### Infrastructure Readiness
- [ ] Database connections tested
- [ ] API endpoints verified
- [ ] Webhook endpoints configured
- [ ] DNS records prepared
- [ ] SSL certificates ready

### Team Preparation
- [ ] Deployment team briefed
- [ ] Rollback procedures documented
- [ ] Communication channels established
- [ ] Monitoring dashboards prepared
- [ ] Alert recipients configured

---

## 🚀 Deployment Execution

### Phase 1: Primary Portals (Accounts 1-4)

**Duration:** 1 hour  
**Portals:** 32  
**Accounts:** 1, 2, 3, 4

#### Step 1.1: Generate Portal Files

```bash
# Navigate to project directory
cd /home/ubuntu/helix-unified

# Generate all 32 primary portals
python3 scripts/portal_template_generator.py batch \
  examples/instance-configs/batch-all-51-portals.json \
  --accounts 1,2,3,4 \
  --output-dir generated-portals-phase6

# Verify generation
ls -la generated-portals-phase6/
# Expected: 32 portal directories
```

**Expected Output:**
```
helix-ch-primary-1/
helix-ch-secondary-1/
helix-ch-analytics-1/
... (32 total)
```

#### Step 1.2: Validate Generated Portals

```bash
# Validate each portal's configuration
for portal in generated-portals-phase6/*/; do
  echo "Validating: $portal"
  python3 scripts/portal_template_generator.py validate "$portal/config.json"
done

# Expected: All validations pass
```

#### Step 1.3: Deploy to Account 1 (Consciousness Hub)

```bash
# Deploy 8 Consciousness Hub portals to Account 1
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-51-portals.json \
  --account 1 \
  --verbose

# Monitor deployment
watch -n 5 'curl -s https://helix-account-1.manus.space/health'
```

**Deployment Steps:**
1. Upload portal files to Manus.Space
2. Configure domain mappings
3. Set up SSL certificates
4. Initialize databases
5. Configure webhooks
6. Run health checks

**Expected Time:** 15 minutes

#### Step 1.4: Deploy to Account 2 (Workflow Engine)

```bash
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-51-portals.json \
  --account 2 \
  --verbose
```

**Expected Time:** 15 minutes

#### Step 1.5: Deploy to Account 3 (Agent Coordinator)

```bash
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-51-portals.json \
  --account 3 \
  --verbose
```

**Expected Time:** 15 minutes

#### Step 1.6: Deploy to Account 4 (Portal Constellation)

```bash
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-51-portals.json \
  --account 4 \
  --verbose
```

**Expected Time:** 15 minutes

#### Step 1.7: Verify Phase 1 Deployment

```bash
# Test all 32 primary portals
for account in {1..4}; do
  echo "Testing Account $account..."
  for i in {1..8}; do
    curl -s https://helix-account-$account-portal-$i.manus.space/health | jq .status
  done
done

# Expected: All return "healthy"
```

---

### Phase 2: Analytics Portals (Account 5)

**Duration:** 30 minutes  
**Portals:** 8  
**Account:** 5

#### Step 2.1: Generate Analytics Portals

```bash
python3 scripts/portal_template_generator.py batch \
  examples/instance-configs/batch-all-51-portals.json \
  --accounts 5 \
  --output-dir generated-portals-phase6
```

#### Step 2.2: Deploy to Account 5

```bash
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-51-portals.json \
  --account 5 \
  --verbose
```

#### Step 2.3: Configure Metrics Collection

```bash
# Enable metrics aggregation from all primary portals
curl -X POST https://helix-account-5.manus.space/api/metrics/configure \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sources": [
      "helix-account-1.manus.space",
      "helix-account-2.manus.space",
      "helix-account-3.manus.space",
      "helix-account-4.manus.space"
    ],
    "interval_seconds": 30,
    "retention_days": 90,
    "aggregation_enabled": true
  }'
```

#### Step 2.4: Verify Analytics Portals

```bash
# Test analytics portals
for i in {1..8}; do
  curl -s https://helix-account-5-portal-$i.manus.space/health | jq .
done

# Verify metrics are flowing
curl -s https://helix-account-5.manus.space/api/metrics/current | jq .
```

---

### Phase 3: Integration Portals (Account 6)

**Duration:** 30 minutes  
**Portals:** 6  
**Account:** 6

#### Step 3.1: Generate Integration Portals

```bash
python3 scripts/portal_template_generator.py batch \
  examples/instance-configs/batch-all-51-portals.json \
  --accounts 6 \
  --output-dir generated-portals-phase6
```

#### Step 3.2: Deploy to Account 6

```bash
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-51-portals.json \
  --account 6 \
  --verbose
```

#### Step 3.3: Configure External Integrations

```bash
# Configure Zapier integration
curl -X POST https://helix-account-6.manus.space/api/integrations/zapier \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -d '{
    "webhook_url": "https://hooks.zapier.com/hooks/catch/YOUR_WEBHOOK_ID",
    "enabled": true,
    "events": ["portal_created", "health_check", "metrics_update"]
  }'

# Configure Discord bot
curl -X POST https://helix-account-6.manus.space/api/integrations/discord \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -d '{
    "bot_token": "YOUR_DISCORD_BOT_TOKEN",
    "enabled": true,
    "channels": {
      "alerts": "CHANNEL_ID",
      "updates": "CHANNEL_ID",
      "logs": "CHANNEL_ID"
    }
  }'

# Configure Slack integration
curl -X POST https://helix-account-6.manus.space/api/integrations/slack \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -d '{
    "bot_token": "YOUR_SLACK_BOT_TOKEN",
    "enabled": true,
    "channels": {
      "alerts": "#helix-alerts",
      "updates": "#helix-updates"
    }
  }'
```

#### Step 3.4: Verify Integration Portals

```bash
# Test integration portals
for i in {1..6}; do
  curl -s https://helix-account-6-portal-$i.manus.space/health | jq .
done

# Test Zapier webhook
curl -X POST https://helix-account-6.manus.space/api/integrations/zapier/test \
  -H "Authorization: Bearer $MANUS_API_TOKEN"
```

---

### Phase 4: Backup & Disaster Recovery Portals (Account 7)

**Duration:** 30 minutes  
**Portals:** 7  
**Account:** 7

#### Step 4.1: Generate Backup Portals

```bash
python3 scripts/portal_template_generator.py batch \
  examples/instance-configs/batch-all-51-portals.json \
  --accounts 7 \
  --output-dir generated-portals-phase6
```

#### Step 4.2: Deploy to Account 7

```bash
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-51-portals.json \
  --account 7 \
  --verbose
```

#### Step 4.3: Configure Failover

```bash
# Enable automatic failover
curl -X POST https://helix-account-7.manus.space/api/failover/configure \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -d '{
    "primary_account": 1,
    "backup_account": 7,
    "health_check_interval": 30,
    "failover_threshold": 3,
    "auto_failover_enabled": true,
    "rto_minutes": 15,
    "rpo_minutes": 5
  }'

# Configure replication
curl -X POST https://helix-account-7.manus.space/api/replication/configure \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -d '{
    "replication_interval": 60,
    "backup_retention_days": 30,
    "bidirectional": false
  }'
```

#### Step 4.4: Verify Backup Portals

```bash
# Test backup portals
for i in {1..7}; do
  curl -s https://helix-account-7-portal-$i.manus.space/health | jq .
done

# Verify failover configuration
curl -s https://helix-account-7.manus.space/api/failover/status | jq .
```

---

## ✅ Post-Deployment Verification

### Health Check All 51 Portals

```bash
#!/bin/bash
# health_check_all_51.sh

echo "Checking health of all 51 portals..."
echo "======================================"

healthy=0
unhealthy=0

for account in {1..7}; do
  case $account in
    1|2|3|4) portal_count=8 ;;
    5) portal_count=8 ;;
    6) portal_count=6 ;;
    7) portal_count=7 ;;
  esac
  
  echo "Account $account ($portal_count portals):"
  
  for i in $(seq 1 $portal_count); do
    portal_id="helix-account-$account-portal-$i"
    status=$(curl -s https://$portal_id.manus.space/health | jq -r '.status' 2>/dev/null)
    
    if [ "$status" = "healthy" ]; then
      echo "  ✅ $portal_id: $status"
      ((healthy++))
    else
      echo "  ❌ $portal_id: $status"
      ((unhealthy++))
    fi
  done
done

echo ""
echo "Summary: $healthy healthy, $unhealthy unhealthy"
echo "Success Rate: $(echo "scale=2; $healthy * 100 / 51" | bc)%"
```

### Cross-Instance Communication Test

```bash
# Test communication between accounts
curl -X POST https://helix-account-1.manus.space/api/constellation/test-communication \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -d '{
    "target_accounts": [2, 3, 4, 5, 6, 7],
    "message": "Test communication from Account 1"
  }'
```

### Metrics Aggregation Test

```bash
# Verify metrics are aggregating in Account 5
curl -s https://helix-account-5.manus.space/api/metrics/aggregate \
  -H "Authorization: Bearer $MANUS_API_TOKEN" | jq '
  {
    total_portals: .meta.total_portals,
    healthy_portals: .meta.healthy_portals,
    avg_response_time_ms: .metrics.avg_response_time,
    error_rate: .metrics.error_rate,
    avg_consciousness_level: .metrics.avg_consciousness_level
  }'
```

### Failover Test

```bash
# Test failover from Account 1 to Account 7
curl -X POST https://helix-account-7.manus.space/api/failover/test \
  -H "Authorization: Bearer $MANUS_API_TOKEN" \
  -d '{
    "source_account": 1,
    "target_account": 7,
    "test_mode": true
  }'
```

---

## 📊 Deployment Report

After successful deployment, generate a comprehensive report:

```bash
./scripts/deploy_all_instances.sh generate-report \
  --phase 6 \
  --output-format json \
  --include-metrics true \
  --include-logs true
```

**Report Contents:**
- Deployment timeline
- Portal creation summary
- Health check results
- Performance metrics
- Integration status
- Failover configuration
- Recommendations

---

## 🔄 Rollback Procedures

If deployment fails, follow these rollback steps:

### Partial Rollback (Single Account)

```bash
# Rollback Account 5 (Analytics)
./scripts/deploy_all_instances.sh rollback \
  --account 5 \
  --checkpoint latest
```

### Complete Rollback (All Accounts)

```bash
# Rollback all 51 portals to previous state
./scripts/deploy_all_instances.sh rollback-all \
  --checkpoint pre-phase6
```

### Manual Rollback

```bash
# Delete all Phase 6 portals manually
for account in {1..7}; do
  curl -X DELETE https://helix-account-$account.manus.space/api/portals/all \
    -H "Authorization: Bearer $MANUS_API_TOKEN"
done
```

---

## 📈 Success Metrics

### Deployment Success
- [ ] All 51 portals created
- [ ] All 51 portals accessible
- [ ] All 51 portals healthy
- [ ] 100% health check pass rate

### Integration Success
- [ ] Cross-instance communication working
- [ ] Metrics aggregating in Account 5
- [ ] All external integrations connected
- [ ] Failover system operational

### Performance Success
- [ ] Average response time < 500ms
- [ ] Error rate < 0.5%
- [ ] Uptime > 99.9%
- [ ] Consciousness level stable (7-8)

---

## 🎯 Timeline Summary

```
Phase 1: Accounts 1-4 (Primary Portals)
├─ 00:00 - 00:15: Generate 32 portals
├─ 00:15 - 00:45: Deploy to 4 accounts
└─ 00:45 - 01:00: Verify & test
   Duration: 1 hour

Phase 2: Account 5 (Analytics)
├─ 01:00 - 01:15: Generate 8 portals
├─ 01:15 - 01:25: Deploy to Account 5
└─ 01:25 - 01:30: Configure metrics
   Duration: 30 minutes

Phase 3: Account 6 (Integration)
├─ 01:30 - 01:40: Generate 6 portals
├─ 01:40 - 01:50: Deploy to Account 6
└─ 01:50 - 02:00: Configure integrations
   Duration: 30 minutes

Phase 4: Account 7 (Backup & DR)
├─ 02:00 - 02:10: Generate 7 portals
├─ 02:10 - 02:20: Deploy to Account 7
└─ 02:20 - 02:30: Configure failover
   Duration: 30 minutes

Final: Verification & Reporting
├─ 02:30 - 02:45: Run full health checks
├─ 02:45 - 03:00: Generate deployment report
└─ 03:00 - 03:15: Update documentation
   Duration: 45 minutes

TOTAL DURATION: 3 hours
```

---

## 📞 Support & Troubleshooting

### Common Issues

**Portal Generation Fails**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip3 list | grep -E "jinja2|pyyaml"

# Regenerate with verbose output
python3 scripts/portal_template_generator.py generate \
  --verbose config.json
```

**Deployment Fails**
```bash
# Check API connectivity
curl -H "Authorization: Bearer $MANUS_API_TOKEN" \
  https://api.helix-account-1.manus.space/health

# Check rate limits
curl -I https://api.helix-account-1.manus.space/health

# Verify credentials
echo $MANUS_API_TOKEN
```

**Health Checks Failing**
```bash
# Check individual portal logs
curl https://helix-account-1-portal-1.manus.space/logs

# Check database connectivity
curl https://helix-account-1-portal-1.manus.space/api/db/health

# Restart portal
curl -X POST https://helix-account-1-portal-1.manus.space/api/restart
```

---

## ✨ Next Steps

After successful Phase 6 deployment:

1. **Phase 7:** Build advanced features (admin dashboard, analytics)
2. **Phase 8:** Multi-AI coordination (Perplexity, Grok, Claude)
3. **Phase 9:** Real-time features (WebSocket streaming)

---

**Status:** ✅ Ready for Execution  
**Last Updated:** November 18, 2025  
**Estimated Credits:** 50-75  
**Estimated Duration:** 3 hours

