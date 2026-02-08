from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import random
import json
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Dummy user database (in production, use a real database)
users_db = {
    "student@example.com": {
        "password": "password123",
        "name": "John Doe",
        "profile": None
    }
}

# Student profiles storage
student_profiles = {}

# AI Chat logic with enhanced NLP-style responses
def ai_response(question, student_profile=None):
    question = question.lower()
    
    responses = {
        "physics": [
            "Let's break Physics step by step. Think of forces like pushing a shopping cart - the harder you push, the faster it moves!",
            "Physics is all about understanding how things move and interact. Let me explain this concept with a simple analogy...",
            "Great physics question! Let's start with the basics and build up to the complex parts."
        ],
        "math": [
            "Math becomes easier with practice. Let's solve one example together step by step.",
            "Mathematics is like learning a language - once you know the rules, everything makes sense!",
            "Let me break this math concept down into smaller, manageable pieces."
        ],
        "chemistry": [
            "Chemistry is like cooking - you mix ingredients (elements) to create something new!",
            "Think of atoms as tiny building blocks. Let's see how they connect...",
            "Chemistry reactions are like dance partners - they need to match perfectly!"
        ],
        "study plan": [
            "Based on your performance, I recommend focusing more on your weaker subjects while maintaining your strengths.",
            "Let's create a balanced study schedule that includes breaks and revision time.",
            "I'll help you plan your studies based on your upcoming exams and current performance."
        ]
    }
    
    for subject in responses:
        if subject in question:
            return random.choice(responses[subject])
    
    return "That's a great question! Can you tell me which subject this relates to? I'm here to help you understand any concept step by step."

def analyze_student_performance(marks_data):
    """Analyze student performance and identify strengths/weaknesses"""
    if not marks_data:
        return {"strengths": [], "weaknesses": [], "recommendations": []}
    
    avg_score = sum(marks_data.values()) / len(marks_data)
    strengths = [subject for subject, score in marks_data.items() if score >= avg_score + 10]
    weaknesses = [subject for subject, score in marks_data.items() if score < avg_score - 5]
    
    recommendations = []
    for weak_subject in weaknesses:
        recommendations.append(f"Focus more time on {weak_subject} - consider additional practice sessions")
    
    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "average": round(avg_score, 2),
        "recommendations": recommendations
    }

def generate_study_plan(student_profile):
    """Generate personalized study plan based on student profile"""
    if not student_profile:
        return {}
    
    plan = {}
    total_hours = 6  # Default study hours per day
    
    # Allocate more time to weak subjects
    weak_subjects = student_profile.get('analysis', {}).get('weaknesses', [])
    strong_subjects = student_profile.get('analysis', {}).get('strengths', [])
    
    for subject in weak_subjects:
        plan[subject] = "2 hours (Focus area - includes practice and revision)"
    
    for subject in strong_subjects:
        plan[subject] = "1 hour (Maintenance and advanced topics)"
    
    plan["Break Time"] = "1 hour (Distributed throughout the day)"
    plan["Revision"] = "1 hour (Review previous day's topics)"
    
    return plan

@app.route("/")
def home():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template("auth.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email in users_db and users_db[email]['password'] == password:
        session['user_email'] = email
        session['user_name'] = users_db[email]['name']
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials!', 'error')
        return redirect(url_for('home'))

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email in users_db:
        flash('Email already exists!', 'error')
        return redirect(url_for('home'))
    
    users_db[email] = {
        'password': password,
        'name': name,
        'profile': None
    }
    
    session['user_email'] = email
    session['user_name'] = name
    flash('Registration successful!', 'success')
    return redirect(url_for('profile_setup'))

@app.route("/logout")
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route("/dashboard")
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    
    user_email = session['user_email']
    profile = student_profiles.get(user_email, {})
    
    return render_template("dashboard.html", profile=profile, user_name=session['user_name'])

@app.route("/profile-setup")
def profile_setup():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    return render_template("profile_setup.html")

@app.route("/upload-profile", methods=["POST"])
def upload_profile():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    
    user_email = session['user_email']
    
    # Get form data
    subjects = request.form.getlist('subjects')
    marks = {}
    
    for subject in subjects:
        mark_key = f'marks_{subject}'
        if mark_key in request.form:
            marks[subject] = int(request.form[mark_key])
    
    # Handle syllabus file upload
    syllabus_file = None
    if 'syllabus' in request.files:
        file = request.files['syllabus']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_email}_{filename}")
            file.save(file_path)
            syllabus_file = filename
    
    # Analyze performance
    analysis = analyze_student_performance(marks)
    
    # Create student profile
    student_profiles[user_email] = {
        'subjects': subjects,
        'marks': marks,
        'syllabus_file': syllabus_file,
        'analysis': analysis,
        'created_at': datetime.now().isoformat()
    }
    
    flash('Profile created successfully! AI analysis complete.', 'success')
    return redirect(url_for('dashboard'))

@app.route("/study-planner")
def study_planner():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    
    user_email = session['user_email']
    profile = student_profiles.get(user_email, {})
    study_plan = generate_study_plan(profile)
    
    return render_template("study_planner.html", plan=study_plan, profile=profile)

@app.route("/ai-chat")
def ai_chat():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    return render_template("ai_chat.html")

@app.route("/chat-response", methods=["POST"])
def chat_response():
    if 'user_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_email = session['user_email']
    profile = student_profiles.get(user_email, {})
    question = request.json.get('question', '')
    
    response = ai_response(question, profile)
    
    return jsonify({"response": response})

@app.route("/practice")
def practice():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    
    user_email = session['user_email']
    profile = student_profiles.get(user_email, {})
    
    return render_template("practice.html", profile=profile)

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    if 'user_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    subject = request.json.get('subject', '')
    difficulty = request.json.get('difficulty', 'medium')
    
    # Sample quiz questions (in production, use AI to generate based on syllabus)
    sample_questions = {
        "Physics": [
            {
                "question": "What is Newton's first law of motion?",
                "options": ["F=ma", "An object at rest stays at rest", "E=mc²", "v=u+at"],
                "correct": 1,
                "explanation": "Newton's first law states that an object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force."
            }
        ],
        "Math": [
            {
                "question": "What is the derivative of x²?",
                "options": ["x", "2x", "x²", "2x²"],
                "correct": 1,
                "explanation": "The derivative of x² is 2x using the power rule."
            }
        ],
        "Chemistry": [
            {
                "question": "What is the chemical symbol for water?",
                "options": ["H2O", "CO2", "NaCl", "O2"],
                "correct": 0,
                "explanation": "Water is composed of two hydrogen atoms and one oxygen atom, hence H2O."
            }
        ]
    }
    
    questions = sample_questions.get(subject, [])
    return jsonify({"questions": questions})

@app.route("/exam-prep")
def exam_prep():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    
    user_email = session['user_email']
    profile = student_profiles.get(user_email, {})
    
    # Generate revision notes based on weak subjects
    revision_notes = {}
    weak_subjects = profile.get('analysis', {}).get('weaknesses', [])
    
    for subject in weak_subjects:
        revision_notes[subject] = [
            f"Focus on fundamental concepts in {subject}",
            f"Practice previous year questions for {subject}",
            f"Create mind maps for {subject} topics"
        ]
    
    return render_template("exam_prep.html", profile=profile, revision_notes=revision_notes)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
