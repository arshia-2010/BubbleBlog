''' import os
from supabase import create_client
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, flash, session

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_KEY']
)

# --------------------------
# Authentication Routes
# --------------------------

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        # Create user with Supabase Auth
        auth_response = supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        
        # Store additional user data in public.users table
        supabase.table('users').insert({
            'id': auth_response.user.id,
            'email': email
        }).execute()
        
        flash('Account created successfully! Please check your email to verify.', 'success')
        return redirect(url_for('login'))
    
    except Exception as e:
        flash(f'Signup failed: {str(e)}', 'error')
        return redirect(url_for('signup_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        # Store user session
        session['user'] = {
            'id': response.user.id,
            'email': response.user.email,
            'access_token': response.session.access_token
        }
        
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        flash('Invalid email or password', 'error')
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    supabase.auth.sign_out()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# --------------------------
# Protected Routes Example
# --------------------------

@app.route('/create_post', methods=['POST'])
def create_post():
    # Check authentication
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    content = request.form.get('content')
    
    try:
        # Get current user from session
        user_id = session['user']['id']
        
        # Insert post
        supabase.table('posts').insert({
            'user_id': user_id,
            'title': title,
            'content': content
        }).execute()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        flash(f'Error creating post: {str(e)}', 'error')
        return redirect(url_for('create_post_page'))

# --------------------------
# Helper Functions
# --------------------------

def get_current_user():
    """Returns current user from session"""
    return session.get('user')

def is_authenticated():
    """Check if user is logged in"""
    return 'user' in session

if __name__ == '__main__':
    app.run(debug=True)'
    '''