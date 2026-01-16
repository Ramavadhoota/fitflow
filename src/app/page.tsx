'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { useEffect } from 'react';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen gradient-bg flex flex-col items-center justify-center p-6">
      <div className="text-center text-white max-w-2xl">
        <h1 className="text-5xl md:text-6xl font-bold mb-6">FitFlow</h1>
        <p className="text-xl md:text-2xl mb-8 text-gray-100">
          Your Multi-Agent AI Fitness Coach
        </p>
        <p className="text-lg mb-12 text-gray-100">
          Get personalized workout plans, nutrition tracking, and AI-powered coaching all in one place.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Link
            href="/login"
            className="btn-primary bg-white text-primary hover:bg-gray-100"
          >
            Sign In
          </Link>
          <Link
            href="/register"
            className="btn-secondary bg-white text-secondary hover:bg-gray-100"
          >
            Get Started
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 max-w-6xl">
        {[
          {
            icon: '💪',
            title: 'Smart Workouts',
            desc: 'AI-generated workout plans tailored to your fitness level',
          },
          {
            icon: '🍎',
            title: 'Nutrition Tracking',
            desc: 'Track meals and get personalized nutrition recommendations',
          },
          {
            icon: '📊',
            title: 'Progress Analytics',
            desc: 'Real-time insights into your fitness journey',
          },
        ].map((feature, i) => (
          <div key={i} className="card bg-white/10 backdrop-blur text-white">
            <div className="text-4xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
            <p className="text-gray-100">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
