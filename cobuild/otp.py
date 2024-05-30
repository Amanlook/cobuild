import base64
from datetime import datetime
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from urllib.parse import urlencode
from django.conf import settings
from threading import Thread
import pyotp


class OtpMixin:
    default_otp_length = 6
    default_otp_interval = 60 * 15 # 15 minutes
    class generateKey:
        @staticmethod
        def returnValue(contact):
            return str(contact) + str(datetime.now().date()) + "sadsad$%34^y6645433t5@t5754#$%e"

    def generate_otp(self, contact, counter):
        keygen = self.generateKey()
        key = base64.b32encode(keygen.returnValue(
            contact).encode())
        OTP = pyotp.HOTP(key, digits=self.default_otp_length)
        return OTP.at(counter)
    


    def generate_totp(self,contact):
        keygen = self.generateKey()
        key = base64.b32encode(
            keygen.returnValue(contact).encode())
        OTP = pyotp.TOTP(
            key,digits=self.default_otp_length,
            interval=self.default_otp_interval,
            name=contact, issuer='cobuild')
        return OTP.now()

    def verify_totp(self,contact,otp):
        if str(otp) == settings.BYPASS_OTP:
            return True
        if not isinstance(otp,str):
            otp = str(otp)
        keygen = self.generateKey()
        key = base64.b32encode(
            keygen.returnValue(contact).encode())
        OTP = pyotp.TOTP(
            key,
            digits=self.default_otp_length,
            interval=self.default_otp_interval,
            name=contact, issuer='socail_community')
        return OTP.verify(otp,valid_window=3)

        
        
    def verify_otp(self, contact, counter, otp):
        try:
            if str(otp) == settings.BYPASS_OTP:
                return True
            keygen = self.generateKey()
            key = base64.b32encode(keygen.returnValue(
                contact).encode())  # Generating Key
            OTP = pyotp.HOTP(key, digits=self.default_otp_length)        
            return OTP.verify(otp, counter)
        except:
            return False