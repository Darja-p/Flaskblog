from flask import abort, url_for, current_app
import smtplib
from flask_mail import Message
from functools import wraps
from flask_login import current_user
from application import mail




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender="noreply@blogdemo.com", recipients = [user.email])
    msg.body = f'''To reset your password please visit the following link: 
{url_for('reset_token', token=token)}

If you did not made this request, please ignore this email'''
    mail.send(msg)



def sent_contact_email(user_data):
    MAIL_PASSWORD=current_app.config["MAIL_PASSWORD"]
    MAIL_USERNAME=current_app.config["MAIL_USERNAME"]
    print(MAIL_USERNAME, MAIL_PASSWORD)

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(password=MAIL_PASSWORD, user=MAIL_USERNAME)
        connection.sendmail(from_addr=MAIL_USERNAME, to_addrs=MAIL_USERNAME,
                                msg=f"Someone wrote you \n\n Username {user_data[0]}, email {user_data[1]}, phone number {user_data[2]} send you this message: {user_data[3]}")


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id exists(user is loged in) is equal 1 then return route function
        try:
            if current_user.id == 1:
                return f(*args, **kwargs)
        #Otherwise abort with 403 error
            return abort(403)
        except AttributeError:
            return abort (403)
    return decorated_function