import { supabase } from '../supabase/config'

export async function handleSignup(email, password, username) {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          username
        }
      }
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