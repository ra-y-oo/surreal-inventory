# API Documentation

Complete API reference for the Inventory Management System.

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: `https://your-domain.onrender.com`

## General Response Format

All responses are in JSON format.

### Success Response
```json
{
  "key": "value",
  "data": []
}
```
HTTP Status: 200, 201, 204

### Error Response
```json
{
  "error": "Description of what went wrong"
}
```
HTTP Status: 400, 404, 500

## Endpoints

### 1. Health Check

**Purpose**: Wake up the server from Render sleep

**Request**
```
GET /health
```

**Response**
```json
{
  "status": "ok"
}
```

**HTTP Status**: 200

**Example**
```bash
curl http://localhost:5000/health
```

---

### 2. Phones - Add Phone

**Purpose**: Add a new phone model to inventory

**Request**
```
POST /phones
Content-Type: application/json

{
  "model": "iPhone 15 Pro",
  "price": 150000,
  "quantity": 5
}
```

**Required Fields**
- `model` (string): Phone model name. Cannot be empty.
- `price` (number): Price in Kenyan Shillings. Must be >= 0.
- `quantity` (integer): Quantity in stock. Must be >= 0.

**Response** (201 Created)
```json
{
  "id": 1,
  "model": "iPhone 15 Pro",
  "price": 150000.0,
  "quantity": 5
}
```

**Error Cases**
- Missing fields: 400 - "Missing required fields: model, price, quantity"
- Empty model: 400 - "Model cannot be empty"
- Negative price: 400 - "Price cannot be negative"
- Negative quantity: 400 - "Quantity cannot be negative"
- Invalid data type: 400 - "Invalid data type: ..."

**Example**
```bash
curl -X POST http://localhost:5000/phones \
  -H "Content-Type: application/json" \
  -d '{
    "model": "iPhone 15 Pro",
    "price": 150000,
    "quantity": 5
  }'
```

---

### 3. Phones - Get All Phones

**Purpose**: Retrieve all phones in inventory

**Request**
```
GET /phones
```

**Response** (200 OK)
```json
[
  {
    "id": 1,
    "model": "iPhone 15 Pro",
    "price": 150000.0,
    "quantity": 5,
    "created_at": "2026-02-20 14:28:31"
  },
  {
    "id": 2,
    "model": "Samsung Galaxy S24",
    "price": 100000.0,
    "quantity": 8,
    "created_at": "2026-02-20 14:29:15"
  }
]
```

**Example**
```bash
curl http://localhost:5000/phones
```

---

### 4. Phones - Delete Phone

**Purpose**: Remove a phone from inventory

**Request**
```
DELETE /phones/{id}
```

**Path Parameters**
- `id` (integer): The phone ID to delete

**Response** (200 OK)
```json
{
  "message": "Phone deleted"
}
```

**Example**
```bash
curl -X DELETE http://localhost:5000/phones/1
```

---

### 5. Accessories - Add Accessory

**Purpose**: Add a new accessory to inventory

**Request**
```
POST /accessories
Content-Type: application/json

{
  "name": "USB-C Cable",
  "price": 500,
  "quantity": 20
}
```

**Required Fields**
- `name` (string): Accessory name. Cannot be empty.
- `price` (number): Price in Kenyan Shillings. Must be >= 0.
- `quantity` (integer): Quantity in stock. Must be >= 0.

**Response** (201 Created)
```json
{
  "id": 1,
  "name": "USB-C Cable",
  "price": 500.0,
  "quantity": 20
}
```

**Error Cases**
- Missing fields: 400 - "Missing required fields: name, price, quantity"
- Empty name: 400 - "Name cannot be empty"
- Negative price: 400 - "Price cannot be negative"
- Negative quantity: 400 - "Quantity cannot be negative"
- Invalid data type: 400 - "Invalid data type: ..."

**Example**
```bash
curl -X POST http://localhost:5000/accessories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "USB-C Cable",
    "price": 500,
    "quantity": 20
  }'
```

---

### 6. Accessories - Get All Accessories

**Purpose**: Retrieve all accessories in inventory

**Request**
```
GET /accessories
```

**Response** (200 OK)
```json
[
  {
    "id": 1,
    "name": "USB-C Cable",
    "price": 500.0,
    "quantity": 20,
    "created_at": "2026-02-20 14:30:00"
  },
  {
    "id": 2,
    "name": "Screen Protector",
    "price": 300.0,
    "quantity": 50,
    "created_at": "2026-02-20 14:30:45"
  }
]
```

**Example**
```bash
curl http://localhost:5000/accessories
```

---

### 7. Accessories - Delete Accessory

**Purpose**: Remove an accessory from inventory

**Request**
```
DELETE /accessories/{id}
```

**Path Parameters**
- `id` (integer): The accessory ID to delete

**Response** (200 OK)
```json
{
  "message": "Accessory deleted"
}
```

**Example**
```bash
curl -X DELETE http://localhost:5000/accessories/1
```

---

### 8. Summary - Get Stock Summary

**Purpose**: Get total stock value calculations in KES

**Request**
```
GET /summary
```

**Response** (200 OK)
```json
{
  "phones_total": 750000.0,
  "accessories_total": 10000.0,
  "grand_total": 760000.0
}
```

**Calculation**
- `phones_total`: Sum of (price × quantity) for all phones
- `accessories_total`: Sum of (price × quantity) for all accessories
- `grand_total`: phones_total + accessories_total

**Example**
```bash
curl http://localhost:5000/summary
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource successfully created |
| 400 | Bad Request - Invalid input or missing required fields |
| 404 | Not Found - Endpoint doesn't exist |
| 500 | Server Error - Internal server error |

## Error Handling

All errors return JSON with an `error` field:

```json
{
  "error": "Description of the error"
}
```

Common errors:
- `Missing required fields: ...` - Include all required fields
- `Invalid data type: ...` - Check data types (price as number, quantity as integer)
- `... cannot be negative` - Ensure non-negative values
- `... cannot be empty` - Ensure string fields have content

## Rate Limiting

No rate limiting is currently implemented. For production, consider adding rate limiting to prevent abuse.

## Authentication

No authentication is currently implemented. For production with sensitive data, implement API key authentication or OAuth2.

## CORS

CORS is enabled for all origins. The backend accepts requests from any domain.

For production, consider restricting CORS to specific frontend domains:
```python
CORS(app, resources={r"/api/*": {"origins": "https://your-domain.com"}})
```

## Testing with curl

### Complete Test Sequence

```bash
# 1. Check health
curl http://localhost:5000/health

# 2. Add a phone
curl -X POST http://localhost:5000/phones \
  -H "Content-Type: application/json" \
  -d '{"model":"iPhone 15","price":120000,"quantity":10}'

# 3. Get phones
curl http://localhost:5000/phones

# 4. Add an accessory
curl -X POST http://localhost:5000/accessories \
  -H "Content-Type: application/json" \
  -d '{"name":"USB-C Cable","price":500,"quantity":20}'

# 5. Get accessories
curl http://localhost:5000/accessories

# 6. Get summary
curl http://localhost:5000/summary

# 7. Delete a phone (replace ID if needed)
curl -X DELETE http://localhost:5000/phones/1

# 8. Verify it's deleted
curl http://localhost:5000/phones

# 9. Check updated summary
curl http://localhost:5000/summary
```

## Testing with JavaScript/Fetch

```javascript
const API_BASE = 'http://localhost:5000';

// Add a phone
fetch(`${API_BASE}/phones`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'iPhone 15',
    price: 120000,
    quantity: 5
  })
})
.then(res => res.json())
.then(data => console.log(data));

// Get summary
fetch(`${API_BASE}/summary`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## Database Schema

### phones table
- `id` INTEGER PRIMARY KEY
- `model` TEXT NOT NULL
- `price` REAL NOT NULL
- `quantity` INTEGER NOT NULL
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### accessories table
- `id` INTEGER PRIMARY KEY
- `name` TEXT NOT NULL
- `price` REAL NOT NULL
- `quantity` INTEGER NOT NULL
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
