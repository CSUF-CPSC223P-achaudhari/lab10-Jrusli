import json
import threading
import time

def bot_clerk(items):
    cart = []
    lock = threading.Lock()

    inventory = inventory_('inventory.dat')

    robot_fetchers = [[] for _ in range(3)]

    for i, item in enumerate(items):
        robot_fetchers[i % 3].append(item)

    threads = []
    for fetcher_items in robot_fetchers:
        thread = threading.Thread(target=bot_fetcher, args=(fetcher_items, cart, lock, inventory))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return cart

def bot_fetcher(items, cart, lock, inventory):
    for item in items:
        description, seconds = inventory[item]
        time.sleep(seconds)
        with lock:
            cart.append([item, description])
            
def inventory_(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)