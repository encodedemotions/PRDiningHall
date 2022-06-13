from datetime import datetime
import threading
import logging
from typing import Dict

from domain.distribution import Distribution
from utils import get_order_mark
from .menu import RestaurantMenu
from .table import Table
from .waiter import Waiter
import settings

logger = logging.getLogger(__name__)


class DinningHall:
    
    def __init__(self, num_tables = settings.NUM_TABLES, num_waiters=settings.NUM_WAITERS) -> None:
        self.tables = [Table(dinning_hall=self, id=i) for i in range(num_tables)] # todo: convert to dict
        self.waiters = {i:Waiter(i, self) for i in range(num_waiters)}
        self.menu = RestaurantMenu()

        self.prepared_orders:Dict[str, Distribution] = {}
        self.prepares_orders_semaphore = threading.BoundedSemaphore(value=1)
        self.marks = []
    
    def run_simulation(self):
        logger.info("Starting dinning hall simulation...")
        for waiter_id, waiter in self.waiters.items():
            threading.Thread(target=waiter.serve_tables, args=(self.tables, )).start() # todo: target withou arguments
            

    def notify_order_received(self, distribution: Distribution):
        waiter = self.waiters[distribution.waiter_id]

        waiter.add_distribution(distribution)

    
    def on_order_served(self, distribution: Distribution):
        order_total_preparing_time = (datetime.utcnow().timestamp() -  distribution.pick_up_time)

        mark = get_order_mark(order_total_preparing_time, distribution.max_wait * settings.TIME_UNITS)
        self.marks.append(mark)

        logger.info(f"{distribution} mark = {mark}, order_total_preparing_time = {order_total_preparing_time}, max_wait = {distribution.max_wait * settings.TIME_UNITS}, priority={distribution.priority}")
        logger.debug(datetime.utcnow().timestamp())
        logger.debug(distribution.pick_up_time)

        return mark
