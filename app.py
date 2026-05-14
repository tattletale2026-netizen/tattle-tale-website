from flask import Flask, render_template, jsonify, send_from_directory, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv(override=False)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about-lana')
def about_lana():
    return render_template('about-lana.html')

@app.route('/survey')
def survey():
    return render_template("newform.html")

@app.route('/community-survey')
def community_survey_redirect():
    return redirect(url_for('survey'))

@app.route('/booking')
def booking():
    return render_template("booking.html")

@app.route('/turtle-tales-story')
def tattletale_story():
    return render_template('tattletale-story.html')

@app.route('/workshop-chapters')
def workshop_chapters():
    return render_template('workshop-chapters.html')

@app.route('/event-booking')
def event_booking():
    return render_template('event-booking.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/contact')
def contact():
    return render_template('index.html', _anchor='contact')

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/<path:filename>.js')
def serve_js(filename):
    return send_from_directory('templates', f"{filename}.js")

if __name__ == "__main__":
    app.run(debug=False, port=5000)
