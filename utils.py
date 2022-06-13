from domain.distribution import Distribution
from typing import Dict


def distribution_request_to_distribution(distribution:Dict):
    order_id = distribution['order_id']
    table_id = distribution['table_id']
    waiter_id = distribution['waiter_id']
    items = distribution['items']
    priority = distribution['priority']
    max_wait = distribution['max_wait']
    pick_up_time = distribution['pick_up_time']
    cooking_time = distribution['cooking_time']
    cooking_details = distribution['cooking_details']

    distribution_obj = Distribution(order_id, table_id, waiter_id, items, priority, max_wait,
                                    pick_up_time, cooking_time, cooking_details)

    return distribution_obj



def get_order_mark(order_total_preparing_time, max_wait):
        if order_total_preparing_time < max_wait:
            return 5
        elif order_total_preparing_time < max_wait * 1.1:
            return 4
        elif order_total_preparing_time < max_wait * 1.2:
            return 3
        elif order_total_preparing_time < max_wait * 1.3:
            return 2
        elif order_total_preparing_time < max_wait * 1.4:
            return 1
        else:
            return 0
