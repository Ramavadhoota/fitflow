# FitFlow Frontend - Quick Start Guide

## Prerequisites

- Node.js 16+ and npm/yarn
- FastAPI backend running at http://localhost:8001

## Setup

### 1. Install Dependencies

```bash
cd /workspaces/fitflow/frontend
npm install
```

### 2. Configure Environment Variables

The `.env.local` file is already configured with:
```
NEXT_PUBLIC_API_URL=http://localhost:8001
```

Update if your backend is running on a different URL.

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at **http://localhost:3000**

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── page.tsx           # Home page
│   │   ├── layout.tsx         # Root layout
│   │   ├── globals.css        # Global styles
│   │   ├── login/
│   │   │   └── page.tsx       # Login page
│   │   ├── register/
│   │   │   └── page.tsx       # Registration page
│   │   ├── dashboard/
│   │   │   └── page.tsx       # Dashboard (protected)
│   │   ├── workouts/
│   │   │   └── page.tsx       # Workout plans page
│   │   ├── nutrition/
│   │   │   └── page.tsx       # Nutrition tracking page
│   │   ├── coach/
│   │   │   └── page.tsx       # AI coach chat page
│   │   └── progress/
│   │       └── page.tsx       # Progress analytics page
│   │
│   ├── components/             # Reusable components
│   │   ├── Navigation.tsx      # Navigation bar
│   │   └── DashboardCard.tsx   # Dashboard stat card
│   │
│   └── lib/                    # Utilities
│       ├── apiClient.ts        # Axios API client
│       └── store.ts            # Zustand state management
│
├── package.json               # Dependencies
├── tailwind.config.js         # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
├── next.config.js             # Next.js configuration
├── postcss.config.js          # PostCSS configuration
└── .env.local                 # Environment variables
```

## Features Implemented

### 🏠 Home Page
- Landing page with feature highlights
- Call-to-action buttons for sign-in and registration

### 🔐 Authentication
- **Login**: Email + password authentication
- **Register**: User registration with fitness level selection
- JWT token-based security
- Automatic redirect for unauthenticated users

### 📊 Dashboard
- Quick stats overview (workouts, calories, progress, streak)
- Recent workouts feed
- Daily nutrition goals with progress bars
- Quick action buttons

### 💪 Workout Plans
- View personalized workout plans
- Create new workouts with custom exercises
- Start workouts with tracking
- Filter by intensity level
- Calories burned tracking

### 🍎 Nutrition Tracking
- Log meals with full macros (calories, protein, carbs, fat)
- Daily macro counter
- Progress bars for each macro
- Meal history and management
- Goal-based tracking

### 🤖 AI Coach
- Real-time chat interface
- Chat with AI fitness coach
- Suggested conversation topics
- Chat history
- Message timestamps

### 📈 Progress Analytics
- Weight progress line chart
- Workout frequency bar chart
- Calories burned visualization
- Workout type distribution pie chart
- Achievement badges
- Key metrics overview

### 🧭 Navigation
- Sticky navigation bar
- Protected routes (redirect to login if not authenticated)
- Mobile-responsive menu
- User profile display

## API Integration

The frontend connects to the FastAPI backend with these key endpoints:

```
Authentication:
  POST   /auth/register              Register user
  POST   /auth/login                 Login user

Dashboard:
  GET    /user/dashboard             Get dashboard data

Workouts:
  GET    /workouts                   List all workouts
  POST   /workouts                   Create workout
  POST   /workouts/{id}/start        Start workout

Nutrition:
  GET    /nutrition                  Get nutrition data
  POST   /nutrition/log-meal         Log meal
  DELETE /nutrition/meals/{id}       Delete meal

Coach:
  GET    /coach/chat-history         Get chat history
  POST   /coach/chat                 Send chat message

Progress:
  GET    /progress/analytics         Get analytics data
```

## State Management (Zustand)

The app uses Zustand for state management with these stores:

- `useAuthStore` - User authentication and profile
- `useWorkoutStore` - Workout data
- `useNutritionStore` - Nutrition and meal data
- `useProgressStore` - Progress metrics and achievements

## Styling

- **Framework**: Tailwind CSS
- **Color Scheme**:
  - Primary: `#6366f1` (Indigo)
  - Secondary: `#ec4899` (Pink)
  - Accent: `#f59e0b` (Amber)
- **Components**:
  - `.btn-primary` - Primary button
  - `.btn-secondary` - Secondary button
  - `.card` - Card component
  - `.input-field` - Input field
  - `.gradient-bg` - Gradient background

## Development Tips

### Adding New Pages

1. Create a new folder in `src/app/[feature]/`
2. Add `page.tsx` with your page component
3. Use `useAuthStore` to check authentication
4. Redirect to login if needed using `useRouter`

### Adding API Calls

```typescript
import apiClient from '@/lib/apiClient';

// GET request
const response = await apiClient.get('/endpoint');

// POST request
const response = await apiClient.post('/endpoint', data);

// PUT request
const response = await apiClient.put('/endpoint', data);

// DELETE request
await apiClient.delete('/endpoint');
```

### Using State Management

```typescript
import { useAuthStore, useWorkoutStore } from '@/lib/store';

const MyComponent = () => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { workouts, setWorkouts } = useWorkoutStore();

  // Use store values and setters
};
```

## Building for Production

```bash
# Build the app
npm run build

# Start production server
npm start
```

## Troubleshooting

### API Connection Issues
- Ensure backend is running at http://localhost:8001
- Check `.env.local` for correct `NEXT_PUBLIC_API_URL`
- Check browser console for CORS errors

### Authentication Issues
- Clear localStorage and refresh page
- Check if token is being stored: `localStorage.getItem('token')`
- Verify API returns proper token response

### Styling Issues
- Run `npm install` to ensure all dependencies are installed
- Clear `.next` cache: `rm -rf .next`
- Restart dev server

## Next Steps

1. Install dependencies: `npm install`
2. Start the backend FastAPI server at http://localhost:8001
3. Run dev server: `npm run dev`
4. Open http://localhost:3000 in your browser
5. Create an account and explore the app

## Support

For issues with:
- **Frontend**: Check React/Next.js documentation
- **API Integration**: Verify backend endpoints
- **Styling**: See Tailwind CSS documentation
- **State Management**: Check Zustand docs

---

**Happy coding! 💪 Let's get fit with FitFlow!**
