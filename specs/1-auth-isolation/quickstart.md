# Quickstart: Authentication & User Isolation

**Date**: 2026-01-09
**Feature**: Authentication & User Isolation
**Phase**: 1 Design

## Overview

This guide provides a quick implementation path for the authentication and user isolation feature using the established design patterns and contracts.

## Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with npm
- PostgreSQL database (Neon Serverless recommended)
- Better Auth with JWT plugin installed
- FastAPI and Next.js development environment

## Backend Implementation (FastAPI)

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pydantic sqlalchemy sqlmodel python-jose bcrypt
pip install better-auth  # Hypothetical package for Better Auth integration
```

### 2. Configure Environment Variables

Create `.env` file:

```bash
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/todo_app

# Application Configuration
DEBUG=true
```

### 3. Implement User Model

```python
# backend/src/auth/models.py
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4. Implement JWT Middleware

```python
# backend/src/auth/middleware.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = jwt.decode(jwtoken, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
            return True
        except JWTError:
            return False
```

### 5. Implement Authentication Endpoints

```python
# backend/src/api/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import Annotated
from datetime import datetime, timedelta
from jose import jwt
import bcrypt
import os

from ..auth.models import User
from ..auth.middleware import JWTBearer
from ..core.config import get_session

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
async def signup(email: str, password: str, session: Annotated[Session, Depends(get_session)]):
    # Check if user exists
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user
    user = User(email=email, password_hash=password_hash.decode('utf-8'))
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User registered successfully", "user": {"id": user.id, "email": user.email}}

@router.post("/signin")
async def signin(email: str, password: str, session: Annotated[Session, Depends(get_session)]):
    # Find user
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT
    expires_delta = timedelta(hours=int(os.getenv("JWT_EXPIRATION_HOURS", 24)))
    expire = datetime.utcnow() + expires_delta

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": expire
    }

    access_token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_delta.total_seconds()
    }
```

## Frontend Implementation (Next.js)

### 1. Install Dependencies

```bash
npm install axios react-query @tanstack/react-query
npm install js-cookie  # For secure cookie handling
```

### 2. Create Authentication Service

```typescript
// frontend/src/services/auth.ts
import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const authApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to all requests
authApi.interceptors.request.use((config) => {
  const token = Cookies.get('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors
authApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      Cookies.remove('access_token');
      window.location.href = '/auth/signin';
    }
    return Promise.reject(error);
  }
);

export const authServices = {
  signup: async (email: string, password: string) => {
    const response = await authApi.post('/auth/signup', { email, password });
    return response.data;
  },

  signin: async (email: string, password: string) => {
    const response = await authApi.post('/auth/signin', { email, password });

    // Store token securely
    const token = response.data.access_token;
    Cookies.set('access_token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
    });

    return response.data;
  },

  getCurrentUser: async () => {
    const response = await authApi.get('/auth/me');
    return response.data;
  },

  logout: async () => {
    await authApi.post('/auth/logout');
    Cookies.remove('access_token');
  },
};
```

### 3. Create Authentication Hook

```typescript
// frontend/src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { authServices } from '../services/auth';
import Cookies from 'js-cookie';

interface User {
  id: string;
  email: string;
}

interface UseAuthReturn {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = Cookies.get('access_token');
      if (token) {
        try {
          const userData = await authServices.getCurrentUser();
          setUser(userData.user);
        } catch (error) {
          // Token is invalid, clear it
          Cookies.remove('access_token');
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const data = await authServices.signin(email, password);
      // Token is automatically stored by the service
      setUser({ id: data.user.id, email: data.user.email });
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      await authServices.signup(email, password);
      // Auto-login after registration
      await login(email, password);
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authServices.logout();
      setUser(null);
    } catch (error) {
      // Still clear local state even if server logout fails
      Cookies.remove('access_token');
      setUser(null);
    }
  };

  return {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
  };
};
```

### 4. Create Protected Route Component

```typescript
// frontend/src/components/ProtectedRoute.tsx
import { useAuth } from '../hooks/useAuth';
import { useRouter } from 'next/router';
import { useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/signin');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <>{children}</> : null;
};
```

### 5. Create Signup and Signin Pages

```tsx
// frontend/src/pages/auth/signup.tsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../../hooks/useAuth';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { register, isLoading } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await register(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed');
    }
  };

  return (
    <div>
      <h1>Sign Up</h1>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>
    </div>
  );
}
```

## Testing

### Backend Tests

```python
# backend/tests/unit/test_auth_service.py
def test_user_registration(client):
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "TestPassword123!"
    })
    assert response.status_code == 201
    assert "user" in response.json()

def test_user_authentication(client):
    # First register user
    client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "TestPassword123!"
    })

    # Then authenticate
    response = client.post("/auth/signin", json={
        "email": "test@example.com",
        "password": "TestPassword123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Frontend Tests

```typescript
// frontend/tests/unit/hooks/useAuth.test.ts
import { renderHook, act } from '@testing-library/react';
import { useAuth } from '../../src/hooks/useAuth';

jest.mock('../../src/services/auth');

describe('useAuth', () => {
  it('should login user successfully', async () => {
    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login('test@example.com', 'password');
    });

    expect(result.current.isAuthenticated).toBe(true);
  });
});
```

## Security Checklist

- [ ] JWT secret is stored in environment variables
- [ ] HTTPS is enforced in production
- [ ] Passwords are properly hashed with bcrypt
- [ ] JWT tokens have appropriate expiration times
- [ ] Cross-origin requests are properly configured
- [ ] Error messages don't leak sensitive information
- [ ] Authentication state is properly managed
- [ ] Token storage uses secure methods (HttpOnly cookies)

## Next Steps

1. Implement the Todo CRUD operations with user isolation
2. Add refresh token functionality for better UX
3. Implement password reset functionality
4. Add email verification for new accounts
5. Add rate limiting and additional security measures