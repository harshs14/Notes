from django.core.mail import send_mail
from server.settings import EMAIL_HOST_USER

def sendMail(user):
    try:
        otp = Otp.objects.filter(userId = user)
    except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
        otp = None
    if otp is not None:
        otp.delete()

    otp = random.randint(1000,10000)
    otpObj = Otp.objects.create(userId = user, otp = otp)

    subject = 'NOTES VERIFICATION'
    message = 'YOUR OTP : ' + str(otpObj.otp)
    to_mail = [user.email]
    from_mail = EMAIL_HOST_USER
    send_mail(subject, message, from_mail, to_mail, fail_silently=False)