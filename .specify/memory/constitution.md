<!--
Sync Impact Report:
- Version change: 1.0.0 (Initial)
- Modified Principles: All placeholders replaced with Hackathon Phase-2 principles
- Added Sections: Security Guardrails, Technology Stack
- Templates requiring updates: All SDD templates aligned with multi-user JWT principles
- Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development MUST follow the sequence: Constitution → Specification → Plan → Tasks → Implementation. No code may be written without an approved specification and implementation plan. This ensures deterministic, reproducible, and verifiable development.

### II. Security-First & User Isolation
The system MUST guarantee strict user isolation. Unauthorized requests (missing or invalid JWT) MUST return HTTP 401. All database queries and mutations MUST be filtered by the authenticated user's ID. Users must never be able to access or modify data belonging to another user.

### III. Stateless API Design
Backend APIs MUST be RESTful and stateless. Authentication MUST be handled via JWT tokens verifying a shared secret. No server-side sessions or shared state (outside the database) are permitted, ensuring the backend can scale and remain predictable.

### IV. Agentic Implementation Only
All implementation tasks MUST be performed by specialized agents (auth-agent, neon-db-architect, nextjs-app-router-expert, etc.) via Claude Code. Manual coding is strictly prohibited to maintain the integrity of the SDD process.

### V. Testable & Atomic Tasks
Implementation plans MUST be broken into atomic, testable tasks. Each task MUST have associated acceptance criteria that verify functionality and security constraints (e.g., unauthorized access rejection).

### VI. Production-Grade Minimalism
Despite the basic feature scope, the architecture MUST follow production-grade standards: explicit error handling, sensitive data protection (no secrets in code), responsive UI, and persistent storage using Neon PostgreSQL.

## Security Guardrails
- **JWT Verification**: Every protected backend request must verify the JWT signature and expiration.
- **Environment Safety**: Shared secrets and database credentials must only be accessed via environment variables.
- **Input Validation**: All user input must be validated at the system boundaries (Frontend and Backend).

## Technology Stack
- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI with SQLModel (ORM)
- **Authentication**: Better Auth with JWT plugin
- **Database**: Neon Serverless PostgreSQL

## Governance
This constitution is the supreme authority for the project. Any deviations require a formal amendment and a version bump. All PRs and automated reviews MUST verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09
