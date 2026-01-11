---
name: database-schema-design
description: Design relational database schemas, create tables, and manage migrations safely and efficiently.
---

# Database Schema Design

## Instructions

1. **Schema planning**
   - Identify entities and relationships
   - Define primary and foreign keys
   - Normalize data (up to 3NF where applicable)

2. **Table creation**
   - Choose appropriate data types
   - Apply constraints (NOT NULL, UNIQUE, CHECK)
   - Use indexes for performance-critical queries

3. **Migrations**
   - Create forward and rollback migrations
   - Keep migrations small and atomic
   - Version-control all schema changes

4. **Relationships**
   - One-to-one, one-to-many, many-to-many
   - Use junction tables where required
   - Enforce referential integrity

## Best Practices
- Use consistent naming conventions (snake_case)
- Avoid over-indexing
- Never modify production data without migrations
- Document schema decisions
- Test migrations on staging first

## Example Structure
```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  title VARCHAR(200) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
