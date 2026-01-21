'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { useAuthStore } from '@/stores/authStore';

export default function SignupPage() {
  const router = useRouter();
  const { signup, isLoading, error, clearError } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [clientError, setClientError] = useState('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    clearError();
    setClientError('');

    // Validation
    if (!email || !password || !confirmPassword) {
      setClientError('Please fill in all fields');
      return;
    }

    if (!email.includes('@')) {
      setClientError('Please enter a valid email address');
      return;
    }

    if (password.length < 8) {
      setClientError('Password must be at least 8 characters long');
      return;
    }

    if (password !== confirmPassword) {
      setClientError('Passwords do not match');
      return;
    }

    try {
      await signup(email, password);
      router.push('/tasks');
    } catch {
      // Error is already set in store
    }
  };

  const displayError = clientError || error;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="container">
        <div className="max-w-md mx-auto">
          <div className="card">
            <h1 className="text-3xl font-bold text-gray-900 mb-2 text-center">
              Create Account
            </h1>
            <p className="text-gray-600 text-center mb-8">
              Get started with your todo app today
            </p>

            {displayError && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="error-text">{displayError}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-base"
                  placeholder="you@example.com"
                  disabled={isLoading}
                  required
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-base"
                  placeholder="••••••••"
                  disabled={isLoading}
                  required
                />
                <p className="text-xs text-gray-500 mt-1">
                  At least 8 characters
                </p>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                  Confirm Password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="input-base"
                  placeholder="••••••••"
                  disabled={isLoading}
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full btn-primary py-3 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Creating account...' : 'Sign Up'}
              </button>
            </form>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <p className="text-center text-gray-600">
                Already have an account?{' '}
                <Link href="/login" className="text-blue-600 hover:text-blue-700 font-medium">
                  Sign in
                </Link>
              </p>
            </div>
          </div>

          <p className="text-center text-gray-600 text-sm mt-4">
            <Link href="/" className="text-blue-600 hover:text-blue-700">
              ← Back to home
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
