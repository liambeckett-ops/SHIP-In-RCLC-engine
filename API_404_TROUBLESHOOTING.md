# 🚨 404 Error Troubleshooting Guide

## Problem: API Endpoints Return 404 Errors

### 🔍 Symptoms
- Diagnostic page shows 404 errors for `/agents`, `/status`, `/docs`
- Health check might also fail
- Web interface loads but API calls don't work

### 🎯 Most Likely Causes & Solutions

#### 1. **Server Not Running Properly**
**Check**: Is the server actually started?

**Solution**:
```bash
# Stop any running server (Ctrl+C)
# Then restart cleanly:
python web_api_server.py --port 8080
```

**Look for these startup messages**:
```
🚀 Starting Solvine Web API Server
🌐 Web Interface: http://localhost:8080
📖 API Documentation: http://localhost:8080/docs
✅ Static files mounted from: [path]
✅ Web API Ready - [X] agents available
```

#### 2. **Port Conflict**
**Check**: Is port 8080 already in use?

**Solution**:
```bash
# Try a different port:
python web_api_server.py --port 8081

# Or find what's using port 8080:
netstat -ano | findstr :8080
```

#### 3. **FastAPI Route Registration Issue**
**Check**: Run the health check test

**Test**:
1. Start server: `python web_api_server.py --port 8080`
2. Run test: `python test_web_server.py`
3. Or visit: `http://localhost:8080/health`

**Expected**: Should return JSON with server health info

#### 4. **CORS or Browser Issues**
**Check**: Test endpoints directly in browser

**Test URLs**:
- `http://localhost:8080/health` → Should show JSON
- `http://localhost:8080/agents` → Should show agent list
- `http://localhost:8080/status` → Should show system status
- `http://localhost:8080/docs` → Should show API documentation

#### 5. **File Path Issues**
**Check**: Are you running from the correct directory?

**Solution**:
```bash
# Make sure you're in the Solvine_Systems directory
cd "c:\Users\rebek\OneDrive\Documents\Schoolwork\Programming\Personal Projects\Solvine_Systems"

# Verify files exist:
dir web_api_server.py
dir web\solvine_web_ui.html
dir web\diagnostic.html
```

### 🧪 Step-by-Step Diagnosis

#### Step 1: Test Basic Connectivity
```bash
python test_web_server.py
```

This will tell you exactly what's working and what's not.

#### Step 2: Test Individual Endpoints
Open these URLs in your browser (one at a time):

1. `http://localhost:8080/health`
   - **Expected**: JSON with server health
   - **If 404**: Server routing is broken

2. `http://localhost:8080/`
   - **Expected**: Beautiful web interface
   - **If 404**: Static file serving broken

3. `http://localhost:8080/docs`
   - **Expected**: FastAPI auto-generated docs
   - **If 404**: FastAPI not working properly

#### Step 3: Check Server Logs
Look at the server terminal output for errors like:
- `ImportError` messages
- `Port already in use` errors
- `File not found` warnings
- HTTP request logs

#### Step 4: Use Enhanced Diagnostic Page
Visit: `http://localhost:8080/diagnostic`

Click the "Test Health Check" button first - this will tell you if the server is responding at all.

### 🛠️ Common Fixes

#### Fix 1: Clean Server Restart
```bash
# Stop server (Ctrl+C in terminal)
# Wait 2 seconds
# Restart:
python web_api_server.py --port 8080
```

#### Fix 2: Use Different Port
```bash
python web_api_server.py --port 8081
# Then visit: http://localhost:8081
```

#### Fix 3: Check Dependencies
```bash
pip install fastapi uvicorn
# Then restart server
```

#### Fix 4: Verify File Locations
```bash
# Should all exist:
ls web_api_server.py
ls web/solvine_web_ui.html
ls web/diagnostic.html
```

#### Fix 5: Reset Everything
```bash
# Stop server
# Delete any __pycache__ folders
rmdir /s __pycache__
# Restart
python web_api_server.py --port 8080
```

### 🎯 Expected Behavior When Working

When everything is working correctly:

1. **Health Check**: `http://localhost:8080/health` returns:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-08-06T...",
     "service": "Solvine Web API",
     "version": "2.0.0"
   }
   ```

2. **Agents Endpoint**: `http://localhost:8080/agents` returns:
   ```json
   {
     "agents": [...],
     "total_count": 6
   }
   ```

3. **Status Endpoint**: `http://localhost:8080/status` returns:
   ```json
   {
     "agents_count": 6,
     "system_stability": 0.88,
     "uptime": "0h 5m"
   }
   ```

4. **Web Interface**: `http://localhost:8080/` shows the beautiful Solvine interface

5. **API Docs**: `http://localhost:8080/docs` shows interactive API documentation

### 🚀 Quick Resolution Commands

Try these in order:

```bash
# 1. Basic restart
python web_api_server.py --port 8080

# 2. Test connectivity
python test_web_server.py

# 3. Try different port
python web_api_server.py --port 8081

# 4. Check what's using the port
netstat -ano | findstr :8080

# 5. Verify working directory
cd "C:\Users\rebek\OneDrive\Documents\Schoolwork\Programming\Personal Projects\Solvine_Systems"
python web_api_server.py --port 8080
```

### 💡 Pro Tips

- **Always test health endpoint first**: `http://localhost:8080/health`
- **Check server logs**: Look for error messages in the terminal
- **Use diagnostic page**: Enhanced version shows detailed error info
- **Try incognito mode**: Rules out browser cache issues
- **Test with curl**: `curl http://localhost:8080/health` for pure API testing

If none of these fixes work, the issue might be more fundamental (Python environment, FastAPI installation, etc.).

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Health check returns JSON
- ✅ All diagnostic tests pass
- ✅ API docs load at `/docs`
- ✅ Web interface shows agent dropdown
- ✅ Can send messages to agents

The 404 errors should be completely resolved! 🚀
