import logging
import logging.handlers
import os

from source import settings


class TlsSMTPHandler(logging.handlers.SMTPHandler):
    """
    loggingをGmailで送信させるために、SMTPHandlerをオーバーライドしてTLSに対応させる。
    https://gist.github.com/Agasper/8ef727892f7d8d63e0ac
    """
    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            import string  # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr,
                ",".join(self.toaddrs),
                self.getSubject(record),
                formatdate(), msg)
            if self.username:
                smtp.ehlo()  # for tls add this line
                smtp.starttls()  # for tls add this line
                smtp.ehlo()  # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def set_logger(module_name, log_path):
    """共通のロガーを定義する

    Args:
        module_name (str)
        log_path (str): 書き込みたいログファイルのパス

    Returns:
        logger
    """
    logger = logging.getLogger(module_name)

    streamHandler = logging.StreamHandler()
    fileHandler = logging.FileHandler(log_path)
    emailHandler = TlsSMTPHandler(
        mailhost=("smtp.gmail.com", 587),
        fromaddr=os.getenv("from_gmail"),
        toaddrs=[os.getenv("to_email")],
        subject="{Urgent} CHECK LOGS",
        credentials=(os.getenv("from_gmail"), os.getenv("google_app_pw"))
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] (%(filename)s | %(funcName)s | %(lineno)s) %(message)s")

    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    emailHandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.INFO)
    fileHandler.setLevel(logging.DEBUG)
    emailHandler.setLevel(logging.WARNING)

    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    logger.addHandler(emailHandler)

    return logger
