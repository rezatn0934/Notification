from fastapi import APIRouter, Depends, Request
from db.redis_db import get_redis_client
from schemas.user import User
from services.celery_services import send_mail_task
from utils.user import generate_otp

api_router = APIRouter()


@api_router.post('/send_register_mail')
async def send_register_mail(email: User, request: Request, redis_db=Depends(get_redis_client)):
    """
    The send_register_mail function sends a registration confirmation email to the user.

    :param email: EmailStr: Specify the email address of the user
    :param redis_db: Get the redis client
    :return: A coroutine that returns none
    :doc-author: Trelent
    """
    otp_code = generate_otp()
    email = email.email
    subject = "Registration Confirmation"
    message = f"Hello {email},\n\n" \
              f"Thank you for registering. Your OTP code is: {otp_code}.\n\n" \
              "Please use this code to complete the registration process. " \
              "Note: This token will expire in 5 minutes.\n\n" \
              "Regards,\nRSS-Feed-Aggregator Team"

    correlation_id = request.headers.get("correlation-id")
    send_mail_task.delay(email, subject, message, correlation_id)
    await redis_db.set(f"registration_otp:{otp_code}", email, ex=60 * 5)

    return {"message": f"Registration confirmation email has been sent to {email}"}


@api_router.post('/send_reset_password_mail')
async def send_reset_password_mail(email: User, request: Request, redis_db=Depends(get_redis_client)):
    """
    The send_reset_password_mail function sends a password reset email to the user.

    :param email: EmailStr: Specify the email address of the user who requested to reset their password
    :param redis_db: Get the redis client
    :return: None, so the return type is none
    :doc-author: Trelent
    """

    reset_token = generate_otp()
    email = email.email

    subject = "Password Reset Request"
    message = f"Hello,\n\n" \
              f"We received a request to reset the password associated with this email address. " \
              f"If you made this request, " \
              f"please use the following token in the application to reset your password: {reset_token}\n\n" \
              "Note: This token will expire in 5 minutes.\n\n" \
              "If you didn't request this, you can safely ignore this email.\n\n" \
              "Regards,\nRSS-Feed-Aggregator Team"

    correlation_id = request.headers.get("correlation-id")
    send_mail_task.delay(email, subject, message, correlation_id)
    await redis_db.set(f"password_reset_token:{reset_token}", email, ex=60 * 5)

    return {"message": f"Password reset email has been sent to {email}"}
