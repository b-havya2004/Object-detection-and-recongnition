#!/bin/bash
"""
LifeSwap Frontend Startup Script
This script starts the React development server
"""

echo "🚀 Starting LifeSwap Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🌐 Starting React development server on http://localhost:3000"
echo "🔄 Press Ctrl+C to stop the server"

npm start