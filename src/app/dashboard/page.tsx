'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/apiClient';
import { useAuthStore, useWorkoutStore, useNutritionStore, useProgressStore } from '@/lib/store';
import DashboardCard from '@/components/DashboardCard';
import { format } from 'date-fns';

export default function Dashboard() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchDashboardData = async () => {
      try {
        const response = await apiClient.get('/user/dashboard');
        setStats(response.data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [isAuthenticated, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">
            Welcome, {user?.name}!
          </h1>
          <p className="text-gray-600 mt-2">{format(new Date(), 'EEEE, MMMM d, yyyy')}</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <DashboardCard
            title="Workouts This Week"
            value={stats?.workouts_this_week || 0}
            icon="💪"
            color="bg-blue-100"
          />
          <DashboardCard
            title="Calories Today"
            value={`${stats?.calories_today || 0} kcal`}
            icon="🔥"
            color="bg-orange-100"
          />
          <DashboardCard
            title="Goal Progress"
            value={`${stats?.goal_progress || 0}%`}
            icon="📊"
            color="bg-green-100"
          />
          <DashboardCard
            title="Streak Days"
            value={stats?.streak_days || 0}
            icon="🔥"
            color="bg-red-100"
          />
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Workouts */}
          <div className="lg:col-span-2 card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Recent Workouts</h2>
              <a href="/workouts" className="text-primary font-semibold hover:underline">
                View All
              </a>
            </div>

            <div className="space-y-4">
              {stats?.recent_workouts?.length ? (
                stats.recent_workouts.map((workout: any) => (
                  <div key={workout.id} className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold text-gray-900">{workout.name}</h3>
                        <p className="text-sm text-gray-600">
                          {workout.duration} min • {workout.exercises} exercises
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-semibold text-green-600">
                          +{workout.calories} kcal
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-600 text-center py-8">No workouts yet. Start today!</p>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="space-y-4">
            <div className="card">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h2>
              <div className="space-y-2">
                <a
                  href="/workouts"
                  className="block w-full text-center py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary/90"
                >
                  Start Workout
                </a>
                <a
                  href="/nutrition"
                  className="block w-full text-center py-3 bg-secondary text-white rounded-lg font-semibold hover:bg-secondary/90"
                >
                  Log Meal
                </a>
                <a
                  href="/coach"
                  className="block w-full text-center py-3 bg-accent text-white rounded-lg font-semibold hover:bg-accent/90"
                >
                  Chat with Coach
                </a>
              </div>
            </div>

            <div className="card">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Today's Goals</h2>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="font-semibold">Calories</span>
                    <span className="text-gray-600">{stats?.calories_today || 0} / 2000</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-orange-500 h-2 rounded-full"
                      style={{
                        width: `${Math.min(((stats?.calories_today || 0) / 2000) * 100, 100)}%`,
                      }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="font-semibold">Protein</span>
                    <span className="text-gray-600">{stats?.protein_today || 0}g / 150g</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{
                        width: `${Math.min(((stats?.protein_today || 0) / 150) * 100, 100)}%`,
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
