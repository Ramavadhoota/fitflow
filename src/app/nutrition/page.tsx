'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/apiClient';
import { useAuthStore, useNutritionStore } from '@/lib/store';

export default function NutritionPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const { meals, setMeals, dailyGoals } = useNutritionStore();
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [stats, setStats] = useState<any>(null);
  const [formData, setFormData] = useState({
    food_name: '',
    calories: '',
    protein: '',
    carbs: '',
    fat: '',
    quantity: '1',
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchNutritionData = async () => {
      try {
        const response = await apiClient.get('/nutrition');
        setMeals(response.data.meals || []);
        setStats(response.data);
      } catch (error) {
        console.error('Failed to fetch nutrition data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchNutritionData();
  }, [isAuthenticated, router, setMeals]);

  const handleAddMeal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/nutrition/log-meal', formData);
      setMeals([...meals, response.data]);
      setFormData({
        food_name: '',
        calories: '',
        protein: '',
        carbs: '',
        fat: '',
        quantity: '1',
      });
      setShowForm(false);

      // Update stats
      const statsResponse = await apiClient.get('/nutrition');
      setStats(statsResponse.data);
    } catch (error) {
      console.error('Failed to add meal:', error);
    }
  };

  const handleDeleteMeal = async (mealId: string) => {
    try {
      await apiClient.delete(`/nutrition/meals/${mealId}`);
      setMeals(meals.filter((m) => m.id !== mealId));
    } catch (error) {
      console.error('Failed to delete meal:', error);
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
            <h1 className="text-4xl font-bold text-gray-900">Nutrition Tracking</h1>
            <p className="text-gray-600 mt-2">Track your meals and nutritional intake</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="btn-primary"
          >
            {showForm ? 'Cancel' : '+ Log Meal'}
          </button>
        </div>

        {/* Daily Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Calories</h3>
            <p className="text-3xl font-bold text-primary">
              {stats?.total_calories || 0}
            </p>
            <p className="text-xs text-gray-600">Goal: 2000 kcal</p>
          </div>

          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Protein</h3>
            <p className="text-3xl font-bold text-blue-600">
              {stats?.total_protein || 0}g
            </p>
            <p className="text-xs text-gray-600">Goal: 150g</p>
          </div>

          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Carbs</h3>
            <p className="text-3xl font-bold text-yellow-600">
              {stats?.total_carbs || 0}g
            </p>
            <p className="text-xs text-gray-600">Goal: 250g</p>
          </div>

          <div className="card">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Fat</h3>
            <p className="text-3xl font-bold text-orange-600">
              {stats?.total_fat || 0}g
            </p>
            <p className="text-xs text-gray-600">Goal: 65g</p>
          </div>
        </div>

        {/* Add Meal Form */}
        {showForm && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold mb-6">Log Meal</h2>
            <form onSubmit={handleAddMeal} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Food Name
                </label>
                <input
                  type="text"
                  value={formData.food_name}
                  onChange={(e) =>
                    setFormData({ ...formData, food_name: e.target.value })
                  }
                  className="input-field"
                  placeholder="e.g., Chicken breast"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quantity
                  </label>
                  <input
                    type="text"
                    value={formData.quantity}
                    onChange={(e) =>
                      setFormData({ ...formData, quantity: e.target.value })
                    }
                    className="input-field"
                    placeholder="100g"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Calories
                  </label>
                  <input
                    type="number"
                    value={formData.calories}
                    onChange={(e) =>
                      setFormData({ ...formData, calories: e.target.value })
                    }
                    className="input-field"
                    placeholder="165"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Protein (g)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.protein}
                    onChange={(e) =>
                      setFormData({ ...formData, protein: e.target.value })
                    }
                    className="input-field"
                    placeholder="31"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Carbs (g)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.carbs}
                    onChange={(e) =>
                      setFormData({ ...formData, carbs: e.target.value })
                    }
                    className="input-field"
                    placeholder="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fat (g)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.fat}
                    onChange={(e) =>
                      setFormData({ ...formData, fat: e.target.value })
                    }
                    className="input-field"
                    placeholder="3.6"
                  />
                </div>
              </div>

              <button type="submit" className="btn-primary w-full">
                Log Meal
              </button>
            </form>
          </div>
        )}

        {/* Meals List */}
        <div className="card">
          <h2 className="text-2xl font-bold mb-6">Today's Meals</h2>
          {meals.length > 0 ? (
            <div className="space-y-4">
              {meals.map((meal) => (
                <div
                  key={meal.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                >
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {meal.food_name}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {meal.calories} cal • {meal.protein}g protein • {meal.carbs}g carbs • {meal.fat}g fat
                    </p>
                  </div>
                  <button
                    onClick={() => handleDeleteMeal(meal.id)}
                    className="text-red-600 hover:text-red-800 font-semibold"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 text-center py-8">
              No meals logged yet. Start logging!
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
