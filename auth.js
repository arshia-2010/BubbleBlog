supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN') {
      console.log('User signed in:', session.user)
      // Redirect or update UI
    } else if (event === 'SIGNED_OUT') {
      console.log('User signed out')
      // Redirect to login
    }
  })

  //

  async function checkAuth() {
    const { data: { user } } = await supabase.auth.getUser()
    
    if (!user) {
      window.location.href = 'index.html'
    }
  }

//

async function handleLogout() {
    const { error } = await supabase.auth.signOut()
    if (!error) {
      window.location.href = 'index.html'
    }
  }