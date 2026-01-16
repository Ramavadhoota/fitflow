# API Integration Guide - FitFlow Frontend

## Base URL

```
http://localhost:8001
```

Configure via environment variable:
```
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Authentication

All endpoints (except `/auth/*`) require:
```
Authorization: Bearer {token}
```

Token is automatically included by the `apiClient` interceptor.

---

## Endpoints Reference

### Authentication Endpoints

#### POST `/auth/register`
Register a new user.

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "age": 25,
  "gender": "male",
  "fitness_level": "beginner"
}
```

**Response** (200):
```json
{
  "access_token": "jwt_token_here",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

**Error Handling**: 400, 422
- Email already exists
- Invalid password format
- Missing required fields

#### POST `/auth/login`
Authenticate user with email and password.

**Request**:
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response** (200):
```json
{
  "access_token": "jwt_token_here",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

**Error Handling**: 401
- Invalid credentials

---

### Dashboard Endpoints

#### GET `/user/dashboard`
Get user dashboard overview data.

**Response** (200):
```json
{
  "workouts_this_week": 4,
  "calories_today": 1850,
  "goal_progress": 75,
  "streak_days": 12,
  "protein_today": 125,
  "recent_workouts": [
    {
      "id": "workout_id",
      "name": "Morning Cardio",
      "duration": 30,
      "exercises": "Treadmill, Bike, Elliptical",
      "calories": 350
    }
  ]
}
```

---

### Workout Endpoints

#### GET `/workouts`
Get all workouts for the user.

**Query Parameters**:
- `skip`: Pagination offset (default: 0)
- `limit`: Items per page (default: 10)
- `intensity`: Filter by intensity (light, moderate, intense)

**Response** (200):
```json
{
  "workouts": [
    {
      "id": "uuid",
      "name": "Full Body Strength",
      "duration": 45,
      "exercises": "Squats, Bench Press, Deadlifts",
      "intensity": "intense",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 15,
  "skip": 0,
  "limit": 10
}
```

#### POST `/workouts`
Create a new workout.

**Request**:
```json
{
  "name": "HIIT Training",
  "duration": 30,
  "exercises": "Burpees, Mountain Climbers, Jump Squats",
  "intensity": "intense"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "name": "HIIT Training",
  "duration": 30,
  "exercises": "Burpees, Mountain Climbers, Jump Squats",
  "intensity": "intense",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### GET `/workouts/{id}`
Get details of a specific workout.

**Response** (200):
```json
{
  "id": "uuid",
  "name": "HIIT Training",
  "duration": 30,
  "exercises": "Burpees, Mountain Climbers, Jump Squats",
  "intensity": "intense",
  "calories_burned": 280,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### POST `/workouts/{id}/start`
Start a workout session.

**Response** (200):
```json
{
  "session_id": "uuid",
  "workout_id": "uuid",
  "started_at": "2024-01-15T14:30:00Z",
  "status": "active"
}
```

#### PUT `/workouts/{id}`
Update an existing workout.

**Request**:
```json
{
  "name": "Updated HIIT",
  "duration": 35,
  "intensity": "moderate"
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "name": "Updated HIIT",
  "duration": 35,
  "intensity": "moderate"
}
```

#### DELETE `/workouts/{id}`
Delete a workout.

**Response** (204): No content

---

### Nutrition Endpoints

#### GET `/nutrition`
Get nutrition data for today.

**Response** (200):
```json
{
  "meals": [
    {
      "id": "uuid",
      "food_name": "Chicken Breast",
      "quantity": "100g",
      "calories": 165,
      "protein": 31,
      "carbs": 0,
      "fat": 3.6,
      "logged_at": "2024-01-15T12:30:00Z"
    }
  ],
  "total_calories": 1850,
  "total_protein": 125,
  "total_carbs": 180,
  "total_fat": 52
}
```

#### POST `/nutrition/log-meal`
Log a meal entry.

**Request**:
```json
{
  "food_name": "Grilled Salmon",
  "quantity": "150g",
  "calories": 280,
  "protein": 35,
  "carbs": 0,
  "fat": 18
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "food_name": "Grilled Salmon",
  "quantity": "150g",
  "calories": 280,
  "protein": 35,
  "carbs": 0,
  "fat": 18,
  "logged_at": "2024-01-15T13:30:00Z"
}
```

#### DELETE `/nutrition/meals/{id}`
Delete a meal entry.

**Response** (204): No content

#### GET `/nutrition/daily-summary`
Get daily nutrition summary with goals.

**Response** (200):
```json
{
  "date": "2024-01-15",
  "consumed": {
    "calories": 1850,
    "protein": 125,
    "carbs": 180,
    "fat": 52
  },
  "goals": {
    "calories": 2000,
    "protein": 150,
    "carbs": 250,
    "fat": 65
  },
  "remaining": {
    "calories": 150,
    "protein": 25,
    "carbs": 70,
    "fat": 13
  }
}
```

---

### AI Coach Endpoints

#### GET `/coach/chat-history`
Get chat history with the AI coach.

**Query Parameters**:
- `limit`: Number of messages to retrieve (default: 50)
- `skip`: Pagination offset (default: 0)

**Response** (200):
```json
{
  "messages": [
    {
      "id": "uuid",
      "role": "user",
      "content": "What workout should I do today?",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "id": "uuid",
      "role": "assistant",
      "content": "Based on your fitness level...",
      "timestamp": "2024-01-15T10:01:00Z"
    }
  ]
}
```

#### POST `/coach/chat`
Send a message to the AI coach.

**Request**:
```json
{
  "message": "What should I eat before a workout?"
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "response": "Pre-workout nutrition is important...",
  "timestamp": "2024-01-15T10:02:00Z"
}
```

---

### Progress & Analytics Endpoints

#### GET `/progress/analytics`
Get comprehensive progress analytics.

**Response** (200):
```json
{
  "total_workouts": 42,
  "total_calories_burned": 12500,
  "weight_change": -2.5,
  "achievements": [
    {
      "id": "uuid",
      "title": "First Workout",
      "description": "Completed your first workout",
      "date": "2024-01-01"
    }
  ],
  "weight_history": [
    {
      "date": "2024-01-01",
      "weight": 85.0
    },
    {
      "date": "2024-01-15",
      "weight": 82.5
    }
  ],
  "workout_frequency": [
    {
      "day": "Monday",
      "workouts": 6
    }
  ],
  "calories_history": [
    {
      "date": "2024-01-15",
      "calories": 320
    }
  ],
  "workout_types": [
    {
      "name": "Strength",
      "value": 20
    }
  ]
}
```

#### GET `/progress/achievements`
Get user achievements.

**Response** (200):
```json
{
  "achievements": [
    {
      "id": "uuid",
      "title": "Week Warrior",
      "description": "Complete 7 workouts in a week",
      "unlocked": true,
      "date": "2024-01-10"
    }
  ]
}
```

#### POST `/progress/metrics`
Log a custom metric (weight, measurements, etc).

**Request**:
```json
{
  "metric_type": "weight",
  "value": 82.5,
  "unit": "kg",
  "notes": "Morning weight"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "metric_type": "weight",
  "value": 82.5,
  "unit": "kg",
  "logged_at": "2024-01-15T08:00:00Z"
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Server Error |

### Error Examples

**400 - Bad Request**:
```json
{
  "detail": "Invalid workout duration"
}
```

**401 - Unauthorized**:
```json
{
  "detail": "Not authenticated"
}
```

**422 - Validation Error**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

---

## Rate Limiting

API rate limiting is enforced:
- **Limit**: 1000 requests per hour
- **Header**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

---

## CORS

Frontend can make cross-origin requests to the API. CORS headers are configured in the backend.

---

## Implementation Example

```typescript
import apiClient from '@/lib/apiClient';

// Register
const registerResponse = await apiClient.post('/auth/register', {
  name: 'John Doe',
  email: 'john@example.com',
  password: 'password123',
  age: 25,
  gender: 'male',
  fitness_level: 'beginner'
});

// Store token
localStorage.setItem('token', registerResponse.data.access_token);

// Get dashboard
const dashboardResponse = await apiClient.get('/user/dashboard');
console.log(dashboardResponse.data);

// Create workout
const workoutResponse = await apiClient.post('/workouts', {
  name: 'Morning Run',
  duration: 30,
  exercises: 'Running',
  intensity: 'moderate'
});

// Log meal
const mealResponse = await apiClient.post('/nutrition/log-meal', {
  food_name: 'Oatmeal',
  quantity: '200g',
  calories: 150,
  protein: 5,
  carbs: 27,
  fat: 3
});

// Chat with coach
const chatResponse = await apiClient.post('/coach/chat', {
  message: 'What exercises should I do?'
});

// Get analytics
const analyticsResponse = await apiClient.get('/progress/analytics');
```

---

## Testing API Endpoints

### Using cURL

```bash
# Register
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"pass123","age":25,"gender":"male","fitness_level":"beginner"}'

# Login
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123"}'

# Get Dashboard (with token)
curl -X GET http://localhost:8001/user/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

For detailed frontend implementation, see [FEATURES.md](./FEATURES.md)
