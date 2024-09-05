import uvicorn
import os

# Determine the environment (default to 'development' if not set)
env = os.getenv("ENV", "development")
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    if env == "production":
        # Production settings
        uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
    else:
        # Development settings
        uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True, log_level="debug")
