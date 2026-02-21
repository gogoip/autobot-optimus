-- Core schema placeholder for local development
CREATE TABLE IF NOT EXISTS conversations (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS approvals (
  id INTEGER PRIMARY KEY,
  conversation_id INTEGER NOT NULL,
  action TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
