# Project Structure & Organization

## Directory Layout

```
AI-Study-Buddy/
├── .kiro/                    # Kiro IDE configuration
│   └── steering/            # AI assistant guidance files
├── .vscode/                 # VS Code configuration
├── app.py                   # Main Flask application
├── static/                  # Static assets
│   └── style.css           # Additional CSS styles and animations
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template with navigation and theming
│   ├── auth.html          # Login/registration page
│   ├── dashboard.html     # Main user dashboard
│   ├── profile_setup.html # Student profile creation
│   ├── study_planner.html # Personalized study plans
│   ├── ai_chat.html       # AI tutor chat interface
│   ├── practice.html      # Quiz and practice exercises
│   └── exam_prep.html     # Exam preparation materials
└── uploads/               # User-uploaded files (syllabus, etc.)
```

## File Organization Principles

### Templates Structure
- **base.html**: Contains common layout, navigation, theming, and JavaScript utilities
- **Feature templates**: Each major feature has its own template extending base.html
- **Consistent naming**: Use descriptive names matching Flask route functions

### Static Assets
- **style.css**: Additional styles for animations, responsive design, and enhanced UI
- **Inline styles**: Complex component styles are kept in templates for better maintainability
- **External CDN**: Font Awesome icons loaded from CDN

### Application Structure
- **Single file app**: All Flask routes and logic in `app.py` (suitable for development)
- **Global data stores**: In-memory dictionaries for users and profiles
- **Modular functions**: Separate functions for AI responses, analytics, and study planning

## Component Organization

### Navigation Structure
```
Home (/) → Auth → Dashboard → Features
                     ├── Profile Setup
                     ├── Study Planner  
                     ├── AI Chat
                     ├── Practice
                     └── Exam Prep
```

### Data Flow
1. **Authentication**: Login/Register → Session creation
2. **Profile Setup**: Subject selection → Performance data → AI analysis
3. **Dashboard**: Performance overview → Quick actions
4. **Features**: Personalized content based on profile data

### Template Inheritance
```
base.html (layout, navigation, theming)
├── auth.html (login/register forms)
├── dashboard.html (performance overview)
├── profile_setup.html (academic data collection)
├── study_planner.html (AI-generated schedules)
├── ai_chat.html (conversational interface)
├── practice.html (quiz generation)
└── exam_prep.html (revision materials)
```

## Naming Conventions

### Files & Directories
- Use `snake_case` for Python files and functions
- Use `kebab-case` for HTML templates and CSS classes
- Use descriptive names that match functionality

### Flask Routes
- Route functions match template names (e.g., `study_planner()` → `study_planner.html`)
- Use RESTful patterns where applicable
- Group related functionality (auth routes, feature routes, API routes)

### CSS & JavaScript
- Use CSS custom properties for consistent theming
- Prefix component-specific styles with feature name
- Keep JavaScript functions focused and well-named

## Development Workflow

### Adding New Features
1. Create route function in `app.py`
2. Create corresponding template in `templates/`
3. Add navigation link in `base.html` if needed
4. Update any related data structures
5. Test authentication and session handling

### Styling Guidelines
- Extend existing CSS variables for consistency
- Use the established grid system for layouts
- Maintain responsive design patterns
- Test both light and dark themes

### Data Management
- Add new data fields to existing dictionaries
- Maintain backward compatibility with existing profiles
- Consider data validation and error handling
- Document any new data structures