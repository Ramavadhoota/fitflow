import { create } from 'zustand';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: true }),
  setToken: (token) => set({ token }),
  logout: () => {
    set({ user: null, token: null, isAuthenticated: false });
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  },
}));

interface WorkoutStore {
  workouts: any[];
  selectedWorkout: any | null;
  setWorkouts: (workouts: any[]) => void;
  setSelectedWorkout: (workout: any) => void;
}

export const useWorkoutStore = create<WorkoutStore>((set) => ({
  workouts: [],
  selectedWorkout: null,
  setWorkouts: (workouts) => set({ workouts }),
  setSelectedWorkout: (workout) => set({ selectedWorkout: workout }),
}));

interface NutritionStore {
  meals: any[];
  dailyGoals: any | null;
  setMeals: (meals: any[]) => void;
  setDailyGoals: (goals: any) => void;
}

export const useNutritionStore = create<NutritionStore>((set) => ({
  meals: [],
  dailyGoals: null,
  setMeals: (meals) => set({ meals }),
  setDailyGoals: (goals) => set({ dailyGoals: goals }),
}));

interface ProgressStore {
  metrics: any[];
  achievements: any[];
  setMetrics: (metrics: any[]) => void;
  setAchievements: (achievements: any[]) => void;
}

export const useProgressStore = create<ProgressStore>((set) => ({
  metrics: [],
  achievements: [],
  setMetrics: (metrics) => set({ metrics }),
  setAchievements: (achievements) => set({ achievements }),
}));
