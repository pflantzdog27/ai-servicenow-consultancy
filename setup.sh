#!/bin/bash
# Document Repository Setup Script

echo "🚀 Setting up AI ServiceNow Document Repository"
echo "==============================================="

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p backend/{app/{api,models,services,auth},storage/documents,tests}
mkdir -p frontend/{components,pages,styles}
mkdir -p nginx

# Backend setup
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize Alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Create .env file
echo "⚙️ Creating environment configuration..."
cat > .env << EOL
# AI APIs
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENV=us-east-1

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/servicenow_ai

# Security
JWT_SECRET=your-super-secret-jwt-key-change-this

# Environment
ENVIRONMENT=development
EOL

cd ..

# Frontend setup
echo "⚛️ Setting up React frontend..."
cd frontend
npm install
cd ..

# Docker setup
echo "🐳 Creating Docker configuration..."
cat > docker-compose.yml << EOL
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/servicenow_ai
    volumes:
      - ./backend:/app
      - document_storage:/app/storage
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=servicenow_ai
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  document_storage:
EOL

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your actual API keys"
echo "2. Start services: docker-compose up -d"
echo "3. Visit http://localhost:3000 for the frontend"
echo "4. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "For development:"
echo "- Backend: cd backend && uvicorn main:app --reload"
echo "- Frontend: cd frontend && npm run dev"