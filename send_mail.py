import smtplib
from email.mime.text import MIMEText

def _send_mail(to, subject, text=None, subtype='html'):
    print(f"----Config: {config.mail_service}----")
    if not config.mail_smtp:
        print('no smtp')
        return
    msg = MIMEText(text, _subtype=subtype, _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = config.mail_from
    msg['To'] = to
    try:
        print(f'send mail to {to}')
        if config.mail_ssl or config.mail_starttls or config.mail_port:
            # SSL與STARTTLS皆被設定為強制使用, 衝突時, 優先使用SSL
            tls = False
            if config.mail_ssl == 'True': # 強制使用SSL
                s = smtplib.SMTP_SSL(config.mail_smtp, config.mail_port)
            elif config.mail_starttls == 'True': # 強制使用STARTTLS
                s = smtplib.SMTP(config.mail_smtp, config.mail_port)
                tls = True
            elif config.mail_port == 465: # 透過埠號識別加密協議, 465多為SSL
                s = smtplib.SMTP_SSL(config.mail_smtp, config.mail_port)
            elif config.mail_port == 587: # 透過埠號識別加密協議, 587多為STARTTLS
                s = smtplib.SMTP(config.mail_smtp, config.mail_port)
                tls = True
            s.connect(config.mail_smtp, config.mail_port)
            if tls == True:
                try:
                    smtp_tls_response = s.starttls()
                    print(f'SMTP TLS ==>: {smtp_tls_response}')
                except smtplib.SMTPException as e:
                    print(f"smtp starttls failed: {e}")

        elif config.mail_ssl == 'False' and config.mail_starttls == 'False': # 無安全性傳輸
                s = smtplib.SMTP(config.mail_smtp)
                s.connect(config.mail_smtp, config.mail_port)

        if config.mail_user:
            s.login(config.mail_user, config.mail_password)
        status = s.sendmail(config.mail_from, to, msg.as_string())
        s.close()
        if not status:
            print('寄信成功')
        else:
            print(f'寄信失敗。{status}')
    except Exception as e:
        print(f'send mail error: {e}')
    return

receiver = 'username@example.com' # receiver email

import config_gmail_ssl as config
_send_mail(receiver, f'{config.mail_service} QianDao Test Message', text='Are all settings correct?\r\nSent via send_mail.py')
import config_gmail_starttls as config
_send_mail(receiver, f'{config.mail_service} QianDao Test Message', text='Are all settings correct?\r\nSent via send_mail.py')
import config_outlook as config
_send_mail(receiver, f'{config.mail_service} QianDao Test Message', text='Are all settings correct?\r\nSent via send_mail.py')
import config_yahoo_ssl as config
_send_mail(receiver, f'{config.mail_service} QianDao Test Message', text='Are all settings correct?\r\nSent via send_mail.py')
import config_yahoo_starttls as config
_send_mail(receiver, f'{config.mail_service} QianDao Test Message', text='Are all settings correct?\r\nSent via send_mail.py')