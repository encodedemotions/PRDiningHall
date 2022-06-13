import logging
import time
import requests

logger = logging.getLogger(__name__)

#KITCHEN_BASE_URL = "http://kitchen-container:5000"
KITCHEN_BASE_URL = "http://127.0.0.1:5000"

def send_order_to_kitchen(order):
    logger.debug(f"Sending post request to {KITCHEN_BASE_URL}/order, id = " + str(order.order_id))
    
    r = requests.post(f'{KITCHEN_BASE_URL}/order', json=order.__dict__)
    logger.debug(f"Order items: " + str(order.__dict__['items']))   