'use client';

import { useState, useEffect } from 'react';
import { signOut } from 'next-auth/react';
import { User } from 'next-auth';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import TodoList from '@/components/todo/TodoList';
import TodoForm from '@/components/todo/TodoForm';
import Statistics from '@/components/todo/Statistics';
import { Todo } from '@/types/todo';

interface DashboardClientProps {
  user: User;
}

export default function DashboardClient({ user }: DashboardClientProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  // Load todos from localStorage initially
  useEffect(() => {
    const savedTodos = localStorage.getItem('todos');
    if (savedTodos) {
      setTodos(JSON.parse(savedTodos));
    }
    setLoading(false);
  }, []);

  // Save todos to localStorage whenever they change
  useEffect(() => {
    if (!loading) {
      localStorage.setItem('todos', JSON.stringify(todos));
    }
  }, [todos, loading]);

  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });

  const addTodo = (text: string) => {
    const newTodo: Todo = {
      id: Date.now().toString(),
      text,
      completed: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setTodos([newTodo, ...todos]);
  };

  const toggleTodo = (id: string) => {
    setTodos(todos.map(todo =>
      todo.id === id
        ? { ...todo, completed: !todo.completed, updatedAt: new Date().toISOString() }
        : todo
    ));
  };

  const deleteTodo = (id: string) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  const updateTodo = (id: string, text: string) => {
    setTodos(todos.map(todo =>
      todo.id === id
        ? { ...todo, text, updatedAt: new Date().toISOString() }
        : todo
    ));
  };

  const clearCompleted = () => {
    setTodos(todos.filter(todo => !todo.completed));
  };

  const stats = {
    total: todos.length,
    completed: todos.filter(todo => todo.completed).length,
    active: todos.filter(todo => !todo.completed).length,
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        user={user}
        onSignOut={() => signOut({ callbackUrl: '/' })}
      />

      <div className="lg:pl-64">
        <Header
          user={user}
          onMenuClick={() => setSidebarOpen(true)}
          onSignOut={() => signOut({ callbackUrl: '/' })}
        />

        <main className="py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">My Tasks</h1>
              <p className="text-gray-600 dark:text-gray-400">
                {stats.active > 0
                  ? `You have ${stats.active} active task${stats.active !== 1 ? 's' : ''}`
                  : 'No active tasks - add a new one to get started!'}
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <TodoForm onAddTodo={addTodo} />

                <div className="mt-8">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {filter === 'all' ? 'All Tasks' :
                       filter === 'active' ? 'Active Tasks' : 'Completed Tasks'}
                    </h2>

                    <div className="flex flex-wrap gap-2">
                      <button
                        onClick={() => setFilter('all')}
                        className={`px-3 py-1.5 text-sm rounded-md ${
                          filter === 'all'
                            ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-200'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
                        }`}
                      >
                        All
                      </button>
                      <button
                        onClick={() => setFilter('active')}
                        className={`px-3 py-1.5 text-sm rounded-md ${
                          filter === 'active'
                            ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-200'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
                        }`}
                      >
                        Active
                      </button>
                      <button
                        onClick={() => setFilter('completed')}
                        className={`px-3 py-1.5 text-sm rounded-md ${
                          filter === 'completed'
                            ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-200'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
                        }`}
                      >
                        Completed
                      </button>
                    </div>
                  </div>

                  <TodoList
                    todos={filteredTodos}
                    onToggleTodo={toggleTodo}
                    onDeleteTodo={deleteTodo}
                    onUpdateTodo={updateTodo}
                  />
                </div>
              </div>

              <div className="space-y-6">
                <Statistics stats={stats} onClearCompleted={clearCompleted} />

                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Stats</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Completion Rate</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Tasks Today</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {todos.filter(todo =>
                          new Date(todo.createdAt).toDateString() === new Date().toDateString()
                        ).length}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Avg. Completion</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {stats.total > 0 ? (stats.completed / stats.total).toFixed(2) : 0}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}