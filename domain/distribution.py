
class Distribution:
    def __init__(self, order_id, table_id, waiter_id, items, priority, max_wait, pick_up_time, cooking_time, cooking_details):
        self.order_id = order_id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.items = items
        self.priority = priority
        self.max_wait = max_wait
        self.pick_up_time = pick_up_time
        self.cooking_time = cooking_time
        self.cooking_details = cooking_details

    def __str__(self) -> str:
        return f"""`Distribution: order_id={self.order_id}, table_od={self.table_id}, waiter_id={self.waiter_id}`"""
