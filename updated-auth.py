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
from flask import Flask, request, session, jsonify, send_from_directory, abort

app = Flask(__name__, static_folder='static', template_folder='templates')
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
    'signup_success': "Account created successfully!",
    'login_success': "Login successful!",
    'logout_success': "You've been logged out",
    'auth_required': "Please login to access this page",
    'password_errors': {
        'min_length': f"Must be at least {PASSWORD_RULES['min_length']} characters",
        'needs_upper': "Requires an uppercase letter",
        'needs_lower': "Requires a lowercase letter",
        'needs_number': "Requires a number",
        'needs_special': f"Requires a special character ({PASSWORD_RULES['allowed_special']})"
    }
}

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
@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(
            os.path.join(app.static_folder, 'images'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    except FileNotFoundError:
        abort(404)  # Silent fail if no favicon exists

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    errors = validate_password(password)
    if errors:
        return jsonify({
            'status': 'error',
            'message': 'Login failed - password invalid',
            'errors': errors,
            'console': f"console.log('%cLOGIN FAILED%c for {email}: {errors}', 'color: red;', '')"
        }), 400
    
    session['user'] = {'email': email}
    return jsonify({
        'status': 'success',
        'message': MESSAGES['login_success'],
        'redirect': '/dashboard',
        'console': f"console.log('%cLOGIN SUCCESS%c for {email}', 'color: green;', '')"
    })

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    errors = validate_password(password)
    if errors:
        return jsonify({
            'status': 'error',
            'message': 'Signup failed - password invalid',
            'errors': errors,
            'console': f"console.log('%cSIGNUP FAILED%c for {email}: {errors}', 'color: red;', '')"
        }), 400
    
    session['user'] = {'email': email}
    return jsonify({
        'status': 'success',
        'message': MESSAGES['signup_success'],
        'redirect': '/dashboard',
        'console': f"console.log('%cNEW ACCOUNT%c created for {email}', 'color: blue;', '')"
    })

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return jsonify({
            'status': 'error',
            'message': MESSAGES['auth_required'],
            'redirect': '/',
            'console': "console.log('%cUNAUTHORIZED%c dashboard access attempt', 'color: orange;', '')"
        }), 401
    
    return jsonify({
        'status': 'success',
        'user': session['user'],
        'console': f"console.log('%cDASHBOARD%c accessed by {session['user']['email']}', 'color: purple;', '')"
    })

@app.route('/logout', methods=['POST'])
def logout():
    user_email = session.get('user', {}).get('email', 'unknown')
    session.clear()
    return jsonify({
        'status': 'success',
        'message': MESSAGES['logout_success'],
        'redirect': '/',
        'console': f"console.log('%cLOGOUT%c by {user_email}', 'color: gray;', '')"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)