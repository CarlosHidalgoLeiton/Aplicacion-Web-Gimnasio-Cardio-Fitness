import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración de la cuenta de correo
remitente = 'cardiofitnessgr@gmail.com'
contraseña = 'ifjqdysbyknxpmuf'  

def sendEmail(documentId, destinyEmail, token):
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinyEmail
    mensaje['Subject'] = 'Restaurar Contraseña'

    contenido_html = f"""
        <html>

        <body>
            <div style="display: grid; grid-template-rows: 50px 1fr; justify-content: center; align-items: center; background-color: #1B2E40; border-radius: 7px; color: white; margin-bottom: 20px;">
                <h2 style="text-align: center;">Cardio Fitness Gym</h2>
                <h4 style="text-align: center;">Solicitud cambio de contraseña</h1>
            </div>

            <table role="presentation" style="width: 100%; height: 100%; border: 0; cellpadding: 0; cellspacing: 0;">
                <tr>
                    <td style="text-align: center; vertical-align: middle;">
                        <span style="font-size: 15px; text-align: center;">Para el cambio de contraseña debe de ingresar al siguiente enlace: </span>
                    </td>
                </tr>
            </table>

            <table role="presentation" style="width: 100%; height: 100%; border: 0; cellpadding: 0; cellspacing: 0;">
                <tr>
                    <td style="text-align: center; vertical-align: middle;">
                        <a style="text-align: center; text-decoration: none; background-color: #f21D2F; color: white; border-radius: 10px; width: 170px; padding: 8px; display: inline-block;" href="http://127.0.0.1:5000/changePassword/{documentId}/{token}">
                            <b>Cambiar contraseña</b>
                        </a>
                    </td>
                </tr>
            </table>
            
            <div style=" background-color: #1B2E40; border-radius: 10px; color: white; margin-bottom: 20px;">
                <h4 style="text-align: center; padding: 20px;" >© Cardio Fitness Gym 2024</h4>
            </div>
        </body>

        </html>
        """

    mensaje.attach(MIMEText(contenido_html, 'html'))

    # Conexión al servidor SMTP de Gmail (puedes usar otro si lo prefieres)
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()  # Iniciar la conexión segura
        servidor.login(remitente, contraseña)  # Autenticación

        # Enviar el correo
        texto = mensaje.as_string()
        servidor.sendmail(remitente, destinyEmail, texto)
        return True

    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

    finally:
        servidor.quit()  # Cerrar la conexión al servidor
