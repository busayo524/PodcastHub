PodcastHub
PodcastHub is a social media platform for podcast enthusiasts. Users can create accounts, make posts, upload audio files, and interact with other users' content.

### Features

User authentication (register, login, logout)
User profiles with customizable profile pictures
Create, read, update, and delete text posts
Upload, play, update, and delete audio files
View posts and audios from specific users
Responsive design for various screen sizes

### Technology Stack

Backend: Python with Flask framework
Database: SQLite with SQLAlchemy ORM
Frontend: HTML, CSS, JavaScript
Authentication: Flask-Login
Forms: Flask-WTF
File Uploads: Flask-Uploads

### Setup and Installation

1. Clone the repository:
git clone https://github.com/busayo524/podcasthub.git

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
pip install -r requirements.txt

4. Set up the database:
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

6. Run the application:
python run.py

7. Open a web browser and navigate to http://localhost:5000

### Project Structure

podtok/ - Main application package
static/ - Static files (CSS, JS, images)
templates/ - HTML templates
users/ - User-related routes and forms
posts/ - Post-related routes and forms
audios/ - Audio-related routes and forms
main/ - Main routes
errors/ - Error handlers
models.py - Database models
__init__.py - Application factory


### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### License
This project is licensed under the MIT License.


### Conclusion

This README provides a comprehensive overview of your podcast social website project. It includes installation instructions, usage details, and an explanation of the project structure. Feel free to customize it further to suit your project’s specific features and requirements.
