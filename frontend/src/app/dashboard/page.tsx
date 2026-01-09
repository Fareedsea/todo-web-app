'use client';

import { TodoList } from './components/TodoList';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';

import Link from 'next/link';

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl p-8 md:p-10 border border-gray-100 dark:border-gray-700 mb-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-8">
              <div>
                <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-3">
                  My Tasks
                </h1>
                <p className="text-gray-600 dark:text-gray-300 text-lg">
                  Stay organized and boost your productivity
                </p>
              </div>
              <div className="flex items-center space-x-4 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-gray-700 dark:to-gray-700 p-4 rounded-xl border border-gray-200 dark:border-gray-600">
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">0</div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">Pending</div>
                </div>
                <div className="w-px h-12 bg-gray-200 dark:bg-gray-600"></div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">0</div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">Completed</div>
                </div>
                <div className="w-px h-12 bg-gray-200 dark:bg-gray-600"></div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">0</div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">Total</div>
                </div>
              </div>
            </div>

            <div className="mt-8">
              <TodoList />
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}