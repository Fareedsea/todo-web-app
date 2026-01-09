---
name: database-schema-design
description: Design robust databases by creating tables, migrations, and well-structured schemas. Use for backend and data-driven applications.
---

# Database Skill – Tables, Migrations & Schema Design

## Instructions

1. **Schema planning**
   - Identify entities and relationships
   - Define primary and foreign keys
   - Normalize data where appropriate

2. **Table creation**
   - Use clear, consistent naming conventions
   - Choose correct data types
   - Add constraints (NOT NULL, UNIQUE, DEFAULT)

3. **Migrations**
   - Version-control all schema changes
   - Write reversible (up/down) migrations
   - Keep migrations small and focused

4. **Relationships**
   - One-to-one, one-to-many, many-to-many
   - Index foreign keys
   - Enforce referential integrity

## Best Practices
- Use snake_case for table and column names
- Avoid premature optimization
- Index columns used in joins and searches
- Document schema decisions
- Test migrations in a staging environment
- Never modify old migrations in production

## Example Structure
```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  title VARCHAR(200) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_user
    FOREIGN KEY (user_id_
