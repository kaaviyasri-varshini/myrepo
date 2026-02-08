# Technology Stack & Development Guidelines

## Tech Stack

### Backend
- **Framework**: Flask (Python web framework)
- **Language**: Python 3.x
- **Session Management**: Flask sessions with secret key
- **File Handling**: Werkzeug utilities for secure file uploads
- **Data Storage**: In-memory dictionaries (development setup)

### Frontend
- **Template Engine**: Jinja2 (Flask's default)
- **Styling**: Custom CSS with CSS variables for theming
- **JavaScript**: Vanilla JS for interactivity
- **Icons**: Font Awesome 6.0.0
- **Responsive Design**: CSS Grid and Flexbox

### File Structure
- `app.py`: Main Flask application
- `templates/`: Jinja2 HTML templates
- `static/`: CSS, JS, and static assets
- `uploads/`: User-uploaded files (syllabus documents)

## Development Commands

### Running the Application
```bash
python app.py
```
The app runs in debug mode by default on `http://localhost:5000`

### Development Setup
```bash
# Install Flask (if not already installed)
pip install flask

# Run the application
python app.py
```

## Code Conventions

### Python/Flask
- Use Flask's built-in session management
- Store user data in global dictionaries (development pattern)
- Follow Flask route naming conventions (`snake_case`)
- Use `render_template()` for all HTML responses
- Use `jsonify()` for API responses
- Handle file uploads with `secure_filename()`

### Templates
- Extend `base.html` for all pages
- Use Jinja2 template inheritance
- Follow consistent block naming: `title`, `content`
- Use Flask's `url_for()` for all internal links
- Handle flash messages in base template

### Styling
- Use CSS custom properties (variables) for theming
- Support both light and dark themes via `data-theme` attribute
- Follow BEM-like naming for CSS classes
- Use CSS Grid for layouts, Flexbox for components
- Maintain responsive design with mobile-first approach

### JavaScript
- Use vanilla JavaScript (no frameworks)
- Follow async/await pattern for API calls
- Handle errors gracefully with try/catch
- Use `fetch()` for AJAX requests
- Store theme preference in localStorage

## Architecture Patterns

### Session-Based Authentication
- Store user email and name in Flask session
- Check session before accessing protected routes
- Clear session on logout

### In-Memory Data Storage
- `users_db`: User credentials and basic info
- `student_profiles`: Detailed academic profiles and analytics
- Note: This is development setup - production should use proper database

### AI Response System
- Simple keyword-based response matching
- Extensible pattern for adding new subjects/responses
- Returns contextual responses based on student profile

### File Upload Pattern
- Use `secure_filename()` for safety
- Store files in `uploads/` directory
- Prefix filenames with user email for organization