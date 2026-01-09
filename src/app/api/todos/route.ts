import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  // In a real app, this would fetch from a database
  // For now, we'll return an empty array as todos are stored in localStorage
  return Response.json({ todos: [] });
}

export async function POST(request: NextRequest) {
  // In a real app, this would save to a database
  const body = await request.json();
  return Response.json({ success: true, todo: body });
}