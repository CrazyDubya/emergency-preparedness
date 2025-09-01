#!/usr/bin/env python3
"""
FastAPI Server for Emergency Preparedness System
RESTful API with authentication and real-time features
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uvicorn
import json
import jwt
import hashlib
from datetime import datetime, timedelta
import asyncio
import logging
from pathlib import Path

# Import our system modules
from integrated_preparedness_system import IntegratedPreparednessSystem
from user_profile_manager import UserProfileManager
from backup_manager import BackupManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="Emergency Preparedness API",
    description="Complete disaster readiness platform API",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = "emergency_preparedness_secret_key_change_in_production"
ALGORITHM = "HS256"

# In-memory storage for demo (use proper database in production)
api_keys = {
    "admin_key": {"user_id": "admin", "role": "admin", "profile": "admin"},
    "user_key": {"user_id": "user1", "role": "user", "profile": "default"},
    "gui_key": {"user_id": "gui", "role": "user", "profile": "default"}  # Embedded GUI key
}

# Global system instances (in production, use dependency injection)
systems = {}

# Pydantic models
class LoginRequest(BaseModel):
    api_key: str
    profile: Optional[str] = "default"

class ProfileUpdate(BaseModel):
    family: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None

class RiskAssessmentRequest(BaseModel):
    scenario_type: str
    severity: int
    location: str = "suburban"

class DrillRequest(BaseModel):
    drill_type: str
    participants: int
    difficulty: str = "intermediate"

class BackupRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class AlertSubscription(BaseModel):
    alert_types: List[str]
    location: Optional[str] = None
    notification_method: str = "api"

# Authentication functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key and return user info"""
    api_key = credentials.credentials
    
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return api_keys[api_key]

def get_system(user_info: dict = Depends(verify_api_key)) -> IntegratedPreparednessSystem:
    """Get or create system instance for user"""
    user_id = user_info["user_id"]
    profile = user_info["profile"]
    
    if user_id not in systems:
        systems[user_id] = IntegratedPreparednessSystem(profile=profile)
        logger.info(f"Created system instance for user: {user_id}")
    
    return systems[user_id]

# API Routes

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Emergency Preparedness API",
        "version": "3.0.0",
        "status": "operational",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "auth": "/auth/login",
            "profile": "/api/profile",
            "risk": "/api/risk/*",
            "supplies": "/api/supplies/*",
            "alerts": "/api/alerts/*",
            "drills": "/api/drills/*",
            "backup": "/api/backup/*"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_users": len(systems),
        "api_version": "3.0.0"
    }

# Authentication endpoints

@app.post("/auth/login")
async def login(request: LoginRequest):
    """Authenticate with API key and get access token"""
    if request.api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    user_info = api_keys[request.api_key]
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_info["user_id"], "role": user_info["role"]},
        expires_delta=timedelta(hours=24)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_info["user_id"],
        "role": user_info["role"],
        "profile": request.profile or user_info["profile"]
    }

# Profile management endpoints

@app.get("/api/profile")
async def get_profile(system: IntegratedPreparednessSystem = Depends(get_system)):
    """Get current user profile"""
    return {
        "profile": system.profile_manager.profile_data,
        "summary": system.profile_manager.get_profile_summary()
    }

@app.put("/api/profile")
async def update_profile(
    update: ProfileUpdate,
    system: IntegratedPreparednessSystem = Depends(get_system)
):
    """Update user profile"""
    success_count = 0
    
    if update.family:
        if system.profile_manager.save_family_info(update.family):
            success_count += 1
    
    if update.location:
        if system.profile_manager.save_location_info(update.location):
            success_count += 1
    
    if update.preferences:
        if system.profile_manager.save_preferences(update.preferences):
            success_count += 1
    
    return {
        "success": success_count > 0,
        "sections_updated": success_count,
        "profile_summary": system.profile_manager.get_profile_summary()
    }

# Risk assessment endpoints

@app.get("/api/risk/assessment")
async def get_risk_assessment(system: IntegratedPreparednessSystem = Depends(get_system)):
    """Get current risk assessment"""
    cached_assessment = system.profile_manager.get_risk_assessment()
    
    if cached_assessment:
        return {
            "assessment": cached_assessment,
            "cached": True,
            "needs_update": system.profile_manager.is_update_needed('risk_assessment')
        }
    else:
        return {
            "assessment": None,
            "cached": False,
            "needs_update": True
        }

@app.post("/api/risk/calculate")
async def calculate_risk(
    request: RiskAssessmentRequest,
    system: IntegratedPreparednessSystem = Depends(get_system)
):
    """Calculate comprehensive risk for scenario"""
    try:
        scenario = {"type": request.scenario_type, "severity": request.severity}
        risk_result = system.advanced_risk_engine.calculate_comprehensive_risk(
            scenario, request.location
        )
        
        return {
            "success": True,
            "risk_analysis": risk_result,
            "scenario": scenario,
            "location": request.location
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk calculation failed: {str(e)}"
        )

# Supplies management endpoints

@app.get("/api/supplies/inventory")
async def get_supplies_inventory(system: IntegratedPreparednessSystem = Depends(get_system)):
    """Get supplies inventory"""
    try:
        # This would need to be implemented in the supply tracker
        return {
            "inventory": [],  # Placeholder
            "total_items": 0,
            "categories": [],
            "expiring_soon": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get inventory: {str(e)}"
        )

@app.get("/api/supplies/expiry")
async def check_expiry(system: IntegratedPreparednessSystem = Depends(get_system)):
    """Check items expiring soon"""
    try:
        expiring = system.supply_tracker.check_expiry_dates()
        return {
            "expiring_items": expiring,
            "count": len(expiring),
            "checked_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check expiry: {str(e)}"
        )

# Alerts endpoints

@app.get("/api/alerts/active")
async def get_active_alerts(system: IntegratedPreparednessSystem = Depends(get_system)):
    """Get active alerts"""
    try:
        alerts = system.alert_monitor.get_active_alerts()
        return {
            "active_alerts": alerts,
            "count": len(alerts),
            "last_checked": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get alerts: {str(e)}"
        )

@app.post("/api/alerts/subscribe")
async def subscribe_alerts(
    subscription: AlertSubscription,
    system: IntegratedPreparednessSystem = Depends(get_system)
):
    """Subscribe to alert types"""
    try:
        # This would need to be implemented in the alert aggregator
        return {
            "success": True,
            "subscription": subscription.dict(),
            "message": "Alert subscription updated"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to subscribe: {str(e)}"
        )

# Drill endpoints

@app.post("/api/drills/start")
async def start_drill(
    request: DrillRequest,
    system: IntegratedPreparednessSystem = Depends(get_system)
):
    """Start an emergency drill"""
    try:
        result = system.drill_simulator.run_drill(
            request.drill_type,
            request.participants
        )
        
        # Record the activity
        system.profile_manager.record_activity('drill_completed', {
            'type': request.drill_type,
            'participants': request.participants,
            'score': result.get('score', 0)
        })
        
        return {
            "success": True,
            "drill_result": result,
            "drill_type": request.drill_type,
            "participants": request.participants
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Drill failed: {str(e)}"
        )

@app.get("/api/drills/history")
async def get_drill_history(system: IntegratedPreparednessSystem = Depends(get_system)):
    """Get drill history"""
    activities = system.profile_manager.profile_data.get('activities', {})
    drill_activities = [
        {
            "activity": key,
            "timestamp": value["timestamp"],
            "details": value["details"]
        }
        for key, value in activities.items()
        if 'drill' in key
    ]
    
    return {
        "drill_history": drill_activities,
        "total_drills": len(drill_activities)
    }

# Backup endpoints

@app.post("/api/backup/create")
async def create_backup(
    request: BackupRequest,
    background_tasks: BackgroundTasks,
    system: IntegratedPreparednessSystem = Depends(get_system)
):
    """Create a system backup"""
    try:
        success, path = system.backup_manager.create_backup(
            backup_name=request.name,
            description=request.description or "API-initiated backup"
        )
        
        return {
            "success": success,
            "backup_path": path,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Backup failed: {str(e)}"
        )

@app.get("/api/backup/list")
async def list_backups(system: IntegratedPreparednessSystem = Depends(get_system)):
    """List all available backups"""
    try:
        backups = system.backup_manager.list_backups()
        return {
            "backups": backups,
            "count": len(backups)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list backups: {str(e)}"
        )

# Reports endpoints

@app.get("/api/reports/comprehensive")
async def get_comprehensive_report(system: IntegratedPreparednessSystem = Depends(get_system)):
    """Generate comprehensive preparedness report"""
    try:
        report = system.generate_comprehensive_report()
        return {
            "report": report,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )

@app.get("/api/export/{format}")
async def export_data(
    format: str,
    system: IntegratedPreparednessSystem = Depends(get_system)
):
    """Export all data in specified format"""
    if format not in ["json", "csv", "html", "pdf"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported export format"
        )
    
    try:
        if format == "json":
            export_data = {
                'profile': system.profile_manager.profile_data,
                'timestamp': datetime.now().isoformat(),
                'version': '3.0',
                'api_export': True
            }
            
            return JSONResponse(
                content=export_data,
                headers={
                    "Content-Disposition": f"attachment; filename=export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=f"Export format {format} not yet implemented"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )

# WebSocket endpoint for real-time updates (placeholder)
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    try:
        while True:
            # Send periodic updates
            await websocket.send_json({
                "type": "status_update",
                "timestamp": datetime.now().isoformat(),
                "active_users": len(systems)
            })
            await asyncio.sleep(30)  # Send update every 30 seconds
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    print("🚀 Starting Emergency Preparedness API Server...")
    print("📋 API Documentation: http://localhost:8000/docs")
    print("🔑 Default API Keys:")
    print("  • admin_key (admin role)")
    print("  • user_key (user role)")
    print("  • gui_key (embedded GUI)")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )