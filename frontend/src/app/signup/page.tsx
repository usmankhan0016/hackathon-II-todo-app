'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { ArrowLeft, AlertCircle, Info } from 'lucide-react';

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
    <div className="min-h-screen bg-[#0B0F0E] flex items-center justify-center p-4">
      <div className="container">
        <div className="max-w-md mx-auto">
          {/* Card */}
          <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-8">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-[#E6F2EF] mb-3 tracking-tight">
                Create Account
              </h1>
              <p className="text-[#9FB3AD] text-base">
                Start organizing your tasks today
              </p>
            </div>

            {/* Error message */}
            {displayError && (
              <div className="mb-6 p-4 bg-[#0B0F0E] border border-[#E5484D] rounded-lg">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-[#E5484D] mt-0.5 flex-shrink-0" />
                  <p className="text-[#E5484D] text-sm font-medium flex-1">{displayError}</p>
                </div>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Email field */}
              <div className="space-y-2">
                <label htmlFor="email" className="block text-sm font-semibold text-[#E6F2EF]">
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-all duration-200 outline-none placeholder-[#6B7F7A] disabled:opacity-50 disabled:cursor-not-allowed"
                  placeholder="you@example.com"
                  disabled={isLoading}
                  required
                />
              </div>

              {/* Password field */}
              <div className="space-y-2">
                <label htmlFor="password" className="block text-sm font-semibold text-[#E6F2EF]">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-all duration-200 outline-none placeholder-[#6B7F7A] disabled:opacity-50 disabled:cursor-not-allowed"
                  placeholder="••••••••"
                  disabled={isLoading}
                  required
                />
                <p className="text-xs text-[#6B7F7A] mt-1.5 flex items-center gap-1.5">
                  <Info className="w-3.5 h-3.5" />
                  At least 8 characters required
                </p>
              </div>

              {/* Confirm password field */}
              <div className="space-y-2">
                <label htmlFor="confirmPassword" className="block text-sm font-semibold text-[#E6F2EF]">
                  Confirm Password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-all duration-200 outline-none placeholder-[#6B7F7A] disabled:opacity-50 disabled:cursor-not-allowed"
                  placeholder="••••••••"
                  disabled={isLoading}
                  required
                />
              </div>

              {/* Submit button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-6 px-6 py-4 bg-[#00E676] text-[#0B0F0E] font-semibold rounded-lg hover:bg-[#00C965] transition-all duration-200 transform hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating account...
                  </span>
                ) : (
                  'Create Account'
                )}
              </button>
            </form>

            {/* Sign in link */}
            <div className="mt-8 pt-6 border-t border-[#1F2A28]">
              <p className="text-center text-[#9FB3AD] text-sm">
                Already have an account?{' '}
                <Link
                  href="/login"
                  className="text-[#00E676] hover:text-[#00C965] font-semibold transition-colors duration-200 hover:underline"
                >
                  Sign in instead
                </Link>
              </p>
            </div>
          </div>

          {/* Back to home link */}
          <div className="text-center mt-6">
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-[#9FB3AD] hover:text-[#E6F2EF] text-sm font-medium transition-colors duration-200 bg-[#111716] border border-[#1F2A28] px-4 py-2 rounded-lg hover:border-[#00E676]"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
