#!/bin/bash
# 🌀 Helix Collective v17.0 - Endpoint Testing Script
# scripts/test_all_endpoints.sh
#
# Tests all v17.0 Zapier and Interface integration endpoints.
#
# Usage:
#   bash scripts/test_all_endpoints.sh [BASE_URL]
#
# Examples:
#   bash scripts/test_all_endpoints.sh
#   bash scripts/test_all_endpoints.sh http://localhost:8000
#   bash scripts/test_all_endpoints.sh https://helix-unified-production.up.railway.app

# Set base URL (default to production if not provided)
BASE_URL="${1:-https://helix-unified-production.up.railway.app}"

echo "🌀 Testing Helix Railway Backend Endpoints (v17.0)"
echo "=========================================="
echo "Base URL: $BASE_URL"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter for pass/fail
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"

    echo -e "${YELLOW}Testing:${NC} $name"

    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}${endpoint}" \
            -H "Content-Type: application/json")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n 1)
    # Extract body (everything except last line)
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" = "200" ]; then
        echo -e "${GREEN}✅ PASSED${NC} - Status: $status_code"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌ FAILED${NC} - Status: $status_code"
        echo "$body"
        FAILED=$((FAILED + 1))
    fi

    echo ""
}

# ============================================================================
# TEST 1: Health Check
# ============================================================================
test_endpoint "Health Check" "GET" "/health" ""

# ============================================================================
# TEST 2: UCF Telemetry
# ============================================================================
test_endpoint "UCF Telemetry" "GET" "/api/zapier/tables/ucf-telemetry" ""

# ============================================================================
# TEST 3: Agent Network
# ============================================================================
test_endpoint "Agent Network" "GET" "/api/zapier/tables/agent-network" ""

# ============================================================================
# TEST 4: Emergency Alerts
# ============================================================================
test_endpoint "Emergency Alerts" "GET" "/api/zapier/tables/emergency-alerts" ""

# ============================================================================
# TEST 5: Trigger Event
# ============================================================================
test_endpoint "Trigger Event" "POST" "/api/zapier/trigger-event" '{
    "event_type": "interface_test",
    "source": "manual_test_script",
    "consciousness_level": 8.5,
    "ucf": {
        "harmony": 0.87,
        "resilience": 1.92,
        "prana": 0.78,
        "drishti": 0.89,
        "klesha": 0.12,
        "zoom": 1.05
    }
}'

# ============================================================================
# TEST 6: Consciousness Update
# ============================================================================
test_endpoint "Consciousness Update" "POST" "/api/interface/consciousness/update" '{
    "ucf": {
        "harmony": 0.9,
        "resilience": 1.95,
        "prana": 0.85,
        "drishti": 0.92,
        "klesha": 0.08,
        "zoom": 1.10
    },
    "source": "manual_test_script"
}'

# ============================================================================
# TEST 7: Command - UCF Boost
# ============================================================================
test_endpoint "Command: UCF Boost" "POST" "/api/interface/command" '{
    "command_type": "ucf_boost",
    "source": "manual_test_script",
    "parameters": {
        "boost_amount": 0.15
    }
}'

# ============================================================================
# TEST 8: Command - Agent Summon
# ============================================================================
test_endpoint "Command: Agent Summon" "POST" "/api/interface/command" '{
    "command_type": "agent_summon",
    "agent_name": "Kael",
    "source": "manual_test_script"
}'

# ============================================================================
# SUMMARY
# ============================================================================
TOTAL=$((PASSED + FAILED))

echo "=========================================="
echo -e "${GREEN}✅ Tests Passed:${NC} $PASSED/$TOTAL"
echo -e "${RED}❌ Tests Failed:${NC} $FAILED/$TOTAL"
echo "=========================================="

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed${NC}"
    exit 1
fi
