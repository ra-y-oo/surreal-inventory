# Quick Start Guide

Get the Inventory Management System up and running in minutes.

## Prerequisites

- Python 3.x
- Git (optional, for version control)
- A modern web browser

## Local Setup (5 minutes)

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the Flask Server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Open the Frontend

**Option A: Open HTML file directly**
```bash
# In another terminal, navigate to frontend folder
cd frontend
# Then open index.html in your browser
# File → Open File → select index.html
```

**Option B: Use Python HTTP Server**
```bash
# From the frontend directory
python -m http.server 8000

# Then open http://localhost:8000 in your browser
```

### Step 4: Test the Application

1. Fill out the "Add Phone" form:
   - Model: iPhone 15 Pro
   - Price: 120000
   - Quantity: 5

2. Click "Add Phone"

3. You should see the phone appear in the Phones table below

4. The "Stock Summary" should update automatically

5. Try adding an accessory too!

### Step 5: Test Deletion

- Click the "Delete" button next to any item
- Confirm the deletion
- Item disappears and summary updates

## API Testing

While the server is running, test endpoints in another terminal:

```bash
# Test health check
curl http://localhost:5000/health

# Add a phone
curl -X POST http://localhost:5000/phones \
  -H "Content-Type: application/json" \
  -d '{"model":"Samsung S24","price":100000,"quantity":3}'

# Get all phones
curl http://localhost:5000/phones

# Get inventory summary
curl http://localhost:5000/summary

# Add an accessory
curl -X POST http://localhost:5000/accessories \
  -H "Content-Type: application/json" \
  -d '{"name":"Screen Protector","price":300,"quantity":50}'

# Get all accessories
curl http://localhost:5000/accessories

# Delete a phone (replace 1 with actual phone ID)
curl -X DELETE http://localhost:5000/phones/1
```

## Troubleshooting

### Port 5000 Already in Use
```bash
# Find what's using port 5000
lsof -i :5000

# Or try a different port by editing app.py
# Change: port = int(os.environ.get('PORT', 5000))
# To:     port = int(os.environ.get('PORT', 5001))
```

### CORS Errors in Browser Console
- Make sure the backend is running on localhost:5000
- Check that the frontend is loading from a different port (8000)
- The app.py already has CORS enabled with `CORS(app)`

### Database Errors
- Ensure backend folder has write permissions
- The database file `inventory.db` will be created automatically
- To reset the database, delete `inventory.db` and restart the server

## Production Deployment

### Deploy Backend to Render

1. Push your code to GitHub
2. Go to https://render.com and sign up
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - **Name**: surreal-inventory-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Root Directory**: (leave empty)

6. After deployment, you'll get a URL like: `https://surreal-inventory-api.onrender.com`

### Deploy Frontend to Netlify

1. Go to https://netlify.com
2. Click "Add new site" or "Import an existing project"
3. Drag and drop your `frontend` folder
4. Site deploys instantly!

### Update Frontend Config for Production

Edit `frontend/index.html` and change:
```javascript
// Line ~15, change this:
const API_BASE_URL = 'http://localhost:5000';

// To this (use your actual Render URL):
const API_BASE_URL = 'https://surreal-inventory-api.onrender.com';
```

## Next Steps

✅ Application is working locally
✅ All endpoints tested
✅ Ready for deployment

For detailed API documentation, see [API.md](./API.md)

For production deployment guide, see [DEPLOYMENT.md](./DEPLOYMENT.md)
