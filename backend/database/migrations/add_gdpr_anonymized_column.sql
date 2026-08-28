-- Migration: Add gdpr_anonymized column to tickets table
-- For GDPR "right to erasure" tracking
-- Run this on existing databases

-- Add the column with default FALSE
ALTER TABLE tickets
ADD COLUMN IF NOT EXISTS gdpr_anonymized BOOLEAN DEFAULT FALSE;

-- Backfill: Mark existing tickets with GDPR erasure in resolution_notes as anonymized
UPDATE tickets
SET gdpr_anonymized = TRUE
WHERE resolution_notes LIKE '%GDPR erasure%'
  AND gdpr_anonymized = FALSE;

-- Optional: Add index for faster filtering
CREATE INDEX IF NOT EXISTS idx_tickets_gdpr_anonymized ON tickets(gdpr_anonymized);

-- Verify migration
DO $$
DECLARE
    column_exists boolean;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'tickets'
        AND column_name = 'gdpr_anonymized'
    ) INTO column_exists;

    IF column_exists THEN
        RAISE NOTICE 'Migration successful: gdpr_anonymized column added to tickets table';
    ELSE
        RAISE EXCEPTION 'Migration failed: gdpr_anonymized column not found';
    END IF;
END $$;
