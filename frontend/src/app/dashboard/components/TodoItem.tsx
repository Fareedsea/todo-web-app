import { useState } from 'react';
import { Todo } from '@/lib/types';

interface TodoItemProps {
  todo: Todo;
  onToggleComplete: (id: string, currentStatus: boolean) => void;
  onUpdate: (id: string, updates: Partial<Todo>) => void;
  onDelete: (id: string) => void;
}

export const TodoItem = ({ todo, onToggleComplete, onUpdate, onDelete }: TodoItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');

  const handleSave = () => {
    onUpdate(todo.id, { title: editTitle, description: editDescription });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleCancel();
    } else if (e.key === 'Enter' && e.ctrlKey) {
      handleSave();
    }
  };

  return (
    <div className={`border rounded-2xl p-6 shadow-sm transition-all duration-300 hover:shadow-lg ${todo.isCompleted ? 'bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-green-200 dark:border-green-800/50' : 'bg-gradient-to-r from-white to-gray-50 dark:from-gray-700/50 dark:to-gray-800/50 border-gray-200 dark:border-gray-600'}`}>
      {isEditing ? (
        <div className="space-y-5">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full p-4 border-2 rounded-xl text-lg font-semibold bg-white dark:bg-gray-600 text-gray-900 dark:text-white border-indigo-200 dark:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none"
            autoFocus
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full p-4 border-2 rounded-xl bg-white dark:bg-gray-600 text-gray-900 dark:text-white border-gray-200 dark:border-gray-500 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none"
            rows={3}
          />
          <div className="flex space-x-4 pt-2">
            <button
              onClick={handleSave}
              className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl hover:from-green-700 hover:to-emerald-700 transition-all duration-200 shadow-md hover:shadow-xl flex items-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span>Save</span>
            </button>
            <button
              onClick={handleCancel}
              className="px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-xl hover:from-gray-600 hover:to-gray-700 transition-all duration-200 shadow-md hover:shadow-xl flex items-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span>Cancel</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start space-x-4">
          <button
            onClick={() => onToggleComplete(todo.id, todo.isCompleted)}
            className={`flex-shrink-0 w-7 h-7 rounded-full border-2 flex items-center justify-center mt-1 transition-all duration-300 ${todo.isCompleted
              ? 'bg-gradient-to-r from-green-500 to-emerald-500 border-green-500 shadow-inner scale-110'
              : 'border-gray-300 dark:border-gray-500 hover:border-indigo-400 hover:scale-105'}`}
            aria-label={todo.isCompleted ? "Mark as incomplete" : "Mark as complete"}
          >
            {todo.isCompleted && (
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
          <div className="flex-1 min-w-0">
            <h3 className={`text-xl font-bold ${todo.isCompleted ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-900 dark:text-gray-100'}`}>
              {todo.title}
            </h3>
            {todo.description && (
              <p className={`mt-3 text-gray-600 dark:text-gray-300 ${todo.isCompleted ? 'line-through opacity-75' : ''}`}>
                {todo.description}
              </p>
            )}
            <div className="mt-4 flex flex-wrap items-center gap-4 text-sm">
              <div className="flex items-center text-gray-500 dark:text-gray-400">
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Created: {new Date(todo.createdAt).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center text-gray-500 dark:text-gray-400">
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Updated: {new Date(todo.updatedAt).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  todo.isCompleted
                    ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                    : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                }`}>
                  {todo.isCompleted ? 'Completed' : 'Pending'}
                </span>
              </div>
            </div>
          </div>
          <div className="flex flex-col space-y-2">
            <button
              onClick={() => setIsEditing(true)}
              className="p-2.5 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 rounded-xl hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors duration-200 flex items-center justify-center"
              aria-label="Edit"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
            <button
              onClick={() => onDelete(todo.id)}
              className="p-2.5 text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 rounded-xl hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors duration-200 flex items-center justify-center"
              aria-label="Delete"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};