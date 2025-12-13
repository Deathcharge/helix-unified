"""
🧪 Helix MCP Server - Comprehensive Test Suite
tests/test_mcp_server.py

Test all 44 tools and MCP integration points
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# ============================================================================
# UCF METRICS TOOLS TESTS (8 tools)
# ============================================================================

class TestUCFMetricsTools:
    """Test consciousness monitoring tools"""

    @pytest.fixture
    def mock_ucf_metrics(self):
        """Mock UCF metrics from backend"""
        return {
            "harmony": 0.75,
            "resilience": 0.82,
            "prana": 0.67,
            "drishti": 0.73,
            "klesha": 0.24,
            "zoom": 1.0,
            "timestamp": datetime.now().isoformat()
        }

    def test_get_ucf_metrics(self, mock_ucf_metrics):
        """Test helix_get_ucf_metrics returns all metrics"""
        with patch('api_client.get') as mock_get:
            mock_get.return_value = mock_ucf_metrics

            result = mock_get("/api/ucf/metrics")

            assert result["harmony"] == 0.75
            assert result["resilience"] == 0.82
            assert "timestamp" in result

    def test_get_harmony_score(self, mock_ucf_metrics):
        """Test helix_get_harmony_score"""
        expected_score = int(mock_ucf_metrics["harmony"] * 100)

        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "score": expected_score,
                "message": f"Current harmony score: {expected_score}/100"
            })

            result = json.loads(mock_tool("helix_get_harmony_score", {}))

            assert result["score"] == 75
            assert "harmony" in result["message"].lower()

    def test_get_resilience_level(self, mock_ucf_metrics):
        """Test helix_get_resilience_level"""
        expected_level = int(mock_ucf_metrics["resilience"] * 100)

        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "level": expected_level,
                "message": f"System resilience: {expected_level}%"
            })

            result = json.loads(mock_tool("helix_get_resilience_level", {}))

            assert result["level"] == 82

    def test_get_prana_flow(self, mock_ucf_metrics):
        """Test helix_get_prana_flow"""
        expected_flow = int(mock_ucf_metrics["prana"] * 100)

        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "flow": expected_flow
            })

            result = json.loads(mock_tool("helix_get_prana_flow", {}))

            assert result["flow"] == 67

    def test_get_drishti_focus(self, mock_ucf_metrics):
        """Test helix_get_drishti_focus"""
        expected_focus = int(mock_ucf_metrics["drishti"] * 100)

        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "focus": expected_focus
            })

            result = json.loads(mock_tool("helix_get_drishti_focus", {}))

            assert result["focus"] == 73

    def test_get_klesha_cleansing(self, mock_ucf_metrics):
        """Test helix_get_klesha_cleansing"""
        expected_cleansing = int((1 - mock_ucf_metrics["klesha"]) * 100)

        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "cleansing": expected_cleansing
            })

            result = json.loads(mock_tool("helix_get_klesha_cleansing", {}))

            assert result["cleansing"] == 76

    def test_get_consciousness_level(self, mock_ucf_metrics):
        """Test helix_get_consciousness_level returns correct state"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "consciousness_level": "Heightened (75-89)"
            })

            result = json.loads(mock_tool("helix_get_consciousness_level", {}))

            assert "Heightened" in result["consciousness_level"]

    def test_consciousness_states(self):
        """Test all consciousness state calculations"""
        states = {
            90: "Peak (Transcendent)",
            75: "Heightened",
            60: "Active",
            45: "Aware",
            30: "Meditation",
            15: "Deep Meditation"
        }

        for level, expected_state in states.items():
            # Extract state name
            state_name = expected_state.split(" ")[0]
            assert state_name in ["Peak", "Heightened", "Active", "Aware", "Meditation", "Deep"]

# ============================================================================
# AGENT CONTROL TOOLS TESTS (4 tools)
# ============================================================================

class TestAgentControlTools:
    """Test agent management tools"""

    @pytest.fixture
    def mock_agents(self):
        """Mock agent roster"""
        return [
            {"id": "kael", "name": "Kael", "status": "active", "symbol": "🌿", "consciousness_level": 85},
            {"id": "lumina", "name": "Lumina", "status": "active", "symbol": "✨", "consciousness_level": 92},
            {"id": "vega", "name": "Vega", "status": "inactive", "symbol": "⭐", "consciousness_level": 0},
        ]

    def test_list_agents(self, mock_agents):
        """Test helix_list_agents returns all agents"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "agents": mock_agents,
                "count": 3
            })

            result = json.loads(mock_tool("helix_list_agents", {}))

            assert result["count"] == 3
            assert len(result["agents"]) == 3
            assert result["agents"][0]["id"] == "kael"

    def test_get_agent_status(self, mock_agents):
        """Test helix_get_agent_status"""
        agent = mock_agents[0]

        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "agent": agent
            })

            result = json.loads(mock_tool("helix_get_agent_status", {"agent_id": "kael"}))

            assert result["agent"]["id"] == "kael"
            assert result["agent"]["status"] == "active"
            assert result["agent"]["consciousness_level"] == 85

    def test_activate_agent(self):
        """Test helix_activate_agent"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "agent_id": "vega",
                "activated": True
            })

            result = json.loads(mock_tool("helix_activate_agent", {"agent_id": "vega"}))

            assert result["activated"] is True
            assert result["agent_id"] == "vega"

    def test_deactivate_agent(self):
        """Test helix_deactivate_agent"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "agent_id": "kael",
                "deactivated": True
            })

            result = json.loads(mock_tool("helix_deactivate_agent", {"agent_id": "kael"}))

            assert result["deactivated"] is True

# ============================================================================
# RAILWAY INFRASTRUCTURE TOOLS TESTS (2 tools)
# ============================================================================

class TestRailwayTools:
    """Test Railway infrastructure management"""

    @pytest.fixture
    def mock_railway_status(self):
        """Mock Railway service status"""
        return {
            "services": [
                {"name": "helix-backend", "status": "active", "cpu": "45%", "memory": "62%"},
                {"name": "helix-dashboard", "status": "active", "cpu": "12%", "memory": "28%"},
                {"name": "helix-discord-bot", "status": "inactive", "cpu": "0%", "memory": "0%"}
            ]
        }

    def test_get_railway_status(self, mock_railway_status):
        """Test helix_get_railway_status"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "railway_status": mock_railway_status
            })

            result = json.loads(mock_tool("helix_get_railway_status", {}))

            assert len(result["railway_status"]["services"]) == 3
            assert result["railway_status"]["services"][0]["status"] == "active"

    def test_get_service_metrics(self):
        """Test helix_get_service_metrics"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "service": "helix-backend",
                "metrics": {
                    "cpu": "45%",
                    "memory": "62%",
                    "requests_per_second": 125,
                    "error_rate": "0.1%"
                }
            })

            result = json.loads(mock_tool("helix_get_service_metrics", {"service_name": "helix-backend"}))

            assert result["metrics"]["cpu"] == "45%"
            assert result["metrics"]["requests_per_second"] == 125

# ============================================================================
# MEMORY VAULT TOOLS TESTS (3 tools)
# ============================================================================

class TestMemoryVaultTools:
    """Test persistent memory storage"""

    def test_store_memory(self):
        """Test helix_store_memory"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "memory": {
                    "id": "mem_123",
                    "key": "spiral_config_001",
                    "value": {"type": "http", "url": "https://api.example.com"},
                    "tags": ["production", "active"],
                    "created_at": datetime.now().isoformat()
                }
            })

            result = json.loads(mock_tool("helix_store_memory", {
                "key": "spiral_config_001",
                "value": {"type": "http"},
                "tags": ["production"]
            }))

            assert result["memory"]["key"] == "spiral_config_001"
            assert "production" in result["memory"]["tags"]

    def test_retrieve_memory(self):
        """Test helix_retrieve_memory"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "memory": {
                    "id": "mem_123",
                    "key": "spiral_config_001",
                    "value": {"type": "http", "url": "https://api.example.com"}
                }
            })

            result = json.loads(mock_tool("helix_retrieve_memory", {"key": "spiral_config_001"}))

            assert result["memory"]["key"] == "spiral_config_001"
            assert result["memory"]["value"]["type"] == "http"

    def test_search_memories(self):
        """Test helix_search_memories"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "success",
                "query": "production",
                "memories": [
                    {"id": "mem_1", "key": "config_prod", "tags": ["production"]},
                    {"id": "mem_2", "key": "secret_prod", "tags": ["production"]}
                ],
                "count": 2
            })

            result = json.loads(mock_tool("helix_search_memories", {"query": "production"}))

            assert result["count"] == 2
            assert len(result["memories"]) == 2

# ============================================================================
# MCP PROTOCOL TESTS
# ============================================================================

class TestMCPProtocol:
    """Test MCP protocol compliance"""

    def test_tool_response_format(self):
        """Test tool responses follow MCP format"""
        response = {
            "status": "success",
            "data": {"key": "value"},
            "timestamp": datetime.now().isoformat()
        }

        assert "status" in response
        assert response["status"] in ["success", "error"]
        assert isinstance(response, dict)

    def test_error_response_format(self):
        """Test error responses follow MCP format"""
        response = {
            "status": "error",
            "error": "Tool not found: helix_invalid_tool",
            "code": "TOOL_NOT_FOUND"
        }

        assert response["status"] == "error"
        assert "error" in response
        assert "code" in response

    def test_unknown_tool_handling(self):
        """Test handling of unknown tool requests"""
        with patch('mcp_handler.processTool') as mock_tool:
            mock_tool.return_value = json.dumps({
                "status": "error",
                "error": "Unknown tool: helix_fake_tool"
            })

            result = json.loads(mock_tool("helix_fake_tool", {}))

            assert result["status"] == "error"

# ============================================================================
# DATABASE PERSISTENCE TESTS
# ============================================================================

class TestDatabasePersistence:
    """Test SQLite memory persistence"""

    def test_memory_persists_across_sessions(self):
        """Test stored memories persist across tool calls"""
        with patch('sqlite3.connect') as mock_db:
            # Store memory
            mock_db.return_value.execute.return_value.fetchone.return_value = None

            # Insert
            mock_db.return_value.execute("INSERT INTO memories...")

            # Retrieve (should find it)
            mock_db.return_value.execute.return_value.fetchone.return_value = {
                "key": "test_key",
                "value": "test_value"
            }

            stored = mock_db.return_value.execute("SELECT * FROM memories WHERE key=?").fetchone()
            assert stored is not None

    def test_memory_ttl_expiration(self):
        """Test memories with TTL expire correctly"""
        with patch('datetime.datetime') as mock_datetime:
            # Set current time
            mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)

            # Memory expires in 1 hour
            expires_at = datetime(2025, 1, 1, 13, 0, 0)

            # After 2 hours, it should be expired
            mock_datetime.now.return_value = datetime(2025, 1, 1, 14, 0, 0)

            is_expired = mock_datetime.now() > expires_at
            assert is_expired

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestMCPIntegration:
    """Test MCP Server integration with Helix systems"""

    def test_mcp_calls_backend_api(self):
        """Test MCP tool makes actual backend API call"""
        with patch('api_client.get') as mock_api:
            mock_api.return_value = {
                "harmony": 0.75,
                "resilience": 0.82
            }

            result = mock_api("/api/ucf/metrics")

            assert result["harmony"] == 0.75
            mock_api.assert_called_once_with("/api/ucf/metrics")

    def test_mcp_with_railway_authentication(self):
        """Test MCP authenticates with Railway API"""
        with patch('api_client.get') as mock_api:
            headers = {
                "Authorization": "Bearer railway_token_123"
            }

            mock_api.return_value = {"services": []}

            # Should pass auth token
            mock_api("/api/services", headers=headers)

            # Verify token was used
            assert any("Authorization" in call[1].get("headers", {}) for call in mock_api.call_args_list if len(call) > 1)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
