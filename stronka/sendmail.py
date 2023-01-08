import smtplib
from email.mime.text import MIMEText

def send_verification_email(to, link):
    sender = 'zabawkowe.okazje@gmail.com'
    password = 'jgbuxqxdnhivowdw'
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(sender, password)

    message = """\
    Kliknij w poniższy link aby aktywować konto Zabawkowe Okazje:
    <a href="{}">{}</a>
    """.format(link, link)
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Weryfikacja e-mail Zabawkowe Okazje'
    msg['From'] = sender
    msg['To'] = to

    smtpserver.sendmail(sender, to, msg.as_string())
    print('Verification email sent!')
    smtpserver.close()
