from flask import Flask, render_template, url_for
from datetime import datetime
app = Flask(__name__)

podcasts = [
    {
        'id': 1,
        'title': 'Tech Talk Weekly',
        'host': 'Adewale Vanessa',
        'description': 'Weekly discussion in technology',
        'category': 'Technology',
        'episodes': [
            {
                'title': 'The Future of AI',
                'description': 'Exploring the latest advancement in artificial intelligence',
                'duration': '45:00',
                'date_posted': datetime(2023, 9, 1)
            },
            {
                'title': 'Cybersecurity Essentials',
                'description': 'Tips for keeping your digital life secure',
                'duration': '38:30',
                'date_posted': datetime(2023, 9, 8)
            }
        ]
    },
    {
        'id': 2,
        'title': 'Health and Wellness Journey',
        'host': 'Mary Adeoye',
        'description': 'insights into maintaining a healthy lifestyle',
        'category': 'Health',
        'episodes': [
            {
                'title': 'Nutrition Myths Debunked',
                'description': 'Seperating fact from fiction in dietary advice',
                'duration': '52:45',
                'date_posted': datetime(2023, 9, 11)
            },
            {
                'title': 'Mindfulness Meditation Guide',
                'description': 'A beginner\'s guide to mindfulness practices',
                'duration': '40:45',
                'date_posted': datetime(2023, 8, 15)
            }
        ]
    }
]

@app.route("/")
@app.route("/Home")
def home():
    return render_template('home.html', podcasts=podcasts)

@app.route("/About")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)