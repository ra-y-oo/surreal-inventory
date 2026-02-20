# Deployment Guide

Complete step-by-step guide to deploying the Inventory Management System to production.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Static)                    │
│              (Netlify, Vercel, or GitHub Pages)         │
│                   index.html + CSS + JS                 │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/HTTPS
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   Backend (API)                         │
│                   (Render or Heroku)                    │
│                   Flask + SQLite                        │
│                    app.py + database                    │
└─────────────────────────────────────────────────────────┘
```

## Backend Deployment on Render

### Prerequisites
- GitHub account with your repository
- Render account (free tier available at render.com)

### Step 1: Prepare Your Repository

Push your code to GitHub:
```bash
git add .
git commit -m "Initial inventory app"
git push origin main
```

Ensure your backend folder structure is correct:
```
backend/
├── app.py
├── requirements.txt
└── Procfile
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Click "Sign up"
3. Connect your GitHub account
4. Grant permission to access your repositories

### Step 3: Create a Web Service

1. From Render dashboard, click "New +" → "Web Service"
2. Search for your repository and connect it
3. Fill in the service details:

   **Name**: `surreal-inventory-api`
   
   **Environment**: `Python 3`
   
   **Build Command**: `cd backend && pip install -r requirements.txt`
   
   **Start Command**: `cd backend && gunicorn app:app`
   
   **Plan**: Free (or Paid for 24/7 uptime)

4. Click "Create Web Service"

### Step 4: Configure Environment Variables (if needed)

In Render dashboard → Your Service → Environment:
- No environment variables needed for basic setup
- If using PostgreSQL later, add `DATABASE_URL`

### Step 5: Deploy

Render will automatically:
- Build your application
- Run the start command
- Assign you a public URL

Your backend will be available at: `https://surreal-inventory-api.onrender.com`

### Step 6: Verify Deployment

Test your backend is running:
```bash
curl https://surreal-inventory-api.onrender.com/health
```

You should see: `{"status":"ok"}`

### Important Notes for Render

**Cold Starts**: First request after inactivity takes 10-30 seconds
- The frontend handles this with the health check on page load
- Subsequent requests are instant

**Data Persistence**: SQLite data persists during the service lifecycle
- If you restart the service, data is preserved
- For production with critical data, upgrade to PostgreSQL

**Sleep Mode**: Free tier services sleep after 15 minutes of inactivity
- Your frontend wakes the server with a `/health` call on page load
- This is normal and expected

---

## Frontend Deployment Options

### Option 1: Netlify (Recommended)

#### Step 1: Prepare Files
```bash
# Ensure your frontend folder has index.html
cd frontend
ls -la  # should see index.html
```

#### Step 2: Deploy to Netlify

Method A - Drag and Drop (Easiest):
1. Go to https://netlify.com
2. Sign in or create account
3. Drag and drop your `frontend` folder
4. Your site is now live!

Method B - GitHub Integration:
1. Push `frontend` folder to GitHub
2. Go to netlify.com/sites
3. Click "New site from Git"
4. Connect GitHub repository
5. Set build settings:
   - Base directory: `frontend`
   - No build command needed
6. Deploy

#### Step 3: Get Your Frontend URL

You'll receive a URL like: `https://surreal-inventory.netlify.app`

### Option 2: Vercel

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - Root Directory: `frontend`
   - No build script needed
5. Deploy
6. Get your URL: `https://surreal-inventory.vercel.app`

### Option 3: GitHub Pages

1. Push your code to GitHub
2. Go to repository → Settings → Pages
3. Source: `main` branch
4. Folder: `frontend`
5. Save
6. Your site is at: `https://your-username.github.io/surreal-inventory`

---

## Connect Frontend to Backend

This is the crucial step!

### Step 1: Get Your Backend URL

From Render dashboard, copy your service URL:
- Example: `https://surreal-inventory-api.onrender.com`

### Step 2: Update Frontend Configuration

Edit `frontend/index.html` - around line 15:

**Before:**
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

**After:**
```javascript
const API_BASE_URL = 'https://surreal-inventory-api.onrender.com';
```

### Step 3: Redeploy Frontend

- **Netlify**: Automatically redeploys when you push to GitHub
- **Vercel**: Same - automatic redeploy
- **GitHub Pages**: Push changes, wait 30 seconds

### Step 4: Test Connection

1. Open your frontend URL in browser
2. Check status indicator (should show "✓ Server connected")
3. Add a test phone
4. Verify it appears in the table
5. Check stock summary updates

---

## Production Checklist

- [ ] Backend deployed to Render
- [ ] Backend URL copied
- [ ] Frontend `API_BASE_URL` updated
- [ ] Frontend deployed to Netlify/Vercel/GitHub Pages
- [ ] Frontend and backend URLs match configuration
- [ ] Health check working (status indicator shows green)
- [ ] Can add phones through frontend form
- [ ] Can add accessories through frontend form
- [ ] Stock summary calculates correctly
- [ ] Delete functionality works
- [ ] Tested on mobile device
- [ ] Cold start time acceptable (first load ~10-30s)
- [ ] Data persists after page refresh
- [ ] Error messages display correctly

---

## Monitoring and Maintenance

### Check Backend Health

Monitor your Render service:
1. Go to Render dashboard
2. Select your service
3. Check "Logs" for any errors
4. Check "Metrics" for performance

### Monitor Uptime

Add a simple uptime monitoring (free options):
- https://uptimerobot.com - Monitor your `/health` endpoint
- https://statuspage.io - Create a status page

### Database Backups

For SQLite (current setup):
- Data is stored in `inventory.db`
- Render keeps backups automatically

For enhanced backup:
1. Upgrade to PostgreSQL on Render
2. Enable automated backups
3. Backup frequency: Daily

### Gradual Data Growth

As your inventory grows:
- Small inventories: SQLite works fine
- Large inventories (10k+ items): Consider PostgreSQL

---

## Troubleshooting Deployment

### Frontend Can't Connect to Backend

**Symptoms**:
- Status shows red "Waiting for server"
- Network tab shows CORS error

**Solutions**:
1. Verify backend URL is correct in `API_BASE_URL`
2. Check backend is running: `curl https://backend-url/health`
3. Check CORS headers - backend has `CORS(app)` enabled
4. Clear browser cache and reload

### Backend Returns 503 Error

**Symptoms**:
- "Service Unavailable" when accessing backend

**Solutions**:
1. Service might be starting up (cold start)
2. Check Render dashboard logs for errors
3. Restart the service from Render dashboard
4. Check if you've exceeded free tier quotas

### Data Not Persisting

**Symptoms**:
- Data disappears after service restart

**Solutions for SQLite**:
1. Data persists during session
2. If service crashes, data may be lost
3. Upgrade to PostgreSQL for guaranteed persistence
4. Or add regular backup scripts

### Slow First Load

**Expected behavior**:
- First request to backend takes 10-30 seconds
- This is normal for free Render tier
- Frontend shows "Connecting to server..." during this time
- Subsequent requests are instant

---

## Upgrading to Production Database

### Migrate from SQLite to PostgreSQL

1. From Render dashboard → "Databases"
2. Create new PostgreSQL database
3. Copy connection string
4. Add to service environment variables as `DATABASE_URL`
5. Update `app.py` to use PostgreSQL:

```python
import psycopg2
from psycopg2 import sql

# Instead of SQLite
db = psycopg2.connect(os.environ['DATABASE_URL'])
```

6. Redeploy

---

## Performance Optimization

### Caching
Add Redis for caching inventory summary:
```python
import redis
cache = redis.Redis(url=os.environ['REDIS_URL'])
```

### Database Indexing
Add indices for faster queries:
```python
cursor.execute('CREATE INDEX idx_phone_model ON phones(model)')
```

### CDN for Frontend
Enable Netlify/Vercel CDN (automatic):
- Both services serve via global CDN
- Content cached at edge locations
- Faster worldwide access

---

## Security Checklist (for production)

- [ ] Add rate limiting to prevent abuse
- [ ] Restrict CORS to specific frontend domain
- [ ] Add input validation on backend
- [ ] Use HTTPS only (automatic on Render/Netlify/Vercel)
- [ ] Monitor for unusual activity in logs
- [ ] Consider adding authentication for admin operations
- [ ] regular security updates
- [ ] Backup sensitive data regularly

---

## Support and Resources

- **Render Documentation**: https://render.com/docs
- **Netlify Docs**: https://docs.netlify.com
- **Vercel Docs**: https://vercel.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com
- **GitHub Pages Docs**: https://pages.github.com

---

## Rollback Plan

If something goes wrong:

1. **Frontend Issue**:
   - Netlify/Vercel automatically keeps previous deployments
   - Go to site dashboard → Deployments → Rollback to previous

2. **Backend Issue**:
   - Render keeps deployment history
   - Go to service → Builds → Select previous build → Redeploy

3. **Configuration Issue**:
   - Revert code changes: `git revert <commit-hash>`
   - Push to GitHub
   - Services automatically redeploy

---

Good luck with your deployment! 🚀
