/**
 * Utility functions for secure JWT storage
 */

// Store JWT token
export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
};

// Get JWT token
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
};

// Remove JWT token
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
  }
};

// Check if token exists
export const hasToken = (): boolean => {
  return !!getToken();
};

// Get token expiration time
export const getTokenExpiration = (): number | null => {
  const token = getToken();
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp ? payload.exp * 1000 : null; // Convert to milliseconds
  } catch (error) {
    console.error('Error parsing token:', error);
    return null;
  }
};

// Check if token is expired
export const isTokenExpired = (): boolean => {
  const expiration = getTokenExpiration();
  if (!expiration) return true;

  return Date.now() > expiration;
};

// Check if token will expire soon (within 5 minutes)
export const isTokenExpiringSoon = (): boolean => {
  const expiration = getTokenExpiration();
  if (!expiration) return true;

  const fiveMinutes = 5 * 60 * 1000; // 5 minutes in milliseconds
  return Date.now() + fiveMinutes > expiration;
};