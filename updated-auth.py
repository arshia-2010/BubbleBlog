'''
import os
from flask import Flask, request, redirect, url_for, flash, session, render_template

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')

# --------------------------
# Temporary Authentication Routes (No Supabase)
# --------------------------

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Temporary bypass - just store in session
    session['user'] = {
        'id': 'temp_user_id',
        'email': email
    }
    
    flash('Temporary signup successful!', 'success')
    return redirect(url_for('success_page'))  # Redirect to success page
    # OR use console.log version:
    # return '''
    #    <script>
    #        console.log("Signed up as: {email}");
    #        window.location.href = "/success";
    #    </script>
    # '''.format(email=email)

#
'''
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Temporary bypass - just store in session
    session['user'] = {
        'id': 'temp_user_id',
        'email': email
    }
    
    flash('Temporary login successful!', 'success')
    return redirect(url_for('success_page'))  # Redirect to success page
    # OR use console.log version:
    # return '''
    #    <script>
    #        console.log("Logged in as: {email}");
    #        window.location.href = "/success";
    #    </script>
    # '''.format(email=email)

'''
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# --------------------------
# Sample Pages for Redirection
# --------------------------

@app.route('/success')
def success_page():
    """Sample success page after auth"""
    return render_template('success.html')

@app.route('/home')
def home():
    """Sample home page"""
    return render_template('home.html')

# --------------------------
# Protected Routes Example (Modified)
# --------------------------

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    content = request.form.get('content')
    
    # Temporary message since we're not using Supabase
    flash(f'[DEV] Would create post: "{title}"', 'success')
    return redirect(url_for('success_page'))

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
    app.run(host='0.0.0.0', port=5001, debug=True) '''

#for console.log version

import os
import re
from flask import Flask, request, session, render_template_string, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

# ======================
# CONFIGURATION
# ======================
PASSWORD_RULES = {
    'min_length': 8,
    'needs_upper': True,
    'needs_lower': True,
    'needs_number': True,
    'needs_special': True,
    'allowed_special': '!@#$%^&*'
}

MESSAGES = {
    'welcome': "Welcome to BubbleBlog!",
    'signup_success': "🎉 Account created successfully!",
    'login_success': "🔓 Login successful!",
    'logout_success': "👋 You've been logged out",
    'auth_required': "🔒 Please login to access this page",
    'password_errors': {
        'min_length': f"Password must be at least {PASSWORD_RULES['min_length']} characters",
        'needs_upper': "Must contain at least one uppercase letter",
        'needs_lower': "Must contain at least one lowercase letter",
        'needs_number': "Must contain at least one number",
        'needs_special': f"Must contain one special character ({PASSWORD_RULES['allowed_special']})"
    }
}

# ======================
# UTILITY FUNCTIONS
# ======================
def validate_password(password):
    errors = []
    if len(password) < PASSWORD_RULES['min_length']:
        errors.append(MESSAGES['password_errors']['min_length'])
    if PASSWORD_RULES['needs_upper'] and not re.search(r'[A-Z]', password):
        errors.append(MESSAGES['password_errors']['needs_upper'])
    if PASSWORD_RULES['needs_lower'] and not re.search(r'[a-z]', password):
        errors.append(MESSAGES['password_errors']['needs_lower'])
    if PASSWORD_RULES['needs_number'] and not re.search(r'[0-9]', password):
        errors.append(MESSAGES['password_errors']['needs_number'])
    if PASSWORD_RULES['needs_special'] and not re.search(f'[{PASSWORD_RULES["allowed_special"]}]', password):
        errors.append(MESSAGES['password_errors']['needs_special'])
    return errors

# ======================
# ROUTES
# ======================

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>BubbleBlog</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
                .auth-form { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <h1>{{ welcome_message }}</h1>
            
            {% if 'user' in session %}
                <p>Welcome back, {{ session.user.email }}!</p>
                <a href="/dashboard">Go to Dashboard</a>
                <form action="/logout" method="POST" style="margin-top: 20px;">
                    <button type="submit">Logout</button>
                </form>
            {% else %}
                <div class="auth-form">
                    <h2>Login</h2>
                    <form action="/login" method="POST">
                        <input type="email" name="email" placeholder="Email" required><br><br>
                        <input type="password" name="password" placeholder="Password" required><br><br>
                        <button type="submit">Login</button>
                    </form>
                </div>
                
                <div class="auth-form">
                    <h2>Signup</h2>
                    <form action="/signup" method="POST">
                        <input type="email" name="email" placeholder="Email" required><br><br>
                        <input type="password" name="password" placeholder="Password" required><br>
                        <small>Password requirements: 
                        <ul>
                            {% for rule in password_rules.values() %}
                                <li>{{ rule }}</li>
                            {% endfor %}
                        </ul>
                        </small>
                        <button type="submit">Signup</button>
                    </form>
                </div>
            {% endif %}
        </body>
        </html>
    ''', welcome_message=MESSAGES['welcome'], password_rules=MESSAGES['password_errors'])

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    errors = validate_password(password)
    if errors:
        return render_template_string('''
            <script>
                alert(`Login Failed:\n\n• {{ errors|join('\\n• ') }}`);
                window.location.href = "/";
            </script>
        ''', errors=errors), 400
    
    session['user'] = {'email': email}
    return render_template_string(f'''
        <script>
            alert("{MESSAGES['login_success']}");
            window.location.href = "/dashboard";
        </script>
    ''')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    errors = validate_password(password)
    if errors:
        return render_template_string('''
            <script>
                alert(`Signup Failed:\n\n• {{ errors|join('\\n• ') }}`);
                window.location.href = "/";
            </script>
        ''', errors=errors), 400
    
    session['user'] = {'email': email}
    return render_template_string(f'''
        <script>
            alert("{MESSAGES['signup_success']}");
            window.location.href = "/dashboard";
        </script>
    ''')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template_string(f'''
        <script>
            alert("{MESSAGES['logout_success']}");
            window.location.href = "/";
        </script>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return render_template_string(f'''
            <script>
                alert("{MESSAGES['auth_required']}");
                window.location.href = "/";
            </script>
        ''')
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            </style>
        </head>
        <body>
            <h1>Welcome to your Dashboard, {{ session.user.email }}!</h1>
            <p>This is a protected area.</p>
            <form action="/logout" method="POST">
                <button type="submit">Logout</button>
            </form>
        </body>
        </html>
    ''')

# ======================
# ERROR HANDLERS
# ======================
@app.errorhandler(404)
def page_not_found(e):
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page Not Found</title>
        </head>
        <body>
            <h1>Page Not Found</h1>
            <p>The requested URL was not found on this server.</p>
            <a href="/">Return to Homepage</a>
        </body>
        </html>
    '''), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)