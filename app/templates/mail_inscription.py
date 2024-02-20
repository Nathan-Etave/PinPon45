import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Créer un objet MIMEMultipart
msg = MIMEMultipart()
msg['From'] = 'pinpinpinponponpon45@gmail.com'
msg['To'] = 'louis.lebeaupin@gmail.com'                         
msg['Subject'] = 'Mot de passe oublié'


message = """
<html>
    <head>
        <style>
            img {
                width: 100px;
            }

        </style>
    </head>
    <body>
        <p>Bonjour,</p>
        <p>L'équipe de PinPon45 vous souhaite la bienvenue !</p>
        <p>Vous pouvez dès à présent vous connecter à votre compte.</p>
        <p>connectez-vous à l'aide du mot de passe suivant : <strong>1234</strong></p>
        <p>Cordialement,<br>L'équipe de PinPon45</p>
        <img src="https://sdis45.com/wp-content/themes/sdis45/assets/img/logo/logo-loiret.png">
"""

msg.attach(MIMEText(message, 'html'))

mailserver = smtplib.SMTP('smtp.gmail.com', 587)
mailserver.starttls()
mailserver.login('pinpinpinponponpon45@gmail.com', 'leoawgejhmmlhwyy')

mailserver.sendmail('pinpinpinponponpon45@gmail.com', 'louis.lebeaupin@gmail.com', msg.as_string())

mailserver.quit()
