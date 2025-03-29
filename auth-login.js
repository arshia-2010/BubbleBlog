import { supabase } from '../supabase/config'

export async function handleLogin(email, password) {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })

    if (error) throw error
    
    return {
      success: true,
      user: data.user
    }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}