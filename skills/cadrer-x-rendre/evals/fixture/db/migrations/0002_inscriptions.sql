CREATE TABLE sign_ups (
  id INTEGER PRIMARY KEY,
  workshop_id INTEGER NOT NULL REFERENCES workshops(id),
  member_id INTEGER NOT NULL REFERENCES members(id),
  signed_up_at TEXT NOT NULL,  -- ISO 8601, UTC
  cancelled_at TEXT,
  UNIQUE (workshop_id, member_id)
);
