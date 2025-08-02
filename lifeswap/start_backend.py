#!/usr/bin/env python3
"""
LifeSwap Backend Startup Script
This script starts the FastAPI backend server and initializes the database
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("🚀 Starting LifeSwap Backend...")
    print("📁 Working directory:", os.getcwd())
    
    # Check if database exists
    db_file = Path("lifeswap.db")
    if not db_file.exists():
        print("🗄️  Database not found. Creating and seeding with sample data...")
        try:
            subprocess.run([sys.executable, "seed_data.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error seeding database: {e}")
            return 1
    
    # Start the FastAPI server
    print("🌐 Starting FastAPI server on http://localhost:8000")
    print("📚 API documentation will be available at http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())