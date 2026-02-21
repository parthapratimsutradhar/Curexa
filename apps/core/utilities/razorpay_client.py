import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET)
)