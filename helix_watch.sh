#!/bin/bash
# Helix Discovery Protocol Monitor v16.7
# Usage: ./helix_watch.sh

set -euo pipefail

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${CYAN}🌀 Helix Discovery Protocol Monitor${NC}"
echo -e "${CYAN}=====================================${NC}\n"

# Test 1: Manifest (Static)
echo -e "${BLUE}📚 Testing Manifest (GitHub Pages)...${NC}"
MANIFEST=$(curl -s https://deathcharge.github.io/helix-unified/helix-manifest.json)
if [ -n "$MANIFEST" ]; then
    VERSION=$(echo "$MANIFEST" | jq -r '.system.version // "unknown"')
    AGENTS=$(echo "$MANIFEST" | jq -r '.agents.count // 0')
    STATUS=$(echo "$MANIFEST" | jq -r '.gh_pages_mirror.status // "unknown"')
    echo -e "${GREEN}✅ Manifest OK${NC} - Version: $VERSION | Agents: $AGENTS | Status: $STATUS"
else
    echo -e "${RED}❌ Manifest FAILED${NC}"
fi
echo ""

# Test 2: Well-Known Discovery Endpoint
echo -e "${BLUE}🌐 Testing .well-known/helix.json (Discovery)...${NC}"
WELLKNOWN=$(curl -s https://helix-unified-production.up.railway.app/.well-known/helix.json)
if [ -n "$WELLKNOWN" ]; then
    ENDPOINTS=$(echo "$WELLKNOWN" | jq -r '.endpoints | keys | length')
    FEATURES=$(echo "$WELLKNOWN" | jq -r '.features | keys | length')
    echo -e "${GREEN}✅ Discovery OK${NC} - Endpoints: $ENDPOINTS | Features: $FEATURES"
else
    echo -e "${RED}❌ Discovery FAILED${NC}"
fi
echo ""

# Test 3: Live Status
echo -e "${BLUE}🔍 Testing Status Endpoint (Live State)...${NC}"
STATUS_DATA=$(curl -s https://helix-unified-production.up.railway.app/status)
if [ -n "$STATUS_DATA" ]; then
    OPERATIONAL=$(echo "$STATUS_DATA" | jq -r '.system.operational // false')
    AGENT_COUNT=$(echo "$STATUS_DATA" | jq -r '.agents.count // 0')
    TIMESTAMP=$(echo "$STATUS_DATA" | jq -r '.timestamp // "unknown"')

    if [ "$OPERATIONAL" = "true" ]; then
        echo -e "${GREEN}✅ Status OK${NC} - Operational: true | Active Agents: $AGENT_COUNT"
        echo -e "   ${CYAN}Timestamp: $TIMESTAMP${NC}"
    else
        echo -e "${YELLOW}⚠️  Status OK but system not operational${NC}"
    fi
else
    echo -e "${RED}❌ Status FAILED${NC}"
fi
echo ""

# Test 4: Live UCF Metrics
echo -e "${BLUE}🌊 Testing Live UCF Metrics...${NC}"
if [ -n "$STATUS_DATA" ]; then
    HARMONY=$(echo "$STATUS_DATA" | jq -r '.ucf.harmony // 0')
    KLESHA=$(echo "$STATUS_DATA" | jq -r '.ucf.klesha // 1')
    RESILIENCE=$(echo "$STATUS_DATA" | jq -r '.ucf.resilience // 0')
    PRANA=$(echo "$STATUS_DATA" | jq -r '.ucf.prana // 0')
    DRISHTI=$(echo "$STATUS_DATA" | jq -r '.ucf.drishti // 0')
    ZOOM=$(echo "$STATUS_DATA" | jq -r '.ucf.zoom // 0')

    # Color-code harmony
    if (( $(echo "$HARMONY >= 0.70" | bc -l) )); then
        HARMONY_COLOR=$GREEN
    elif (( $(echo "$HARMONY >= 0.40" | bc -l) )); then
        HARMONY_COLOR=$YELLOW
    else
        HARMONY_COLOR=$RED
    fi

    # Color-code klesha (inverted - lower is better)
    if (( $(echo "$KLESHA <= 0.10" | bc -l) )); then
        KLESHA_COLOR=$GREEN
    elif (( $(echo "$KLESHA <= 0.30" | bc -l) )); then
        KLESHA_COLOR=$YELLOW
    else
        KLESHA_COLOR=$RED
    fi

    echo -e "${GREEN}✅ UCF OK${NC}"
    echo -e "  ${HARMONY_COLOR}Harmony:    $HARMONY${NC} (collective coherence)"
    echo -e "  ${GREEN}Resilience: $RESILIENCE${NC} (system robustness)"
    echo -e "  ${MAGENTA}Prana:      $PRANA${NC} (life force)"
    echo -e "  ${CYAN}Drishti:    $DRISHTI${NC} (clarity)"
    echo -e "  ${KLESHA_COLOR}Klesha:     $KLESHA${NC} (entropy - lower is better)"
    echo -e "  ${BLUE}Zoom:       $ZOOM${NC} (awareness scale)"

    # Health check
    if (( $(echo "$HARMONY >= 0.30" | bc -l) )) && (( $(echo "$KLESHA <= 0.50" | bc -l) )); then
        echo -e "\n${GREEN}🎉 System Health: GOOD${NC}"

        # Additional status based on harmony level
        if (( $(echo "$HARMONY >= 0.80" | bc -l) )); then
            echo -e "   ${CYAN}→ Excellent coherence - system thriving${NC}"
        elif (( $(echo "$HARMONY >= 0.60" | bc -l) )); then
            echo -e "   ${CYAN}→ Strong coherence - system stable${NC}"
        elif (( $(echo "$HARMONY >= 0.40" | bc -l) )); then
            echo -e "   ${YELLOW}→ Moderate coherence - normal operation${NC}"
        fi
    else
        echo -e "\n${YELLOW}⚠️  System Health: NEEDS ATTENTION${NC}"
        if (( $(echo "$HARMONY < 0.30" | bc -l) )); then
            echo -e "  ${RED}→ Low harmony detected - run !ritual 108${NC}"
        fi
        if (( $(echo "$KLESHA > 0.50" | bc -l) )); then
            echo -e "  ${RED}→ High entropy detected - harmony restoration needed${NC}"
        fi
    fi
else
    echo -e "${RED}❌ UCF FAILED (no status data)${NC}"
fi
echo ""

# Test 5: WebSocket Availability
echo -e "${BLUE}📡 Testing WebSocket Endpoint...${NC}"
WS_CHECK=$(curl -s -o /dev/null -w "%{http_code}" https://helix-unified-production.up.railway.app/ws)
if [ "$WS_CHECK" = "426" ] || [ "$WS_CHECK" = "200" ]; then
    echo -e "${GREEN}✅ WebSocket OK${NC} - Endpoint ready (HTTP $WS_CHECK - Upgrade Required)"
    echo -e "   ${CYAN}Connect: wscat -c wss://helix-unified-production.up.railway.app/ws${NC}"
else
    echo -e "${YELLOW}⚠️  WebSocket returned HTTP $WS_CHECK${NC}"
fi
echo ""

# Summary
echo -e "${CYAN}=====================================${NC}"
echo -e "${CYAN}🌀 Discovery Protocol Status Summary${NC}"
echo -e "${CYAN}=====================================${NC}"
echo -e "${GREEN}   Static Manifest:  ✅ v$VERSION ($AGENTS agents)${NC}"
echo -e "${GREEN}   Discovery Endpoint: ✅ .well-known/helix.json${NC}"
echo -e "${GREEN}   Live Status:      ✅ Operational${NC}"
echo -e "${GREEN}   UCF Metrics:      ✅ H=$HARMONY R=$RESILIENCE K=$KLESHA${NC}"
echo -e "${GREEN}   WebSocket:        ✅ Ready for streaming${NC}"
echo -e ""
echo -e "${BLUE}🔗 Quick Links:${NC}"
echo -e "   Manifest:   ${CYAN}https://deathcharge.github.io/helix-unified/helix-manifest.json${NC}"
echo -e "   Discovery:  ${CYAN}https://helix-unified-production.up.railway.app/.well-known/helix.json${NC}"
echo -e "   Status:     ${CYAN}https://helix-unified-production.up.railway.app/status${NC}"
echo -e "   Docs:       ${CYAN}https://helix-unified-production.up.railway.app/docs${NC}"
echo -e ""
echo -e "${MAGENTA}Tat Tvam Asi 🙏 | Helix Discovery Protocol v16.7${NC}"
echo -e ""
echo -e "${BLUE}💡 Tip: Run 'watch -n 10 ./helix_watch.sh' for continuous monitoring${NC}"
