import json
import random
import threading
import uuid
from datetime import datetime
import logging
import time
import threading

from settings import TIME_UNITS

from .order import Order
from enum import Enum


logger = logging.getLogger(__name__)


class TableState(Enum):
    FREE = 1
    WAITING_TO_MAKE_ORDER = 2
    WAITING_ORDER_TO_BE_SERVED = 3


class Table:
    def __init__(self, dinning_hall, id) -> None:
        self.state = TableState.WAITING_TO_MAKE_ORDER
        self.order = None
        self.dinning_hall = dinning_hall
        self.id = id
        self.state_lock = threading.Lock()


    def generate_random_order(self, waiter_id):
        order_id = str(uuid.uuid4())
        num_items = random.randint(1, 4)
        items = random.choices(self.dinning_hall.menu.foods, k=num_items)
        item_ids = [item['id'] for item in items]
       # print(json.dumps(items))
        max_wait = 1.3 * max([food_item['preparation-time'] for food_item in items]) # preparation-time_
        priority = random.randint(1, 5)
        
        self.order = Order(order_id, item_ids, priority, max_wait, self.id, waiter_id)

        logger.info(f"Random order for table {self.id} generated: " + str(self.order.order_id) + ', items: ' + str(item_ids))

        return self.order

    def validate_order(self, distribution): # TODO: expand logic (mapper)
        if not self.order or self.order.order_id != distribution.order_id:
            return False
        
        return True

    def __wait_for_visitors(self):
        time.sleep(random.randint(2, 4) * TIME_UNITS)
        self.state = TableState.WAITING_TO_MAKE_ORDER
        
        logger.info(f"Table {self.id} waiting to be served")


    def free_table(self):
        logger.debug(f"Table {self.id} is Free")

        self.order = None
        self.state = TableState.FREE
        
        threading.Thread(target=self.__wait_for_visitors).start()
        