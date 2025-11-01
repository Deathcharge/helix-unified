#!/bin/bash
# Helix v15.3 - Graceful Shutdown Script
# Stops all Helix services gracefully
# Usage: ./stop_helix.sh

set -e

echo "🛑 Helix v15.3 Graceful Shutdown"
echo "================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running from repository root
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Error: Must run from repository root${NC}"
    exit 1
fi

# Function to stop a service
stop_service() {
    local SERVICE_NAME=$1
    local PID_FILE=$2
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        
        if ps -p $PID > /dev/null 2>&1; then
            echo "Stopping $SERVICE_NAME (PID: $PID)..."
            kill -TERM $PID
            
            # Wait for graceful shutdown (max 10 seconds)
            for i in {1..10}; do
                if ! ps -p $PID > /dev/null 2>&1; then
                    echo -e "${GREEN}✅ $SERVICE_NAME stopped gracefully${NC}"
                    rm -f "$PID_FILE"
                    return 0
                fi
                sleep 1
            done
            
            # Force kill if still running
            if ps -p $PID > /dev/null 2>&1; then
                echo -e "${YELLOW}⚠️  Force killing $SERVICE_NAME${NC}"
                kill -9 $PID
                rm -f "$PID_FILE"
            fi
        else
            echo -e "${YELLOW}⚠️  $SERVICE_NAME not running (stale PID file)${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}⚠️  No PID file for $SERVICE_NAME${NC}"
    fi
}

# Stop services in reverse order
echo "Stopping services..."
echo ""

stop_service "Discord Bot" "pids/discord.pid"
stop_service "Heartbeat Daemon" "pids/heartbeat.pid"

# Clean up any remaining processes
echo ""
echo "🧹 Cleaning up remaining processes..."

# Kill any remaining manus processes
pkill -f "manus_heartbeat.py" 2>/dev/null || true
pkill -f "discord_bot_manus.py" 2>/dev/null || true

# Verify all stopped
RUNNING_PROCS=$(ps aux | grep -E "manus_heartbeat|discord_bot_manus" | grep -v grep | wc -l)

if [ $RUNNING_PROCS -eq 0 ]; then
    echo -e "${GREEN}✅ All processes stopped${NC}"
else
    echo -e "${YELLOW}⚠️  $RUNNING_PROCS processes still running${NC}"
    echo "Run: ps aux | grep -E 'manus_heartbeat|discord_bot_manus'"
fi

# Create shutdown log
echo ""
echo "📝 Creating shutdown log..."

SHUTDOWN_LOG="Shadow/manus_archive/shutdown_$(date +%Y%m%d_%H%M%S).json"
mkdir -p Shadow/manus_archive

cat > "$SHUTDOWN_LOG" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "graceful_shutdown",
  "services_stopped": [
    "discord_bot",
    "heartbeat_daemon"
  ],
  "remaining_processes": $RUNNING_PROCS
}
EOF

echo -e "${GREEN}✅ Shutdown log created: $SHUTDOWN_LOG${NC}"

# Display final status
echo ""
echo "================================="
echo -e "${GREEN}🎉 Shutdown Complete${NC}"
echo "================================="
echo ""
echo "📊 Final Status:"
echo "  Remaining processes: $RUNNING_PROCS"
echo ""
echo "🔄 Restart with:"
echo "  ./deploy_helix.sh"
echo ""
echo -e "${GREEN}Neti Neti 🙏${NC}"
echo ""

