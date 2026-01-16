# FitFlow Frontend - Feature Documentation

## Overview

FitFlow is a comprehensive Next.js-based fitness platform frontend that integrates with a FastAPI backend to provide AI-powered fitness coaching, workout planning, and nutrition tracking.

## Core Features

### 1. User Authentication 🔐

**Location**: `src/app/login` and `src/app/register`

#### Registration Page (`/register`)
- User profile setup with:
  - Name, email, password
  - Age and gender
  - Initial fitness level (beginner, intermediate, advanced)
- Form validation
- Error handling with user-friendly messages
- Auto-login after successful registration

#### Login Page (`/login`)
- Email and password authentication
- Session persistence with JWT tokens
- Remember me functionality
- Error messages for failed attempts
- Protected routes redirect to login

**State Management**:
```typescript
useAuthStore() -> {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  setUser(user)
  setToken(token)
  logout()
}
```

### 2. Dashboard 📊

**Location**: `src/app/dashboard/page.tsx`

The main hub after login showing:

#### Key Metrics
- **Workouts This Week**: Total workouts completed
- **Calories Today**: Real-time calorie tracking
- **Goal Progress**: Percentage toward weekly goal
- **Streak Days**: Consecutive workout days

#### Sections
1. **Recent Workouts Feed**
   - Latest completed workouts
   - Duration and exercise count
   - Calories burned
   - "View All" link to workouts page

2. **Quick Actions**
   - Start Workout button → `/workouts`
   - Log Meal button → `/nutrition`
   - Chat with Coach button → `/coach`

3. **Today's Goals**
   - Calorie goal progress bar (0-2000 kcal)
   - Protein goal progress bar (0-150g)
   - Visual indicators with color-coded bars

#### API Calls
```
GET /user/dashboard
Response: {
  workouts_this_week: number,
  calories_today: number,
  goal_progress: number,
  streak_days: number,
  recent_workouts: Workout[],
  protein_today: number
}
```

### 3. Workout Plans 💪

**Location**: `src/app/workouts/page.tsx`

Comprehensive workout management system.

#### Features
- **View Workouts**: Grid view of all available workouts
- **Create Workouts**: Form to create custom workouts
  - Name, duration, intensity level
  - Exercise list
- **Start Workouts**: Begin tracking a workout
- **Filter/Sort**: By intensity or date

#### Workout Card Display
```
┌─ Workout Name ─────────────────┐
│ ⏱️ 30 min                       │
│ 💪 5 exercises                  │
│ 🔥 Intensity: Moderate          │
│                                 │
│    [Start Workout Button]       │
└─────────────────────────────────┘
```

#### Form Inputs
- Workout Name (text)
- Duration (number, minutes)
- Intensity (select: light, moderate, intense)
- Exercises (textarea, comma-separated)

#### API Calls
```
GET    /workouts
POST   /workouts
POST   /workouts/{id}/start
GET    /workouts/{id}
PUT    /workouts/{id}
DELETE /workouts/{id}
```

#### State Management
```typescript
useWorkoutStore() -> {
  workouts: Workout[],
  selectedWorkout: Workout | null,
  setWorkouts(workouts),
  setSelectedWorkout(workout)
}
```

### 4. Nutrition Tracking 🍎

**Location**: `src/app/nutrition/page.tsx`

Complete meal and macro tracking system.

#### Daily Macro Display
- **Calories**: Current vs Goal (2000 kcal)
- **Protein**: Current vs Goal (150g)
- **Carbs**: Current vs Goal (250g)
- **Fat**: Current vs Goal (65g)

Each metric includes:
- Large number display
- Progress bars with visual indicators
- Goal comparison

#### Meal Logging
Form to log meals with:
- Food Name (text)
- Quantity (text, e.g., "100g")
- Calories (number)
- Protein (number, grams)
- Carbs (number, grams)
- Fat (number, grams)

#### Meal Management
- View all logged meals
- Each meal shows:
  - Food name
  - All macros breakdown
  - Remove button
- Delete meals from history

#### API Calls
```
GET    /nutrition
POST   /nutrition/log-meal
DELETE /nutrition/meals/{id}
GET    /nutrition/meals
GET    /nutrition/daily-summary
```

#### State Management
```typescript
useNutritionStore() -> {
  meals: Meal[],
  dailyGoals: Goals | null,
  setMeals(meals),
  setDailyGoals(goals)
}
```

### 5. AI Coach Chat 🤖

**Location**: `src/app/coach/page.tsx`

Real-time chat interface with AI fitness coach.

#### Features
- **Real-time Messaging**: Send/receive messages instantly
- **Chat History**: View previous conversations
- **Suggested Topics**: Quick-start conversation suggestions
  - "What workout should I do today?"
  - "How should I structure my nutrition?"
  - "Tips for staying motivated?"
  - "How to prevent workout injuries?"

#### Chat Interface
- Message display with timestamps
- User messages (right-aligned, blue)
- Assistant messages (left-aligned, gray)
- Typing indicator with animation
- Auto-scroll to latest message
- Input field with send button

#### Message Structure
```typescript
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}
```

#### API Calls
```
GET  /coach/chat-history
POST /coach/chat
```

#### Features to Extend
- File uploads for form checks
- Voice input/output
- Context-aware responses based on user data
- Training plan recommendations

### 6. Progress Analytics 📈

**Location**: `src/app/progress/page.tsx`

Comprehensive analytics dashboard with multiple visualizations.

#### Key Metrics Cards
- **Total Workouts**: Lifetime count
- **Calories Burned**: Total calories
- **Weight Change**: Net weight change (kg)
- **Achievements**: Total badges unlocked

#### Charts

1. **Weight Progress** (Line Chart)
   - X-axis: Date
   - Y-axis: Weight (kg)
   - Track weight trends over time

2. **Workout Frequency** (Bar Chart)
   - X-axis: Day of week
   - Y-axis: Number of workouts
   - See weekly patterns

3. **Calories Burned** (Bar Chart)
   - X-axis: Date
   - Y-axis: Calories
   - Daily energy expenditure

4. **Workout Types** (Pie Chart)
   - Distribution of workout categories
   - Color-coded segments

#### Achievements Section
Trophy display with:
- Achievement title
- Description
- Unlock date

#### API Calls
```
GET /progress/analytics
Response: {
  total_workouts: number,
  total_calories_burned: number,
  weight_change: number,
  achievements: Achievement[],
  weight_history: WeightData[],
  workout_frequency: FrequencyData[],
  calories_history: CalorieData[],
  workout_types: TypeData[]
}
```

#### State Management
```typescript
useProgressStore() -> {
  metrics: Metric[],
  achievements: Achievement[],
  setMetrics(metrics),
  setAchievements(achievements)
}
```

### 7. Navigation 🧭

**Location**: `src/components/Navigation.tsx`

Persistent header navigation.

#### Features
- **Logo**: FitFlow branding
- **Protected Navigation**: Only shows when authenticated
- **Active Route Highlighting**: Current page highlighted
- **Mobile Menu**: Hamburger menu for mobile
- **User Profile**: Name and email display
- **Logout**: Sign out functionality

#### Navigation Links (Authenticated)
- 📊 Dashboard
- 💪 Workouts
- 🍎 Nutrition
- 🤖 Coach
- 📈 Progress

#### Mobile Responsive
- Desktop: Horizontal menu bar
- Mobile: Collapsible hamburger menu
- Touch-friendly button sizes

## API Client Configuration

**Location**: `src/lib/apiClient.ts`

Features:
- Automatic token inclusion in headers
- Base URL configuration from env
- Global error handling
- 401 redirect to login
- Request/response interceptors

```typescript
// Usage
import apiClient from '@/lib/apiClient';

const data = await apiClient.get('/endpoint');
```

## Styling System

### Tailwind CSS Components

**Buttons**
```css
.btn-primary    /* Blue primary button */
.btn-secondary  /* Pink secondary button */
```

**Cards**
```css
.card           /* Rounded white card with shadow */
```

**Forms**
```css
.input-field    /* Styled input with focus states */
```

**Background**
```css
.gradient-bg    /* Multi-color gradient */
```

### Color Palette
- **Primary**: `#6366f1` (Indigo) - Main CTA
- **Secondary**: `#ec4899` (Pink) - Alternative CTA
- **Accent**: `#f59e0b` (Amber) - Highlights
- **Success**: `#10b981` (Green)
- **Warning**: `#f59e0b` (Amber)
- **Danger**: `#ef4444` (Red)

## Protected Routes

All routes except login and register require authentication:
- Dashboard
- Workouts
- Nutrition
- Coach
- Progress

Unauthenticated users are redirected to login.

## Error Handling

### API Errors
- 401: Redirect to login
- 4xx: Display error message
- 5xx: Display server error message

### Form Validation
- Required field validation
- Email format validation
- Number validation
- Error message display

## Environment Variables

```
NEXT_PUBLIC_API_URL=http://localhost:8001
NODE_ENV=development
```

## Performance Optimizations

- Image optimization with Next.js Image component
- Component code splitting
- Dynamic imports for heavy components
- Efficient state management with Zustand
- Memoization for expensive computations

## Accessibility

- Semantic HTML structure
- ARIA labels on interactive elements
- Keyboard navigation support
- Color contrast compliance
- Focus indicators on buttons

## Mobile Responsiveness

- Mobile-first CSS
- Responsive grid layouts
- Touch-friendly buttons
- Adaptive navigation
- Optimized font sizes

---

**For detailed setup and development instructions, see [SETUP.md](./SETUP.md)**
