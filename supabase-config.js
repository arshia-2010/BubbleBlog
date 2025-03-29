import { createClient } from '@supabase/supabase-js'

const supabaseUrl = https://jgbvyhawtdebkpafkrvd.supabase.co
const supabaseAnonKey = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpnYnZ5aGF3dGRlYmtwYWZrcnZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNDE3MDYsImV4cCI6MjA1ODgxNzcwNn0.q70S0NVtT47N5BSBvHe3YouA_2oDzJyg4qPRUDJXR2M'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)