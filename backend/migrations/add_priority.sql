-- Add priority column to tasks table
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(10) NOT NULL DEFAULT 'medium';

-- Add index for filtering by priority
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
