import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
AMOUNT = int(os.getenv("SUBSCRIPTION_AMOUNT", "599900"))
CURRENCY = os.getenv("CURRENCY", "INR")

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

def create_order(user_id: int):
    """
    Create Razorpay order
    """
    order = client.order.create({
        "amount": AMOUNT,
        "currency": CURRENCY,
        "receipt": f"user_{user_id}",
        "notes": {"user_id": str(user_id)}
    })
    return order

def verify_signature(order_id, payment_id, signature):
    """
    Verify payment signature
    """
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
        return True
    except Exception:
        return False
