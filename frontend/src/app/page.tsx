'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';
import {
  CheckCircle2,
  Zap,
  Shield,
  Smartphone,
  Lock,
  Database,
  Code,
  Rocket,
  ArrowRight
} from 'lucide-react';

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
    <div className="min-h-screen bg-[#0B0F0E]">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-12 sm:py-16 md:py-24 px-4 sm:px-6 md:px-8">
        <div className="container max-w-7xl mx-auto relative z-10">
          <div className="text-center space-y-6 sm:space-y-8">
            {/* Hero Icon */}
            <div className="flex justify-center mb-4 sm:mb-6">
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-[#00E676] rounded-lg flex items-center justify-center transform hover:scale-105 transition-transform duration-200">
                <CheckCircle2 className="w-10 h-10 sm:w-12 sm:h-12 text-[#0B0F0E]" />
              </div>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-[#E6F2EF] mb-4 sm:mb-6 leading-tight">
              Welcome to{' '}
              <span className="text-[#00E676]">
                TaskFlow
              </span>
            </h1>

            {/* Subheadline */}
            <p className="text-lg sm:text-xl md:text-2xl text-[#9FB3AD] max-w-3xl mx-auto leading-relaxed px-4">
              A modern, secure, and lightning-fast task management application built with cutting-edge technology
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8 sm:mt-12 px-4">
              <Link
                href="/signup"
                className="group px-8 py-4 bg-[#00E676] text-[#0B0F0E] font-semibold rounded-lg hover:bg-[#00C965] transition-all duration-200 transform hover:-translate-y-0.5 active:scale-95 flex items-center justify-center gap-2"
              >
                Get Started
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/login"
                className="px-8 py-4 bg-transparent border-2 border-[#00E676] text-[#00E676] font-semibold rounded-lg hover:bg-[rgba(0,230,118,0.1)] hover:text-[#00C965] transition-all duration-200 transform hover:-translate-y-0.5 active:scale-95"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 sm:py-16 md:py-20 px-4 sm:px-6 md:px-8 bg-[#111716]">
        <div className="container max-w-7xl mx-auto">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[#E6F2EF] mb-4">
              Powerful Features
            </h2>
            <p className="text-lg sm:text-xl text-[#9FB3AD] max-w-2xl mx-auto">
              Everything you need to organize your tasks and boost productivity
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            {/* Feature 1: Secure */}
            <div className="group bg-[#111716] border border-[#1F2A28] rounded-lg p-6 sm:p-8 hover:border-[#00E676] transition-all duration-200">
              <div className="w-14 h-14 bg-[#00E676] rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-7 h-7 text-[#0B0F0E]" />
              </div>
              <h3 className="text-xl font-bold text-[#E6F2EF] mb-3">Secure Authentication</h3>
              <p className="text-[#9FB3AD] leading-relaxed">
                JWT-based authentication with bcrypt password hashing ensures your data is always protected
              </p>
            </div>

            {/* Feature 2: Fast */}
            <div className="group bg-[#111716] border border-[#1F2A28] rounded-lg p-6 sm:p-8 hover:border-[#00E676] transition-all duration-200">
              <div className="w-14 h-14 bg-[#00E676] rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-7 h-7 text-[#0B0F0E]" />
              </div>
              <h3 className="text-xl font-bold text-[#E6F2EF] mb-3">Lightning Fast</h3>
              <p className="text-[#9FB3AD] leading-relaxed">
                Built with Next.js 16 and React Query for optimal performance and instant updates
              </p>
            </div>

            {/* Feature 3: Responsive */}
            <div className="group bg-[#111716] border border-[#1F2A28] rounded-lg p-6 sm:p-8 hover:border-[#00E676] transition-all duration-200">
              <div className="w-14 h-14 bg-[#00E676] rounded-lg flex items-center justify-center mb-4">
                <Smartphone className="w-7 h-7 text-[#0B0F0E]" />
              </div>
              <h3 className="text-xl font-bold text-[#E6F2EF] mb-3">Fully Responsive</h3>
              <p className="text-[#9FB3AD] leading-relaxed">
                Seamlessly works across desktop, tablet, and mobile devices with a beautiful UI
              </p>
            </div>

            {/* Feature 4: User Isolation */}
            <div className="group bg-[#111716] border border-[#1F2A28] rounded-lg p-6 sm:p-8 hover:border-[#00E676] transition-all duration-200">
              <div className="w-14 h-14 bg-[#00E676] rounded-lg flex items-center justify-center mb-4">
                <Lock className="w-7 h-7 text-[#0B0F0E]" />
              </div>
              <h3 className="text-xl font-bold text-[#E6F2EF] mb-3">Data Privacy</h3>
              <p className="text-[#9FB3AD] leading-relaxed">
                Complete user isolation ensures your tasks remain private and secure
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="py-12 sm:py-16 md:py-20 px-4 sm:px-6 md:px-8 bg-[#0B0F0E]">
        <div className="container max-w-7xl mx-auto">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[#E6F2EF] mb-4">
              Built with Modern Tech
            </h2>
            <p className="text-lg sm:text-xl text-[#9FB3AD] max-w-2xl mx-auto">
              Powered by industry-leading technologies for reliability and performance
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 sm:gap-6">
            {/* Next.js */}
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-4 sm:p-6 hover:border-[#00E676] transition-all duration-200 flex flex-col items-center gap-3">
              <Code className="w-8 h-8 sm:w-10 sm:h-10 text-[#00E676]" />
              <p className="text-[#E6F2EF] font-semibold text-sm sm:text-base">Next.js 16</p>
            </div>

            {/* FastAPI */}
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-4 sm:p-6 hover:border-[#00E676] transition-all duration-200 flex flex-col items-center gap-3">
              <Zap className="w-8 h-8 sm:w-10 sm:h-10 text-[#00E676]" />
              <p className="text-[#E6F2EF] font-semibold text-sm sm:text-base">FastAPI</p>
            </div>

            {/* PostgreSQL */}
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-4 sm:p-6 hover:border-[#00E676] transition-all duration-200 flex flex-col items-center gap-3">
              <Database className="w-8 h-8 sm:w-10 sm:h-10 text-[#00E676]" />
              <p className="text-[#E6F2EF] font-semibold text-sm sm:text-base">PostgreSQL</p>
            </div>

            {/* JWT Auth */}
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-4 sm:p-6 hover:border-[#00E676] transition-all duration-200 flex flex-col items-center gap-3">
              <Lock className="w-8 h-8 sm:w-10 sm:h-10 text-[#00E676]" />
              <p className="text-[#E6F2EF] font-semibold text-sm sm:text-base">JWT Auth</p>
            </div>

            {/* TypeScript */}
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-4 sm:p-6 hover:border-[#00E676] transition-all duration-200 flex flex-col items-center gap-3">
              <Code className="w-8 h-8 sm:w-10 sm:h-10 text-[#00E676]" />
              <p className="text-[#E6F2EF] font-semibold text-sm sm:text-base">TypeScript</p>
            </div>

            {/* Tailwind */}
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-4 sm:p-6 hover:border-[#00E676] transition-all duration-200 flex flex-col items-center gap-3">
              <Rocket className="w-8 h-8 sm:w-10 sm:h-10 text-[#00E676]" />
              <p className="text-[#E6F2EF] font-semibold text-sm sm:text-base">Tailwind CSS</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 sm:py-16 md:py-24 px-4 sm:px-6 md:px-8 bg-[#111716]">
        <div className="container max-w-7xl mx-auto">
          <div className="bg-[#151C1B] border border-[#1F2A28] rounded-lg p-8 sm:p-12 md:p-16 text-center">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[#E6F2EF] mb-4 sm:mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-lg sm:text-xl text-[#9FB3AD] mb-8 sm:mb-10 max-w-2xl mx-auto">
              Join thousands of users who are already managing their tasks efficiently with TaskFlow
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/signup"
                className="group px-8 py-4 bg-[#00E676] text-[#0B0F0E] font-semibold rounded-lg hover:bg-[#00C965] transition-all duration-200 transform hover:-translate-y-0.5 active:scale-95 flex items-center justify-center gap-2"
              >
                Create Free Account
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/login"
                className="px-8 py-4 bg-transparent border-2 border-[#00E676] text-[#00E676] font-semibold rounded-lg hover:bg-[rgba(0,230,118,0.1)] hover:text-[#00C965] transition-all duration-200 transform hover:-translate-y-0.5 active:scale-95"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 sm:py-12 px-4 sm:px-6 md:px-8 bg-[#0B0F0E] border-t border-[#1F2A28]">
        <div className="container max-w-7xl mx-auto">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="text-[#6B7F7A] text-sm">
              &copy; 2026 TaskFlow. All rights reserved.
            </div>
            <div className="flex gap-6 text-sm">
              <Link href="#" className="text-[#6B7F7A] hover:text-[#E6F2EF] transition-colors">
                Privacy
              </Link>
              <Link href="#" className="text-[#6B7F7A] hover:text-[#E6F2EF] transition-colors">
                Terms
              </Link>
              <Link href="#" className="text-[#6B7F7A] hover:text-[#E6F2EF] transition-colors">
                Contact
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
