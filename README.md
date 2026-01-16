# FitFlow Frontend

A comprehensive Next.js frontend for the FitFlow multi-agent AI fitness platform.

## Features

- **User Authentication**: Secure login and registration with JWT tokens
- **Dashboard**: Overview of your fitness metrics, recent workouts, and daily goals
- **Workout Plans**: View, create, and track personalized AI-generated workout plans
- **Nutrition Tracking**: Log meals and track daily nutritional intake (calories, protein, carbs, fat)
- **AI Coach**: Chat with an intelligent fitness coach for personalized guidance
- **Progress Analytics**: Visualize your fitness journey with detailed charts and achievements
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios
- **Charts**: Recharts
- **Date Formatting**: date-fns

## Installation

```bash
# Install dependencies
npm install

# Set up environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > .env.local
```

## Development

```bash
# Start development server
npm run dev

# Build for production
npm build

# Start production server
npm start
```

The application will be available at `http://localhost:3000`

## API Integration

The frontend integrates with the FastAPI backend at `http://localhost:8001`. Key endpoints:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /user/dashboard` - Dashboard data
- `GET /workouts` - List workouts
- `POST /workouts` - Create workout
- `POST /workouts/{id}/start` - Start a workout
- `GET /nutrition` - Nutrition data
- `POST /nutrition/log-meal` - Log a meal
- `POST /coach/chat` - Chat with AI coach
- `GET /progress/analytics` - Analytics data

## Project Structure

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/page.tsx
│   ├── workouts/page.tsx
│   ├── nutrition/page.tsx
│   ├── coach/page.tsx
│   ├── progress/page.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── Navigation.tsx
│   └── DashboardCard.tsx
├── lib/
│   ├── apiClient.ts
│   └── store.ts
└── globals.css
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8001)

## Authentication

The app uses JWT token-based authentication. Tokens are stored in localStorage and automatically sent with API requests.

## Styling

- Custom Tailwind CSS configuration with primary, secondary, and accent colors
- Responsive grid layouts
- Card-based UI components
- Smooth animations and transitions

## Features Details

### Dashboard
- Real-time stats (workouts, calories, progress, streak)
- Recent workouts feed
- Daily nutrition goals with progress bars
- Quick action buttons

### Workouts
- Create custom workout plans
- View all workouts
- Start workouts with tracking
- Filter by intensity level

### Nutrition
- Log meals with macros (protein, carbs, fat, calories)
- Daily macro tracking
- Goal progress indicators
- Meal history

### AI Coach
- Real-time chat interface
- AI-powered fitness guidance
- Suggested topics
- Chat history

### Progress
- Weight tracking chart
- Workout frequency analytics
- Calories burned insights
- Achievement badges
- Multiple chart types (line, bar, pie)

## License

MIT
