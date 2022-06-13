from datetime import datetime
from typing import Dict, List
import time
import random
import threading
import logging

from domain.distribution import Distribution
from settings import TIME_DELTA, TIME_UNITS

from .table import Table, TableState
import service


logger = logging.getLogger(__name__)


class Waiter:
    def __init__(self, id, dinning_hall) -> None:
        self.serving_tables:Dict[str, Table] = {}
        self.distributions:List[Distribution] = []
        self.distributions_mutex = threading.Lock()
        self.dinning_hall = dinning_hall
        self.id = id
        

    def serve_tables(self, tables):
        while True:
            for table in tables:
                table.state_lock.acquire()
                if table.state == TableState.WAITING_TO_MAKE_ORDER:
                    table.state = TableState.WAITING_ORDER_TO_BE_SERVED
                    table.state_lock.release()
                    self.take_order(table)
                else:
                    table.state_lock.release()

            self.serve_distributions() 
            time.sleep(TIME_DELTA)

    def add_distribution(self, distribution: Distribution):
        self.distributions_mutex.acquire()
        self.distributions.append(distribution)
        self.distributions_mutex.release()

        logger.info(f"Waiter {distribution.waiter_id} notified about received order {distribution.order_id}")


    def serve_distributions(self):
        self.distributions_mutex.acquire()

        for distribution in self.distributions:
            if distribution.table_id not in self.serving_tables:
                logger.debug(f"Invalid distribution ({distribution}), waiter - {self.id}")
                continue
            
            valid_distribution = self.serving_tables[distribution.table_id].validate_order(distribution)

            if not valid_distribution:
                logger.debug(f"Invalid distribution ({distribution}), waiter - {self.id}")
                continue

            self.serving_tables[distribution.table_id].free_table()
            self.dinning_hall.on_order_served(distribution)
            del self.serving_tables[distribution.table_id]

            logger.info(f"Order {distribution.order_id} served by waiter {self.id}")

        self.distributions.clear()
        self.distributions_mutex.release()


    def take_order(self, table: Table):
        order = table.generate_random_order(self.id)
        time.sleep(random.randint(2, 4)  * TIME_UNITS)

        order.pick_up_time = datetime.utcnow().timestamp() 
        logger.debug(f"Order {order.order_id} picked up at {order.pick_up_time}")
        self.serving_tables[table.id] = table
        service.send_order_to_kitchen(order)
