from flask import Flask, request
from flask.json import jsonify
import requests
import threading
import logging
import utils
import time

from domain.dinning_hall import DinningHall
from service import KITCHEN_BASE_URL


logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(name)s:%(message)s', datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)


app = Flask(__name__)
dinning_hall = None

@app.route('/distribution', methods=['POST'])
def receive_order():
    distribution = request.json
    distribution_obj = utils.distribution_request_to_distribution(request.json)

    logger.info(f"Order {distribution_obj.order_id} received from kitchen. Cooking time = {distribution_obj.cooking_time}. Notifying the waiter...")
    dinning_hall.notify_order_received(distribution_obj)

    return jsonify(distribution)


if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=5001, host="0.0.0.0",)).start()

    time.sleep(5)
    dinning_hall = DinningHall()
    dinning_hall.run_simulation()