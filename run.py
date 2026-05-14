# run.py
from app import app

try:
    from waitress import serve
    WAITRESS_AVAILABLE = True
except ImportError:
    WAITRESS_AVAILABLE = False
    print("⚠️ Waitress not available. Using Flask development server.")

if __name__ == '__main__':
    if WAITRESS_AVAILABLE:
        print("🚀 Starting production server with Waitress...")
        print("🌐 Server running at: http://localhost:5000")
        print("🌐 Also available at: http://127.0.0.1:5000")
        print("📱 Press Ctrl+C to stop the server")
        serve(app, host='0.0.0.0', port=5000)
    else:
        print("🚀 Starting development server...")
        print("🌐 Server will be available at: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)