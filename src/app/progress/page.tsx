'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/apiClient';
import { useAuthStore, useProgressStore } from '@/lib/store';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

export default function ProgressPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const { metrics, achievements } = useProgressStore();
  const [loading, setLoading] = useState(true);
  const [analyticsData, setAnalyticsData] = useState<any>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchProgressData = async () => {
      try {
        const response = await apiClient.get('/progress/analytics');
        setAnalyticsData(response.data);
      } catch (error) {
        console.error('Failed to fetch progress data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProgressData();
  }, [isAuthenticated, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  const COLORS = ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#06b6d4'];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Progress Analytics</h1>
          <p className="text-gray-600 mt-2">
            Track your fitness journey and achievements
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">
              Total Workouts
            </h3>
            <p className="text-3xl font-bold text-primary">
              {analyticsData?.total_workouts || 0}
            </p>
          </div>

          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">
              Calories Burned
            </h3>
            <p className="text-3xl font-bold text-orange-600">
              {analyticsData?.total_calories_burned || 0}
            </p>
          </div>

          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">
              Weight Change
            </h3>
            <p className="text-3xl font-bold text-green-600">
              {analyticsData?.weight_change || 0} kg
            </p>
          </div>

          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">
              Achievements
            </h3>
            <p className="text-3xl font-bold text-secondary">
              {analyticsData?.achievements?.length || 0}
            </p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Weight Progress */}
          {analyticsData?.weight_history && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">
                Weight Progress
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={analyticsData.weight_history}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="weight"
                    stroke="#6366f1"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Workout Frequency */}
          {analyticsData?.workout_frequency && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">
                Workout Frequency
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analyticsData.workout_frequency}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="day"
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar
                    dataKey="workouts"
                    fill="#6366f1"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* Additional Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Calories Burned */}
          {analyticsData?.calories_history && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">
                Calories Burned
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analyticsData.calories_history}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar
                    dataKey="calories"
                    fill="#f59e0b"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Workout Types */}
          {analyticsData?.workout_types && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">
                Workout Types
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={analyticsData.workout_types}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => `${entry.name}: ${entry.value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {analyticsData.workout_types.map(
                      (entry: any, index: number) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      )
                    )}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* Achievements */}
        {analyticsData?.achievements && (
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 text-gray-900">
              🏆 Achievements
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {analyticsData.achievements.map((achievement: any, i: number) => (
                <div
                  key={i}
                  className="p-4 border-l-4 border-primary bg-blue-50 rounded"
                >
                  <h3 className="font-semibold text-gray-900">
                    {achievement.title}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {achievement.description}
                  </p>
                  <p className="text-xs text-gray-500 mt-2">
                    Unlocked {achievement.date}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
