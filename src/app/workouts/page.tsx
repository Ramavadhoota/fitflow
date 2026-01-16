'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/apiClient';
import { useAuthStore, useWorkoutStore } from '@/lib/store';

export default function WorkoutsPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const { workouts, setWorkouts, selectedWorkout } = useWorkoutStore();
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    duration: '',
    exercises: '',
    intensity: 'moderate',
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchWorkouts = async () => {
      try {
        const response = await apiClient.get('/workouts');
        setWorkouts(response.data.workouts || []);
      } catch (error) {
        console.error('Failed to fetch workouts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, [isAuthenticated, router, setWorkouts]);

  const handleAddWorkout = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/workouts', formData);
      setWorkouts([...workouts, response.data]);
      setFormData({ name: '', duration: '', exercises: '', intensity: 'moderate' });
      setShowForm(false);
    } catch (error) {
      console.error('Failed to add workout:', error);
    }
  };

  const handleStartWorkout = async (workoutId: string) => {
    try {
      const response = await apiClient.post(`/workouts/${workoutId}/start`);
      router.push(`/workouts/${workoutId}`);
    } catch (error) {
      console.error('Failed to start workout:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">Workout Plans</h1>
            <p className="text-gray-600 mt-2">Your personalized AI-generated workout plans</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="btn-primary"
          >
            {showForm ? 'Cancel' : '+ New Workout'}
          </button>
        </div>

        {/* Add Workout Form */}
        {showForm && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold mb-6">Create New Workout</h2>
            <form onSubmit={handleAddWorkout} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Workout Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="input-field"
                  placeholder="e.g., Morning Cardio"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Duration (minutes)
                  </label>
                  <input
                    type="number"
                    value={formData.duration}
                    onChange={(e) =>
                      setFormData({ ...formData, duration: e.target.value })
                    }
                    className="input-field"
                    placeholder="30"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Intensity
                  </label>
                  <select
                    value={formData.intensity}
                    onChange={(e) =>
                      setFormData({ ...formData, intensity: e.target.value })
                    }
                    className="input-field"
                  >
                    <option value="light">Light</option>
                    <option value="moderate">Moderate</option>
                    <option value="intense">Intense</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Exercises (comma-separated)
                </label>
                <textarea
                  value={formData.exercises}
                  onChange={(e) =>
                    setFormData({ ...formData, exercises: e.target.value })
                  }
                  className="input-field"
                  placeholder="Push-ups, Squats, Pull-ups"
                  rows={3}
                />
              </div>

              <button type="submit" className="btn-primary w-full">
                Create Workout
              </button>
            </form>
          </div>
        )}

        {/* Workouts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workouts.length > 0 ? (
            workouts.map((workout) => (
              <div key={workout.id} className="card">
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  {workout.name}
                </h3>
                <div className="space-y-2 mb-4 text-sm text-gray-600">
                  <p>⏱️ {workout.duration || 30} min</p>
                  <p>💪 {workout.exercises || 'Multiple'} exercises</p>
                  <p>
                    🔥 Intensity:{' '}
                    <span className="capitalize font-semibold">
                      {workout.intensity || 'moderate'}
                    </span>
                  </p>
                </div>
                <button
                  onClick={() => handleStartWorkout(workout.id)}
                  className="w-full btn-primary"
                >
                  Start Workout
                </button>
              </div>
            ))
          ) : (
            <div className="col-span-full card text-center py-12">
              <p className="text-gray-600 mb-4">No workouts yet. Create your first one!</p>
              <button
                onClick={() => setShowForm(true)}
                className="btn-primary"
              >
                Create Workout
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
