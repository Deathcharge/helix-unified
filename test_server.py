"""
Simple test server for authentication endpoints
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.auth import router as auth_router
from backend.database import init_db

# Initialize database
init_db()

app = FastAPI(
    title="Helix Auth Test Server",
    description="Testing authentication endpoints",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register auth router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {
        "service": "helix-auth-test",
        "status": "operational",
        "endpoints": {
            "signup": "/auth/signup",
            "login": "/auth/login",
            "demo": "/auth/demo-login",
            "me": "/auth/me"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"\n🚀 Test server starting on http://0.0.0.0:{port}")
    print(f"📚 Endpoints:")
    print(f"   - POST /auth/signup - Create account")
    print(f"   - POST /auth/login - Login")
    print(f"   - POST /auth/demo-login - Demo account")
    print(f"   - GET /auth/me - Get current user\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
