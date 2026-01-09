import uvicorn
import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================

# Get settings from environment or use defaults
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8001))
RELOAD = os.getenv("RELOAD", "True").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ==========================================
# PRINT STARTUP INFO
# ==========================================

def print_startup_info():
    """
    Print startup information to console.
    """
    print("\n" + "="*70)
    print("🚀 FitFlow API - Starting Server")
    print("="*70)
    print(f"Environment: {ENVIRONMENT}")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")
    print(f"Reload: {RELOAD}")
    print(f"Log Level: {LOG_LEVEL}")
    print("-"*70)
    print("📚 API Documentation:")
    print(f"   Swagger UI: http://{HOST}:{PORT}/docs")
    print(f"   ReDoc: http://{HOST}:{PORT}/redoc")
    print(f"   OpenAPI JSON: http://{HOST}:{PORT}/openapi.json")
    print("-"*70)
    print("✨ Available Endpoints:")
    print("   Health Check:")
    print(f"      GET http://{HOST}:{PORT}/health")
    print("   Authentication:")
    print(f"      POST   http://{HOST}:{PORT}/api/v1/auth/register")
    print(f"      GET    http://{HOST}:{PORT}/api/v1/auth/profile")
    print(f"      PUT    http://{HOST}:{PORT}/api/v1/auth/profile")
    print(f"      DELETE http://{HOST}:{PORT}/api/v1/auth/profile")
    print("   Plans:")
    print(f"      POST http://{HOST}:{PORT}/api/v1/plans/generate")
    print(f"      GET  http://{HOST}:{PORT}/api/v1/plans/current")
    print(f"      GET  http://{HOST}:{PORT}/api/v1/plans/history")
    print(f"      GET  http://{HOST}:{PORT}/api/v1/plans/{{plan_id}}")
    print("   Metrics:")
    print(f"      POST http://{HOST}:{PORT}/api/v1/users/metrics/log")
    print(f"      GET  http://{HOST}:{PORT}/api/v1/users/metrics")
    print(f"      GET  http://{HOST}:{PORT}/api/v1/users/metrics/latest")
    print(f"      GET  http://{HOST}:{PORT}/api/v1/users/metrics/trends")
    print("   Chat:")
    print(f"      POST   http://{HOST}:{PORT}/api/v1/chat/message")
    print(f"      GET    http://{HOST}:{PORT}/api/v1/chat/history")
    print(f"      DELETE http://{HOST}:{PORT}/api/v1/chat/history")
    print("   Progress:")
    print(f"      GET http://{HOST}:{PORT}/api/v1/progress/predictions")
    print(f"      GET http://{HOST}:{PORT}/api/v1/progress/dashboard")
    print(f"      GET http://{HOST}:{PORT}/api/v1/progress/insights")
    print("-"*70)
    print("🛑 To stop server: Press Ctrl+C")
    print("="*70 + "\n")


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():
    """
    Main entry point for FitFlow API.
    
    Initializes and starts the Uvicorn server with FastAPI app.
    """
    try:
        # Print startup information
        print_startup_info()
        
        # Run the FastAPI app with Uvicorn
        uvicorn.run(
            "app.api:app",  # Import path: app/api.py -> app object
            host=HOST,
            port=PORT,
            reload=RELOAD,
            log_level=LOG_LEVEL,
            access_log=True
        )
    
    except KeyboardInterrupt:
        """
        Handle graceful shutdown on Ctrl+C
        """
        print("\n\n" + "="*70)
        print("🛑 FitFlow API shutting down...")
        print("="*70 + "\n")
        sys.exit(0)
    
    except Exception as e:
        """
        Handle startup errors
        """
        print(f"\n❌ Error starting server: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
