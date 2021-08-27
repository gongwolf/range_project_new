import os
from datetime import datetime, timedelta


# Hint
# check a file or folder existence: os.path.exists(<path>)
# concat 2 paths together: os.path.join(<path1>, <path2>) use this function instead of
#     "/home/huiying/workplace" + "/" + "range_project_new", why? because it's always safer to do that
# Make use of the datetime and string format functions you learned before


def alert_missing_daily(base_path):
    # base_path: Z:\\logs\\
    # date = datetime.now().date()
    # 2021_07_26_gps.log
    date = datetime.now().date().strftime("%Y_%m_%d")
    path = os.path.join(base_path, date+'_gps.log')
    if not os.path.exists(path):
        print('not exiting')
        alert_via_email()

def alert_via_email():
    gmail_user = 'nmsu.usda.server.alert@gmail.com'
    gmail_password = 'nmsuusda2021'

    sent_from = gmail_user
    to = ['trungle@nmsu.edu', 'hchen@nmsu.edu']
    subject = 'NMSU server is down! Please fix it ASAP!'
    body = 'We currently has no new data coming from today'

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    %s
    """ % (sent_from, ", ".join(to), subject, body)
    send_email(gmail_user, gmail_password, to, subject, body)

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as ex:
        print("Something went wrong….", ex)


if __name__ == '__main__':
    fake_path = 'Z:\\logs'
    alert_missing_daily(fake_path)


