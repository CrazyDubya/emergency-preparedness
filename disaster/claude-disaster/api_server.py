#!/usr/bin/env python3
"""
FastAPI Server for Emergency Preparedness System
RESTful API with authentication and real-time features
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uvicorn
import json
from datetime import datetime, timedelta
import asyncio
import logging
from pathlib import Path

# Import our system modules
from integrated_preparedness_system import IntegratedPreparednessSystem
from user_profile_manager import UserProfileManager
from backup_manager import BackupManager
from security import (
    SecureConfig, JWTManager, RateLimiter,
    get_secure_config, get_rate_limiter
)
from exceptions import (
    InvalidAPIKeyError, TokenExpiredError, PermissionDeniedError,
    AuthenticationError
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize secure configuration
secure_config = get_secure_config()
rate_limiter = get_rate_limiter()

# Initialize JWT manager
try:
    jwt_manager = JWTManager(secure_config.secret_key)
except Exception as e:
    logger.warning(f"JWT manager not available: {e}")
    jwt_manager = None

# FastAPI app initialization
app = FastAPI(
    title="Emergency Preparedness API",
    description="Complete disaster readiness platform API",
    version="3.1.0",
    docs_url="/docs" if secure_config.is_debug_mode else None,
    redoc_url="/redoc" if secure_config.is_debug_mode else None
)

# CORS middleware with secure configuration
allowed_origins = secure_config.allowed_origins
if not allowed_origins and secure_config.is_debug_mode:
    # Allow all origins only in debug mode
    allowed_origins = ["*"]
    logger.warning("CORS: Allowing all origins (debug mode)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Security
security = HTTPBearer()

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
async def verify_api_key(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Verify API key and return user info with rate limiting

    Args:
        request: FastAPI request object
        credentials: HTTP Bearer credentials

    Returns:
        Dictionary with user_id, role, profile, and permissions

    Raises:
        HTTPException: If authentication fails or rate limit exceeded
    """
    api_key = credentials.credentials

    try:
        # Validate the API key
        key_config = secure_config.validate_api_key(api_key)

        # Check rate limit
        key_hash = SecureConfig.hash_api_key(api_key)[:16]  # Use partial hash as key
        if not rate_limiter.is_allowed(key_hash, key_config.rate_limit):
            remaining = rate_limiter.get_remaining(key_hash, key_config.rate_limit)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again later.",
                headers={"X-RateLimit-Remaining": str(remaining)}
            )

        return {
            "user_id": key_config.user_id,
            "role": key_config.role,
            "profile": key_config.profile,
            "permissions": key_config.permissions
        }

    except InvalidAPIKeyError:
        logger.warning(f"Invalid API key attempt from {request.client.host}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def verify_jwt_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Verify JWT token and return user info

    For endpoints that use JWT instead of API key authentication
    """
    if jwt_manager is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="JWT authentication not available"
        )

    token = credentials.credentials

    try:
        payload = jwt_manager.verify_token(token, "access")
        return {
            "user_id": payload["sub"],
            "role": payload.get("role", "user"),
            "permissions": payload.get("permissions", [])
        }

    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except AuthenticationError as e:
        logger.warning(f"Invalid token from {request.client.host}: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )


def require_role(required_role: str):
    """Dependency to require a specific role"""
    async def role_checker(user_info: dict = Depends(verify_api_key)):
        if user_info["role"] != required_role and user_info["role"] != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return user_info
    return role_checker


def require_permission(required_permission: str):
    """Dependency to require a specific permission"""
    async def permission_checker(user_info: dict = Depends(verify_api_key)):
        permissions = user_info.get("permissions", [])
        if "*" not in permissions and required_permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_permission} permission"
            )
        return user_info
    return permission_checker


def get_system(user_info: dict = Depends(verify_api_key)) -> IntegratedPreparednessSystem:
    """Get or create system instance for user"""
    user_id = user_info["user_id"]
    profile = user_info.get("profile", "default")

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
async def login(request: LoginRequest, req: Request):
    """Authenticate with API key and get JWT access token"""
    try:
        # Validate API key
        key_config = secure_config.validate_api_key(request.api_key)

        if jwt_manager is None:
            # Return API key info if JWT not available
            return {
                "access_token": request.api_key,
                "token_type": "bearer",
                "user_id": key_config.user_id,
                "role": key_config.role,
                "profile": request.profile or key_config.profile,
                "jwt_available": False
            }

        # Create JWT access token
        access_token = jwt_manager.create_access_token(
            user_id=key_config.user_id,
            role=key_config.role,
            permissions=key_config.permissions
        )

        # Create refresh token
        refresh_token = jwt_manager.create_refresh_token(key_config.user_id)

        logger.info(f"User {key_config.user_id} logged in from {req.client.host}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": key_config.user_id,
            "role": key_config.role,
            "profile": request.profile or key_config.profile,
            "expires_in": 3600  # 1 hour
        }

    except InvalidAPIKeyError:
        logger.warning(f"Failed login attempt from {req.client.host}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

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