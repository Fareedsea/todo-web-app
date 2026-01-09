# Todo Web Application

A modern, responsive todo application built with Next.js 16, TypeScript, and Tailwind CSS.

## Features

- User authentication (sign up/in)
- Task management with CRUD operations
- Filtering (all, active, completed)
- Statistics dashboard
- Dark/light mode support
- Responsive design for all devices
- Local storage persistence

## Tech Stack

- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- NextAuth.js
- Bcryptjs (for password hashing)
- Heroicons (for icons)

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
NEXTAUTH_SECRET=your-secret-key
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── api/             # API routes
│   │   └── auth/        # Authentication routes
│   ├── dashboard/       # Dashboard page
│   └── globals.css      # Global styles
├── components/          # Reusable components
│   ├── layout/          # Layout components
│   └── todo/            # Todo-specific components
├── types/               # TypeScript type definitions
└── lib/                 # Utility functions
```

## Environment Variables

- `NEXTAUTH_SECRET` - Secret for NextAuth (use a strong random string in production)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter