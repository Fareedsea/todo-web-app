'use client';

import { useState, useEffect } from 'react';
import { TodoItem } from './TodoItem';
import { TodoForm } from './TodoForm';
import { useTodos } from '@/hooks/useTodos';
import { Todo } from '@/lib/types';

export const TodoList = () => {
  const { todos, loading, error, fetchTodos, createTodo, updateTodo, deleteTodo } = useTodos();
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  const handleCreateTodo = async (title: string, description?: string) => {
    await createTodo({ title, description });
    setShowForm(false);
  };

  const handleToggleComplete = async (id: string, currentStatus: boolean) => {
    await updateTodo(id, { isCompleted: !currentStatus });
  };

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    await updateTodo(id, updates);
  };

  const handleDeleteTodo = async (id: string) => {
    await deleteTodo(id);
  };

  // Calculate task statistics
  const totalTasks = todos.length;
  const completedTasks = todos.filter(todo => todo.isCompleted).length;
  const pendingTasks = totalTasks - completedTasks;

  return (
    <div className="space-y-6">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Your Tasks</h2>
          <p className="text-gray-600 dark:text-gray-300">Manage and organize your daily activities</p>
        </div>

        <div className="flex flex-wrap gap-4">
          <div className="flex items-center space-x-3 bg-gradient-to-r from-indigo-50 to-indigo-100 dark:from-indigo-900/20 dark:to-indigo-800/20 p-3 rounded-xl border border-indigo-200 dark:border-indigo-700/50">
            <div className="w-3 h-3 bg-indigo-500 rounded-full"></div>
            <div>
              <div className="text-lg font-semibold text-indigo-700 dark:text-indigo-300">{pendingTasks}</div>
              <div className="text-xs text-indigo-600 dark:text-indigo-400">Pending</div>
            </div>
          </div>

          <div className="flex items-center space-x-3 bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 p-3 rounded-xl border border-green-200 dark:border-green-700/50">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <div>
              <div className="text-lg font-semibold text-green-700 dark:text-green-300">{completedTasks}</div>
              <div className="text-xs text-green-600 dark:text-green-400">Completed</div>
            </div>
          </div>

          <div className="flex items-center space-x-3 bg-gradient-to-r from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 p-3 rounded-xl border border-purple-200 dark:border-purple-700/50">
            <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
            <div>
              <div className="text-lg font-semibold text-purple-700 dark:text-purple-300">{totalTasks}</div>
              <div className="text-xs text-purple-600 dark:text-purple-400">Total</div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition-all duration-200 shadow-lg hover:shadow-xl flex items-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>{showForm ? 'Cancel' : '+ Add New Task'}</span>
          </button>

          <div className="flex space-x-2">
            <button className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200">
              All
            </button>
            <button className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200">
              Active
            </button>
            <button className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200">
              Completed
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-xl flex items-center space-x-3" role="alert">
          <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {showForm && (
        <div className="mb-6 bg-gradient-to-br from-white to-gray-50 dark:from-gray-700/50 dark:to-gray-800/50 p-6 rounded-2xl border border-gray-200 dark:border-gray-600 transition-all duration-300 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <svg className="w-5 h-5 mr-2 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create New Task
            </h3>
          </div>
          <TodoForm onSubmit={handleCreateTodo} onCancel={() => setShowForm(false)} />
        </div>
      )}

      {loading ? (
        <div className="flex flex-col items-center justify-center py-16">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-indigo-200 dark:border-gray-700 rounded-full animate-spin border-t-indigo-600 dark:border-t-indigo-400"></div>
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
              <svg className="w-8 h-8 text-indigo-600 dark:text-indigo-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
          <span className="mt-4 text-gray-600 dark:text-gray-400 font-medium">Loading your tasks...</span>
        </div>
      ) : (
        <div className="space-y-4">
          {todos.length === 0 ? (
            <div className="text-center py-16 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700/30 dark:to-gray-800/30 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-8 transition-all duration-300">
              <div className="mx-auto w-24 h-24 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 dark:from-indigo-900/20 dark:to-purple-900/20 flex items-center justify-center mb-6">
                <svg className="w-12 h-12 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
              <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-3">No tasks yet</h3>
              <p className="text-gray-600 dark:text-gray-400 text-lg max-w-md mx-auto mb-6">Get started by adding a new task to your list. Click the button above to create your first task.</p>
              <button
                onClick={() => setShowForm(true)}
                className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                Create Your First Task
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {todos.map(todo => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  onToggleComplete={handleToggleComplete}
                  onUpdate={handleUpdateTodo}
                  onDelete={handleDeleteTodo}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};