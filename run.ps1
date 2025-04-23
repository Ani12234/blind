# Activate virtual environment
.\venv\Scripts\activate

# Start backend server
Write-Host "Starting backend server..."
cd backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn main:app --reload"
cd ..

# Start frontend
Write-Host "Starting frontend..."
cd frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start"

Write-Host "VisionMate is starting up..."
Write-Host "Backend server will be available at http://localhost:8000"
Write-Host "Frontend will be available at http://localhost:19006" 