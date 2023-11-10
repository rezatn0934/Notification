from fastapi import HTTPException, status
from config.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
import yagmail


class EmailSender:
    def __init__(self):

        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance variables for this particular object.
        In this case, we are setting up a connection to an SMTP server and storing it in self.server.

        :param self: Represent the instance of the class
        :return: An instance of the class
        :doc-author: Trelent
        """
        self.smtp_server = settings.EMAIL_HOST
        self.smtp_port = settings.EMAIL_PORT
        self.sender_email = settings.EMAIL_HOST_USER
        self.password = settings.EMAIL_HOST_PASSWORD

    def send_email(self, recipient_email, subject, message_body):

        """
        The send_email function takes in a recipient_email, subject, and message.
        It then creates an email text string with the sender's email address as well as the recipient's email address.
        The function then uses smtplib to connect to the SMTP server using TLS encryption on port 587 (the default for Gmail).
        It logs into the account using credentials from a .env file and sends an email with all of these parameters.

        :param self: Represent the instance of the class
        :param recipient_email: Specify the recipient's email address
        :param subject: Set the subject of the email
        :param message_body: Send the body of the email
        :return: A dictionary with the key 'message' and value &quot;email sent successfully&quot;
        :doc-author: Trelent
        """

        try:

            yag_smtp_connection = yagmail.SMTP(
                user=self.sender_email,
                password=self.password,
                host=self.smtp_server)

            yag_smtp_connection.send(recipient_email, subject, message_body)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to send email: " + str(e))


def get_email_sender():
    """
    The get_email_sender function returns an instance of the EmailSender class.
        This is a singleton pattern, which means that only one instance of this class will be created.
        The get_email_sender function can be called multiple times and it will always return the same object.

    :return: An instance of the emailsender class
    :doc-author: Trelent
    """
    return EmailSender()
