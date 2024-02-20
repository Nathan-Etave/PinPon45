import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Créer un objet MIMEMultipart
msg = MIMEMultipart()
msg['From'] = 'pinpinpinponponpon45@gmail.com'
msg['To'] = 'louis.lebeaupin@gmail.com'                         
msg['Subject'] = 'Bienvenue sur PinPon45'


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
    <p>Vous avez demandé à réinitialiser votre mot de passe. Voici un lien pour le réinitialiser :</p>
    <p><a href="https://github.com/Nathan-Etave/PinPon45">Reinitialisation</a></p>
    <p>Cordialement,<br>L'équipe de PinPon45</p>
    <img src="https://sdis45.com/wp-content/themes/sdis45/assets/img/logo/logo-loiret.png">
  </body>
</html>
"""

msg.attach(MIMEText(message, 'html'))

mailserver = smtplib.SMTP('smtp.gmail.com', 587)
mailserver.starttls()
mailserver.login('pinpinpinponponpon45@gmail.com', 'leoawgejhmmlhwyy')

mailserver.sendmail('pinpinpinponponpon45@gmail.com', 'louis.lebeaupin@gmail.com', msg.as_string())

mailserver.quit()
