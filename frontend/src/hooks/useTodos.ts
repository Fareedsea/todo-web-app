import { useState, useEffect } from 'react';
import apiClient from '@/lib/api';
import { Todo, TodoCreate, TodoUpdate } from '@/lib/types';

interface UseTodosReturn {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  fetchTodos: () => Promise<void>;
  createTodo: (todoData: TodoCreate) => Promise<void>;
  updateTodo: (id: string, updates: TodoUpdate) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}

export const useTodos = (): UseTodosReturn => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get<Todo[]>('/todos');
      setTodos(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch todos');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTodo = async (todoData: TodoCreate) => {
    try {
      setError(null);
      const response = await apiClient.post<Todo>('/todos', todoData);
      setTodos(prev => [...prev, response.data]);
    } catch (err: any) {
      setError(err.message || 'Failed to create todo');
      console.error('Error creating todo:', err);
    }
  };

  const updateTodo = async (id: string, updates: TodoUpdate) => {
    try {
      setError(null);
      const response = await apiClient.put<Todo>(`/todos/${id}`, updates);
      setTodos(prev => prev.map(todo => todo.id === id ? response.data : todo));
    } catch (err: any) {
      setError(err.message || 'Failed to update todo');
      console.error('Error updating todo:', err);
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      setError(null);
      await apiClient.delete(`/todos/${id}`);
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (err: any) {
      setError(err.message || 'Failed to delete todo');
      console.error('Error deleting todo:', err);
    }
  };

  return {
    todos,
    loading,
    error,
    fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
  };
};