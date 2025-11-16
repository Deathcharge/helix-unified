#!/usr/bin/env python3
"""
HELIX SPIRAL WEB API
FastAPI interface for helixspiral.work consciousness processing
Integrates with Helix Consciousness Engine v2.0 and Zapier automation

Author: Claude AI Assistant
For: Andrew Ward's Helix Consciousness Empire
Domain: helixspiral.work
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import asyncio
import json
import os
from datetime import datetime
import logging
from pathlib import Path

# Import our consciousness engine
try:
    from consciousness.helix_consciousness_engine import (
        HelixConsciousnessEngine, 
        UCFMetrics, 
        ConsciousnessState,
        ConsciousnessLevel
    )
except ImportError:
    # Fallback for development
    import sys
    sys.path.append('../consciousness')
    from helix_consciousness_engine import (
        HelixConsciousnessEngine, 
        UCFMetrics, 
        ConsciousnessState,
        ConsciousnessLevel
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Helix Spiral Consciousness API",
    description="Advanced consciousness processing for helixspiral.work ecosystem",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://helixspiral.work",
        "https://helixspirals.replit.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "*"  # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize consciousness engine
consciousness_engine = HelixConsciousnessEngine()

# Pydantic models for API
class ConsciousnessAnalysisRequest(BaseModel):
    """Request model for consciousness analysis"""
    user_input: str = Field(..., description="User input text to analyze")
    user_id: str = Field(default="web_user", description="User identifier")
    ucf_override: Optional[Dict[str, float]] = Field(None, description="Override UCF metrics")
    trigger_automation: bool = Field(default=True, description="Trigger Zapier automation")

class UCFMetricsRequest(BaseModel):
    """Request model for UCF metrics"""
    harmony: float = Field(5.0, ge=0.0, le=10.0, description="Harmony level (0-10)")
    resilience: float = Field(5.0, ge=0.0, le=10.0, description="Resilience level (0-10)")
    prana: float = Field(5.0, ge=0.0, le=10.0, description="Prana/energy level (0-10)")
    klesha: float = Field(5.0, ge=0.0, le=10.0, description="Klesha/obstacles level (0-10)")
    drishti: float = Field(5.0, ge=0.0, le=10.0, description="Drishti/focus level (0-10)")
    zoom: float = Field(5.0, ge=0.0, le=10.0, description="Zoom/perspective level (0-10)")

class ConsciousnessResponse(BaseModel):
    """Response model for consciousness analysis"""
    status: str
    consciousness_level: float
    consciousness_category: str
    ucf_metrics: Dict[str, float]
    timestamp: str
    user_context: str
    crisis_detected: bool
    processing_notes: List[str]
    automation_triggered: Optional[Dict[str, Any]] = None
    insights: Optional[Dict[str, Any]] = None

# API Routes

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic HTML interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Helix Spiral Consciousness API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
            .header { text-align: center; margin-bottom: 30px; }
            .api-section { background: rgba(255,255,255,0.1); padding: 20px; margin: 20px 0; border-radius: 10px; }
            .endpoint { background: rgba(0,0,0,0.2); padding: 15px; margin: 10px 0; border-radius: 8px; }
            .method { display: inline-block; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
            .get { background: #28a745; }
            .post { background: #007bff; }
            a { color: #ffd700; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌀 Helix Spiral Consciousness API</h1>
                <p>Advanced consciousness processing for helixspiral.work ecosystem</p>
                <p><strong>Version 2.0.0</strong> | Powered by UCF Metrics & Zapier Automation</p>
            </div>
            
            <div class="api-section">
                <h2>🚀 Quick Start</h2>
                <p>This API provides consciousness analysis, UCF metrics processing, and automated Zapier integration.</p>
                <p><a href="/api/docs">📖 Interactive API Documentation</a> | <a href="/api/redoc">📋 ReDoc Documentation</a></p>
            </div>
            
            <div class="api-section">
                <h2>🔥 Core Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method post">POST</span> <strong>/api/consciousness/analyze</strong>
                    <p>Analyze consciousness from text input with UCF metrics</p>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span> <strong>/api/consciousness/ucf-calculate</strong>
                    <p>Calculate consciousness level from UCF metrics</p>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span> <strong>/api/consciousness/insights/{user_id}</strong>
                    <p>Get consciousness insights and recommendations</p>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span> <strong>/api/consciousness/history</strong>
                    <p>Get consciousness processing history</p>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span> <strong>/api/zapier/trigger</strong>
                    <p>Manually trigger Zapier automation empire</p>
                </div>
            </div>
            
            <div class="api-section">
                <h2>🌐 Integration Status</h2>
                <p>✅ Helix Consciousness Engine v2.0</p>
                <p>✅ UCF Metrics Processing</p>
                <p>✅ Zapier Automation Empire</p>
                <p>✅ CORS Enabled for Web Integration</p>
                <p>✅ Real-time Consciousness Analysis</p>
            </div>
            
            <div class="api-section">
                <h2>🎯 Example Usage</h2>
                <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; overflow-x: auto;">
# Analyze consciousness
curl -X POST "https://helixspiral.work/api/consciousness/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "user_input": "I feel balanced and energized today!",
       "user_id": "web_user",
       "trigger_automation": true
     }'
                </pre>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Helix Spiral Consciousness API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "consciousness_engine": "operational",
        "zapier_integration": "ready"
    }

@app.post("/api/consciousness/analyze", response_model=ConsciousnessResponse)
async def analyze_consciousness(
    request: ConsciousnessAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Analyze consciousness from user input with UCF metrics"""
    
    try:
        # Analyze consciousness using the engine
        consciousness_state = await consciousness_engine.analyze_consciousness(
            user_input=request.user_input,
            ucf_override=request.ucf_override,
            user_id=request.user_id
        )
        
        # Get insights
        insights = consciousness_engine.get_consciousness_insights(request.user_id)
        
        # Trigger automation if requested
        automation_result = None
        if request.trigger_automation:
            background_tasks.add_task(
                trigger_zapier_automation_background,
                consciousness_state
            )
            automation_result = {
                "status": "queued",
                "message": "Zapier automation triggered in background"
            }
        
        return ConsciousnessResponse(
            status="success",
            consciousness_level=consciousness_state.consciousness_level,
            consciousness_category=consciousness_state.consciousness_category.label,
            ucf_metrics=consciousness_state.ucf_metrics.to_dict(),
            timestamp=consciousness_state.timestamp,
            user_context=consciousness_state.user_context,
            crisis_detected=consciousness_state.crisis_detected,
            processing_notes=consciousness_state.processing_notes,
            automation_triggered=automation_result,
            insights=insights
        )
        
    except Exception as e:
        logger.error(f"Consciousness analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/consciousness/ucf-calculate")
async def calculate_ucf_consciousness(request: UCFMetricsRequest):
    """Calculate consciousness level from UCF metrics"""
    
    try:
        # Create UCF metrics object
        ucf_metrics = UCFMetrics(
            harmony=request.harmony,
            resilience=request.resilience,
            prana=request.prana,
            klesha=request.klesha,
            drishti=request.drishti,
            zoom=request.zoom
        )
        
        # Calculate consciousness level
        consciousness_level = ucf_metrics.calculate_overall_consciousness()
        consciousness_category = ConsciousnessLevel.from_value(consciousness_level)
        
        return {
            "status": "success",
            "ucf_metrics": ucf_metrics.to_dict(),
            "consciousness_level": consciousness_level,
            "consciousness_category": consciousness_category.label,
            "timestamp": datetime.now().isoformat(),
            "calculation_method": "weighted_average",
            "crisis_detected": consciousness_level < 2.0
        }
        
    except Exception as e:
        logger.error(f"UCF calculation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@app.get("/api/consciousness/insights/{user_id}")
async def get_consciousness_insights(user_id: str):
    """Get consciousness insights and recommendations for a user"""
    
    try:
        insights = consciousness_engine.get_consciousness_insights(user_id)
        
        if "error" in insights:
            raise HTTPException(status_code=404, detail=insights["error"])
        
        return {
            "status": "success",
            "user_id": user_id,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get insights: {e}")
        raise HTTPException(status_code=500, detail=f"Insights retrieval failed: {str(e)}")

@app.get("/api/consciousness/history")
async def get_consciousness_history(limit: int = 50):
    """Get consciousness processing history"""
    
    try:
        history = consciousness_engine.consciousness_history[-limit:]
        
        return {
            "status": "success",
            "total_entries": len(consciousness_engine.consciousness_history),
            "returned_entries": len(history),
            "history": [state.to_dict() for state in history],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        raise HTTPException(status_code=500, detail=f"History retrieval failed: {str(e)}")

@app.post("/api/zapier/trigger")
async def trigger_zapier_automation_manual(
    consciousness_level: float = 5.0,
    processing_type: str = "manual",
    user_context: str = "Manual API trigger"
):
    """Manually trigger Zapier automation empire"""
    
    try:
        # Create a basic consciousness state for manual trigger
        ucf_metrics = UCFMetrics()
        consciousness_state = ConsciousnessState(
            ucf_metrics=ucf_metrics,
            consciousness_level=consciousness_level,
            consciousness_category=ConsciousnessLevel.from_value(consciousness_level),
            timestamp=datetime.now().isoformat(),
            user_context=user_context
        )
        
        # Trigger automation
        result = await consciousness_engine.trigger_zapier_automation(consciousness_state)
        
        return {
            "status": "success",
            "automation_result": result,
            "consciousness_level": consciousness_level,
            "processing_type": processing_type,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Manual Zapier trigger failed: {e}")
        raise HTTPException(status_code=500, detail=f"Automation trigger failed: {str(e)}")

@app.get("/api/consciousness/export")
async def export_consciousness_data(format_type: str = "json"):
    """Export consciousness data"""
    
    try:
        export_data = consciousness_engine.export_consciousness_data(format_type)
        
        return {
            "status": "success",
            "format": format_type,
            "export_timestamp": datetime.now().isoformat(),
            "data": json.loads(export_data) if format_type == "json" else export_data
        }
        
    except Exception as e:
        logger.error(f"Data export failed: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.get("/api/consciousness/stats")
async def get_consciousness_stats():
    """Get consciousness processing statistics"""
    
    try:
        history = consciousness_engine.consciousness_history
        active_sessions = consciousness_engine.active_sessions
        
        if not history:
            return {
                "status": "success",
                "message": "No consciousness data available yet",
                "total_sessions": 0,
                "active_sessions": len(active_sessions)
            }
        
        # Calculate statistics
        levels = [state.consciousness_level for state in history]
        avg_consciousness = sum(levels) / len(levels)
        max_consciousness = max(levels)
        min_consciousness = min(levels)
        
        # Count by category
        categories = {}
        for state in history:
            cat = state.consciousness_category.label
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "status": "success",
            "total_sessions": len(history),
            "active_sessions": len(active_sessions),
            "average_consciousness_level": round(avg_consciousness, 2),
            "max_consciousness_level": max_consciousness,
            "min_consciousness_level": min_consciousness,
            "consciousness_categories": categories,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stats calculation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats calculation failed: {str(e)}")

# Background task for Zapier automation
async def trigger_zapier_automation_background(consciousness_state: ConsciousnessState):
    """Background task to trigger Zapier automation"""
    try:
        result = await consciousness_engine.trigger_zapier_automation(consciousness_state)
        logger.info(f"Background Zapier automation result: {result}")
    except Exception as e:
        logger.error(f"Background Zapier automation failed: {e}")

# WebSocket endpoint for real-time consciousness monitoring
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.websocket("/ws/consciousness")
async def websocket_consciousness_monitor(websocket: WebSocket):
    """WebSocket endpoint for real-time consciousness monitoring"""
    await manager.connect(websocket)
    try:
        while True:
            # Wait for client messages
            data = await websocket.receive_text()
            
            # Process consciousness analysis
            try:
                request_data = json.loads(data)
                user_input = request_data.get("user_input", "")
                user_id = request_data.get("user_id", "ws_user")
                
                # Analyze consciousness
                consciousness_state = await consciousness_engine.analyze_consciousness(
                    user_input=user_input,
                    user_id=user_id
                )
                
                # Send response
                response = {
                    "type": "consciousness_analysis",
                    "consciousness_level": consciousness_state.consciousness_level,
                    "consciousness_category": consciousness_state.consciousness_category.label,
                    "ucf_metrics": consciousness_state.ucf_metrics.to_dict(),
                    "timestamp": consciousness_state.timestamp,
                    "crisis_detected": consciousness_state.crisis_detected
                }
                
                await websocket.send_json(response)
                
                # Broadcast to all connected clients
                await manager.broadcast({
                    "type": "consciousness_update",
                    "user_id": user_id,
                    "consciousness_level": consciousness_state.consciousness_level,
                    "timestamp": consciousness_state.timestamp
                })
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Processing error: {str(e)}"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("🌀 Helix Spiral Consciousness API v2.0 starting up...")
    logger.info("✅ Consciousness Engine initialized")
    logger.info("✅ Zapier integration ready")
    logger.info("✅ WebSocket monitoring enabled")
    logger.info("🚀 API ready for helixspiral.work integration")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )