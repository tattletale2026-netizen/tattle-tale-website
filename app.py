from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_mail import Mail, Message
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=False)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Recipient for feedback emails
MAIL_TO = os.environ.get('MAIL_TO', os.environ.get('MAIL_DEFAULT_SENDER'))

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about-lana')
def about_lana():
    return render_template('about-lana.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        d1 = request.form.get("age_range")
        d2 = request.form.get("sheffield_area")
        d3 = request.form.get("heard_about")

        q1_1 = request.form.get("q1_1")
        q1_2 = request.form.get("q1_2")
        q1_3 = request.form.get("q1_3")
        q1_4 = request.form.get("q1_4")

        q2_1 = request.form.get("q2_1")
        q2_2 = request.form.get("q2_2")
        q2_3 = request.form.get("q2_3")
        q2_4 = request.form.get("q2_4")

        q3a = request.form.get("q3a")
        q3b = request.form.get("q3b")
        q3c = request.form.get("q3c")
        q3d = request.form.get("q3d")

        q4 = request.form.get("q4")
        q5 = request.form.get("q5")

        q6 = request.form.getlist("q6")
        q7 = request.form.getlist("q7")

        q8 = request.form.get("q8")
        q9 = request.form.get("q9")
        q10 = request.form.get("q10")
        q11 = request.form.get("q11")
        q12 = request.form.get("q12")
        
        body_content = "New Community Survey Response (Form)\n\n"
        body_content += f"D1: {d1}\nD2: {d2}\nD3: {d3}\n\n"
        body_content += f"Q1: {q1_1}, {q1_2}, {q1_3}, {q1_4}\n"
        body_content += f"Q2: {q2_1}, {q2_2}, {q2_3}, {q2_4}\n\n"
        body_content += f"Q3a: {q3a}\nQ3b: {q3b}\nQ3c: {q3c}\nQ3d: {q3d}\n"
        body_content += f"Q4: {q4}\nQ5: {q5}\n"
        body_content += f"Q6: {', '.join(q6) if q6 else ''}\n"
        body_content += f"Q7: {', '.join(q7) if q7 else ''}\n\n"
        body_content += f"Q8: {q8}\nQ9: {q9}\nQ10: {q10}\nQ11: {q11}\nQ12: {q12}\n"
        
        msg = Message(
            subject='New Community Survey Response - Form',
            recipients=[MAIL_TO]
        )
        msg.body = body_content
        try:
            if app.config['MAIL_USERNAME']:
                mail.send(msg)
                print("[Survey Form] Sent OK")
        except Exception as e:
            print(f"Mail error: {repr(e)}")

        return redirect(url_for("survey", success=1))

    return render_template("newform.html")

@app.route('/community-survey')
def community_survey_redirect():
    return redirect(url_for('survey'))

def get_booking_count():
    json_path = os.path.join(app.root_path, 'templates', 'bookings.json')
    if not os.path.exists(json_path):
        with open(json_path, 'w') as f:
            json.dump({"count": 0}, f)
        return 0
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get("count", 0)
    except:
        return 0

def increment_booking():
    count = get_booking_count()
    json_path = os.path.join(app.root_path, 'templates', 'bookings.json')
    with open(json_path, 'w') as f:
        json.dump({"count": count + 1}, f)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    seats_taken = get_booking_count()
    closed = seats_taken >= 20
    
    if request.method == 'POST':
        if closed:
            return render_template("booking.html", closed=True)
            
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        
        if not first_name or not last_name or not email or not phone:
            return render_template("booking.html", closed=closed, error="All fields are required.")
            
        increment_booking()
        
        # Admin Email
        admin_msg = Message(
            subject='New Workshop One Booking',
            recipients=[MAIL_TO]
        )
        admin_msg.body = f"New Workshop One Booking\n\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone Number: {phone}\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # User Confirmation Email
        user_msg = Message(
            subject='Your Seat is Confirmed – Workshop One',
            recipients=[email]
        )
        user_msg.html = f"""
        <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; background-color: #f9fbfb; padding: 40px; border-radius: 8px; border: 1px solid #e2e8e9;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #174f63; font-size: 24px; font-weight: normal; margin: 0;">Tatle tale</h1>
                <p style="color: #2a8a6e; font-size: 14px; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px;">Workshop One</p>
            </div>
            <p style="font-size: 16px; line-height: 1.6;">Dear {first_name},</p>
            <p style="font-size: 16px; line-height: 1.6;">Thank you for booking your place at Workshop One.</p>
            <p style="font-size: 16px; line-height: 1.6; font-weight: bold; color: #174f63;">Your seat has been successfully confirmed.</p>
            <p style="font-size: 16px; line-height: 1.6;">Our team will contact you soon with additional details.</p>
            
            <div style="background-color: #fff; padding: 20px; border-radius: 6px; margin: 30px 0; border-left: 4px solid #2a8a6e;">
                <p style="margin: 0 0 10px 0; font-weight: bold; color: #174f63;">Important Reminder:</p>
                <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                    <li>This workshop is <strong>strictly 18+</strong>.</li>
                    <li>You must bring a <strong>valid physical photo ID</strong>.</li>
                    <li>No entry without ID.</li>
                </ul>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>Venue Information:</strong><br>
                <a href="https://maps.app.goo.gl/jm2akVWdZtZcy5XW7" style="color: #2a8a6e; text-decoration: none; font-weight: bold;">Workshop Venue</a>
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; margin-top: 30px;">
                If you have any questions, feel free to reply to this email.<br>
                We look forward to welcoming you!
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; margin-top: 30px; color: #666;">
                Warmly,<br>
                The Tatle tale Team
            </p>
        </div>
        """
        
        try:
            if app.config['MAIL_USERNAME']:
                mail.send(admin_msg)
                mail.send(user_msg)
                print(f"[Booking] Sent OK to {email} and admin")
        except Exception as e:
            print(f"Mail error: {repr(e)}")
            
        return redirect(url_for("booking", success=1))
        
    return render_template("booking.html", closed=closed)


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

@app.route('/api/feedback', methods=['POST'])
def handle_feedback():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    if not data:
        return jsonify({'success': False, 'message': 'Invalid request data.'}), 400

    # Honeypot spam check
    if data.get('honeypot'):
        return jsonify({'success': False, 'message': 'Spam detected.'}), 400

    # Validate required fields
    rating = data.get('rating')
    help_status = data.get('helpStatus')
    email = data.get('email')
    message = data.get('message', '')

    if not email or '@' not in email:
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    if not rating or not help_status:
        return jsonify({'success': False, 'message': 'Missing rating or help status.'}), 400

    # Build email
    submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    msg = Message(
        subject='New Homepage Feedback - Tatle tale',
        recipients=[MAIL_TO],
        reply_to=email
    )
    msg.body = (
        f"Rating: {rating}\n"
        f"Help Status: {help_status}\n"
        f"User Email: {email}\n"
        f"Message:\n{message}\n\n"
        f"Submitted At: {submitted_at}\n"
    )

    try:
        if app.config['MAIL_USERNAME']:
            mail.send(msg)
            print(f"[Feedback] Sent OK — rating={rating}, email={email}, at={submitted_at}")
        return jsonify({'success': True, 'message': 'Feedback sent successfully.'})
    except Exception as e:
        print(f"Mail error: {repr(e)}")
        return jsonify({'success': False, 'message': 'Failed to send feedback. Please try again later.'}), 500


@app.route('/api/contact', methods=['POST'])
def handle_contact():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
        
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    msg = Message(f"New Contact Form Submission from {name}",
                  recipients=[MAIL_TO])
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    
    try:
        if app.config['MAIL_USERNAME']:
            mail.send(msg)
            print(f"[Contact] Sent OK from {email}")
        return "Success"
    except Exception as e:
        print(f"Mail error: {repr(e)}")
        return "Error", 500

@app.route('/<path:filename>.js')
def serve_js(filename):
    return send_from_directory('templates', f"{filename}.js")

if __name__ == "__main__":
    app.run(debug=False, port=5000)
