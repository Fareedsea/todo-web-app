import { NextRequest } from 'next/server';
import bcrypt from 'bcryptjs';

// Mock user database (in a real app, this would be a real database)
let mockUsers: any[] = [];

if (typeof window === 'undefined') {
  // Server-side initialization
  if (global.mockUsers === undefined) {
    global.mockUsers = [];
  }
  mockUsers = global.mockUsers;
}

export async function POST(request: NextRequest) {
  try {
    const { email, password, name } = await request.json();

    // Validate input
    if (!email || !password || !name) {
      return Response.json(
        { message: 'Email, password, and name are required' },
        { status: 400 }
      );
    }

    // Check if user already exists
    const existingUser = mockUsers.find((user) => user.email === email);
    if (existingUser) {
      return Response.json(
        { message: 'User with this email already exists' },
        { status: 400 }
      );
    }

    // Validate password strength
    if (password.length < 6) {
      return Response.json(
        { message: 'Password must be at least 6 characters long' },
        { status: 400 }
      );
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create new user
    const newUser = {
      id: Date.now(), // In a real app, use UUID or similar
      email,
      password: hashedPassword,
      name,
      createdAt: new Date().toISOString(),
    };

    mockUsers.push(newUser);

    // Return success response (without password)
    const { password: _, ...userWithoutPassword } = newUser;
    return Response.json(
      { message: 'User created successfully', user: userWithoutPassword },
      { status: 201 }
    );
  } catch (error) {
    console.error('Signup error:', error);
    return Response.json(
      { message: 'Internal server error' },
      { status: 500 }
    );
  }
}