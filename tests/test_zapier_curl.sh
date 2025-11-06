#!/bin/bash
# Zapier Master Webhook - Quick Curl Tests
# ========================================
# Test all 7 routing paths with simple curl commands

# Check if ZAPIER_MASTER_HOOK_URL is set
if [ -z "$ZAPIER_MASTER_HOOK_URL" ]; then
    echo "❌ Error: ZAPIER_MASTER_HOOK_URL environment variable not set"
    echo ""
    echo "Set it with:"
    echo "  export ZAPIER_MASTER_HOOK_URL='https://hooks.zapier.com/hooks/catch/xxxxx/master'"
    exit 1
fi

echo "🌀 Helix Collective - Zapier Master Webhook Curl Tests"
echo "======================================================"
echo "Webhook URL: ${ZAPIER_MASTER_HOOK_URL:0:50}..."
echo ""

# Function to test a webhook path
test_path() {
    local path_name=$1
    local payload=$2

    echo "🧪 Testing: $path_name"
    response=$(curl -s -X POST "$ZAPIER_MASTER_HOOK_URL" \
      -H "Content-Type: application/json" \
      -d "$payload" \
      -w "\nHTTP_CODE:%{http_code}")

    http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)

    if [ "$http_code" = "200" ]; then
        echo "   ✅ PASS (HTTP $http_code)"
    else
        echo "   ❌ FAIL (HTTP $http_code)"
    fi
    echo ""
    sleep 1  # Rate limiting
}

echo "📅 WEEK 1: Core Monitoring (FREE TIER)"
echo "======================================================"
echo ""

# Week 1: Test Event Log (Path A)
test_path "Path A: Event Log" '{
  "type": "event_log",
  "event_title": "Test Event from Curl",
  "event_type": "System",
  "agent_name": "TestAgent",
  "description": "Testing event log path with curl",
  "ucf_snapshot": "{\"harmony\":0.75,\"zoom\":1.02}",
  "timestamp": "'$(date -Iseconds)'",
  "environment": "test"
}'

# Week 1: Test Agent Registry (Path B)
test_path "Path B: Agent Registry" '{
  "type": "agent_registry",
  "agent_name": "Manus",
  "status": "Active",
  "last_action": "Running curl test",
  "health_score": 95,
  "last_updated": "'$(date -Iseconds)'"
}'

# Week 1: Test System State (Path C)
test_path "Path C: System State" '{
  "type": "system_state",
  "component": "Test Suite",
  "status": "Testing",
  "harmony": "0.88",
  "error_log": "",
  "verified": true
}'

echo "📅 WEEK 2-4: Advanced Features (ZAPIER PRO)"
echo "======================================================"
echo ""

# Week 2: Test Telemetry (Path E)
test_path "Path E: Telemetry" '{
  "type": "telemetry",
  "metric_name": "test_curl_latency",
  "value": 42.5,
  "component": "Curl Test Suite",
  "harmony": "0.75",
  "metadata": "{\"test\":true}",
  "timestamp": "'$(date -Iseconds)'"
}'

# Week 3: Test Discord Notification (Path D)
test_path "Path D: Discord Notification" '{
  "type": "discord_notification",
  "channel_name": "status",
  "message": "Test notification from curl script",
  "priority": "normal",
  "channel_id": "123456789"
}'

# Week 3: Test Error Alert (Path F)
test_path "Path F: Error Alert" '{
  "type": "error",
  "error_message": "Test error alert - not a real error",
  "component": "curl_test",
  "severity": "low",
  "context": "{\"test\":true}",
  "stack_trace": "",
  "affected_channels": ["status"]
}'

# Week 4: Test Repository Action (Path G)
test_path "Path G: Repository Action" '{
  "type": "repository",
  "repo_name": "helix-unified",
  "action": "test_curl",
  "details": "Testing repository webhook path",
  "commit_hash": "test123abc",
  "mega_backup_status": "unknown",
  "archive_path": "/tmp"
}'

echo "✅ All curl tests completed!"
echo ""
echo "💡 Next steps:"
echo "  1. Check your Zapier dashboard for test events"
echo "  2. Verify data appears in Notion, Slack, etc."
echo "  3. Run Python test suite: python tests/test_zapier_webhook.py --all"
