# agents.md

## Project Overview
Build a simple **Inventory Management System** for a phone & accessories store.

The system must allow users to:
- Add phone models with price and quantity
- Add accessories with name, price, and quantity
- View all inventory items
- Automatically calculate and display the **total stock value in KES (KSh)**

The app must have:
- A **Python Flask backend**
- A **simple HTML, CSS, and JavaScript frontend**
- A **mobile-responsive design**
- Frontend and backend deployed separately  
  - Backend: Render  
  - Frontend: Any static hosting (Vercel, Netlify, etc.)

---

## Tech Stack

### Backend
- Python
- Flask
- Flask-CORS
- SQLite (or in-memory storage if simpler)
- REST API architecture

### Frontend
- HTML
- CSS (mobile-first, simple layout)
- Vanilla JavaScript (no frameworks)

---

## Architecture Requirements

### Separation of Concerns
- Backend handles:
  - Data storage
  - Business logic
  - Total stock value calculation
- Frontend handles:
  - UI rendering
  - Form submissions
  - Fetching data from the backend API

---

## Backend Requirements (Flask)

### API Endpoints

#### Health Check (Cold Start Trigger)
GET /health
- Returns `{ "status": "ok" }`
- Used by the frontend to wake up the Render server when a user visits the site

#### Phones
POST /phones
GET /phones
Each phone item must include:
- `model` (string)
- `price` (number, KES)
- `quantity` (number)

#### Accessories
POST /accessories
GET /accessories
Each accessory item must include:
- `name` (string)
- `price` (number, KES)
- `quantity` (number)

#### Stock Summary
GET /summary
Returns:
- Total phone stock value
- Total accessories stock value
- **Grand total stock value in KES**

Example response:
```json
{
  "phones_total": 250000,
  "accessories_total": 80000,
  "grand_total": 330000
}

Frontend Requirements
Pages / Sections

Add Phone Form

Add Accessory Form

Inventory List

Phones table

Accessories table

Stock Summary Section

Clearly show Total Stock Value (KSh)

Design Guidelines

Simple and clean UI

Mobile-first layout

Use basic CSS (Flexbox or Grid)

No heavy animations

Clear input labels

Buttons large enough for mobile use

Frontend Behavior
Backend Wake-Up Logic

On page load:

Send a GET /health request to the Render backend

This ensures the backend wakes up from sleep before user actions

Data Flow

Forms submit data using fetch()

After submission:

Refresh inventory list

Refresh stock totals

Handle basic errors (empty fields, invalid numbers)

Currency

All prices must be in Kenyan Shillings (KES / KSh)

Display totals formatted as:

KSh 120,000

Non-Requirements (Do NOT Implement)

Authentication or user accounts

Payments

Advanced analytics

Admin roles

Success Criteria

The project is complete when:

Users can add phones and accessories

Inventory displays correctly

Total stock value is accurate

UI works well on mobile

Frontend successfully wakes the Render backend on load

Notes for the Agent

Prioritize simplicity and clarity

Write clean, commented code

Ensure CORS is correctly configured

The app must be production-ready for basic usage
