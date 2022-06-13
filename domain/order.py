
class Order:
    def __init__(self, id, items, priority, max_wait, table_id, waiter_id) -> None:
        self.order_id = id
        self.items = items
        self.priority = priority
        self.max_wait = max_wait
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.pick_up_time = None