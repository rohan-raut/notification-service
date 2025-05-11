import smtplib
from email.mime.image import MIMEImage
from email.message import EmailMessage
from email.utils import formataddr
from premailer import transform
import importlib.resources

class email_notification:
    
    def __init__(self, host:str, port:int, password:str, sender_email:str, sender_name:str):
        self.host = host
        self.port = port
        self.password = password
        self.sender_email = sender_email
        self.sender_name = sender_name

    def generate_html_template(self, body:str):
        html_body = """\
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
                <style>
                    body {{
                        background-color: #EFEFEF;
                        margin: 0;
                        font-family: Lato, sans-serif;
                        font-size: 14px;
                    }}
                    .container {{
                        width: 650px;
                        height: fit-content;
                        margin: auto;
                    }}
                    .header {{
                        background-color: #2FB0AA;
                        padding: 10px 10px;
                    }}
                    .header img {{
                        width: 150px;
                    }}
                    .content {{
                        background-color: white;
                        padding: 10px;
                    }}
                    p {{
                        margin: 0px;
                        padding: 5px;
                    }}
                </style>
            </head>

            <body>
                <div class="container">
                    <div class="header">
                        <img src="cid:hayame_logo">
                    </div>
                    <div class="content">
                        {body}

                        <div style="border-bottom:1px solid black; width: 90%; margin:40px auto 20px auto;"></div>

                        <div>
                            <div style="text-align:center;">
                                <a href="https://www.facebook.com/hayamedotmy" style="padding:0px 20px; text-decoration:none;">
                                    <img src="cid:facebook_icon" style="width:20px; height:20px">
                                </a>

                                <a href="https://www.instagram.com/hayamesolution" style="padding:0px 20px; text-decoration:none;">
                                    <img src="cid:instagram_icon" style="width:20px; height:20px">
                                </a>

                                <a href="https://wa.me/60124343470" style="padding:0px 20px; text-decoration:none;">
                                    <img src="cid:whatsapp_icon" style="width:20px; height:20px">
                                </a>
                            </div>
                            <div style="padding:5px 0px; font-size:12px; text-align:center;">
                                <p>Hayame Solutions, Shah Alam, Selangor Darul Ehsan, 40470</p>
                            </div>
                        </div>
                    </div>
                </div>
            </body>

            </html>
        """.format(body=body)

        html_body = transform(html_body)

        return html_body
    
    def open_connection(self):
        self.smtp = smtplib.SMTP_SSL(self.host, self.port)
        self.smtp.login(self.sender_email, self.password)

    def close_connection(self):
        self.smtp.close()

    def send_email(self, receiver_email:str, subject:str, body:str, cc=None):
        try:

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = formataddr((self.sender_name, self.sender_email))
            msg['To'] = receiver_email
            
            if(cc is not None):
                msg['cc'] = cc

            html_body = self.generate_html_template(body)
            msg.set_content(html_body, subtype="html")
            msg.make_mixed()

            with importlib.resources.files('notification_service.assets').joinpath('logo.png').open('rb') as fp:
                image = MIMEImage(fp.read())
                image.add_header('Content-ID', '<hayame_logo>')
                msg.attach(image)
            fp.close()

            with importlib.resources.files('notification_service.assets').joinpath('facebook.png').open('rb') as fp:
                image = MIMEImage(fp.read())
                image.add_header('Content-ID', '<facebook_icon>')
                msg.attach(image)
            fp.close()

            with importlib.resources.files('notification_service.assets').joinpath('instagram.png').open('rb') as fp:
                image = MIMEImage(fp.read())
                image.add_header('Content-ID', '<instagram_icon>')
                msg.attach(image)
            fp.close()

            with importlib.resources.files('notification_service.assets').joinpath('whatsapp.png').open('rb') as fp:
                image = MIMEImage(fp.read())
                image.add_header('Content-ID', '<whatsapp_icon>')
                msg.attach(image)
            fp.close()

            self.smtp.send_message(msg)
        
        except Exception as e:
            print("Exception: " + str(e))

