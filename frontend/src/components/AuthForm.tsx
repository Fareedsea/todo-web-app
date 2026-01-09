import React, { useState } from 'react';
import { useRouter } from 'next/router';
import apiClient from '../services/api';

interface AuthFormProps {
  mode: 'signup' | 'signin';
}

const AuthForm: React.FC<AuthFormProps> = ({ mode }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (mode === 'signup') {
        // Validate password match
        if (password !== confirmPassword) {
          setError('Passwords do not match');
          setLoading(false);
          return;
        }

        // Validate password strength
        if (password.length < 8) {
          setError('Password must be at least 8 characters');
          setLoading(false);
          return;
        }

        // Make signup request
        await apiClient.post('/auth/signup', { email, password });
      } else {
        // Make signin request
        const response = await apiClient.post('/auth/signin', { email, password });

        // Store the token in localStorage
        if (response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token);
        }
      }

      // Redirect to dashboard after successful auth
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Auth error:', err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError(mode === 'signup'
          ? 'Failed to create account'
          : 'Failed to sign in');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form-container">
      <form onSubmit={handleSubmit} className="auth-form">
        <h2>{mode === 'signup' ? 'Create Account' : 'Sign In'}</h2>

        {error && <div className="error-message">{error}</div>}

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {mode === 'signup' && (
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password:</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : mode === 'signup' ? 'Sign Up' : 'Sign In'}
        </button>
      </form>

      <div className="auth-switch">
        {mode === 'signup' ? (
          <p>
            Already have an account?{' '}
            <a href="/auth/signin">Sign in here</a>
          </p>
        ) : (
          <p>
            Don't have an account?{' '}
            <a href="/auth/signup">Sign up here</a>
          </p>
        )}
      </div>
    </div>
  );
};

export default AuthForm;