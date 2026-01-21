'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, checkAuth } = useAuthStore();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    checkAuth();
    setIsChecking(false);
  }, [checkAuth]);

  useEffect(() => {
    if (!isChecking && isAuthenticated) {
      router.push('/tasks');
    }
  }, [isChecking, isAuthenticated, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="container">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Welcome to Todo App
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            A modern full-stack application for managing your tasks efficiently
          </p>

          <div className="flex gap-4 justify-center">
            <Link
              href="/signup"
              className="btn-primary text-lg px-8 py-3"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="btn-secondary text-lg px-8 py-3"
            >
              Sign In
            </Link>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card">
              <h3 className="text-xl font-semibold mb-2">Secure</h3>
              <p className="text-gray-600">
                JWT-based authentication with bcrypt password hashing
              </p>
            </div>
            <div className="card">
              <h3 className="text-xl font-semibold mb-2">Fast</h3>
              <p className="text-gray-600">
                Built with Next.js 16 and React Query for optimal performance
              </p>
            </div>
            <div className="card">
              <h3 className="text-xl font-semibold mb-2">Responsive</h3>
              <p className="text-gray-600">
                Works seamlessly on desktop, tablet, and mobile devices
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
