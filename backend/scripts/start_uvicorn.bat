:: start_uvicorn.bat
echo "Starting uvicorn server..."
start /B uvicorn main:app --host 127.0.0.1 --port 8000 --reload > uvicorn.log 2>&1
timeout /t 10 /nobreak
type uvicorn.log
