# LifeSwap - Empathy Through Lived Experiences

A platform that promotes empathy and reduces bias through immersive, choice-driven simulations of daily lives from different walks of life.

## Features

- 🎭 **Interactive Life Simulations** - Experience daily lives through branching decision trees
- 👥 **User Profiles & Progress** - Track empathy points, badges, and achievements  
- 📚 **Life Experience Library** - Categorized collection of diverse life paths
- 🤔 **Reflection System** - Post-experience journaling and sharing
- 🏆 **Gamification** - Points, badges, leaderboards, and challenges
- 🛠️ **Admin Dashboard** - Content management and analytics
- 📱 **Responsive Design** - Works on desktop and mobile devices

## Tech Stack

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL Database
- JWT Authentication
- File Upload Support

### Frontend  
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion
- React Router
- Axios

## Quick Start

### Option 1: Using Startup Scripts (Recommended)

1. **Start the Backend**
   ```bash
   python start_backend.py
   ```
   This will automatically:
   - Install Python dependencies if needed
   - Create and seed the database with sample data
   - Start the FastAPI server on http://localhost:8000

2. **Start the Frontend** (in a new terminal)
   ```bash
   ./start_frontend.sh
   ```
   This will automatically:
   - Install Node.js dependencies if needed
   - Start the React development server on http://localhost:3000

### Option 2: Manual Setup

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python seed_data.py  # Create sample data
   uvicorn main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Default Login Credentials
- **Admin User**: admin@lifeswap.com / admin123
- Or create a new account via the registration page

## Project Structure

```
lifeswap/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── docs/             # Documentation
└── README.md         # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.