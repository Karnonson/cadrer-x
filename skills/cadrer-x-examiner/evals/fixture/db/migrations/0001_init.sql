CREATE TABLE workshops (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  starts_at TEXT NOT NULL,  -- ISO 8601, UTC
  seats INTEGER NOT NULL CHECK (seats > 0)
);

CREATE TABLE members (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'member' CHECK (role IN ('member', 'organizer'))
);
