import json
import threading
import time

def bot_clerk(items):
    cart = []
    lock = threading.Lock()

    with open('inventory.dat', 'r') as file:
        inventory = json.load(file)

    fetchers = [[] for _ in range(3)]

    for i, item in enumerate(items):
        fetchers[i % 3].append(item)

    threads = []
    for fetcher_items in fetchers:
        thread = threading.Thread(target=bot_fetcher, args=(fetcher_items, cart, lock, inventory))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return cart

def bot_fetcher(items, cart, lock, inventory):
    for item in items:
        description, sec = inventory[item]
        time.sleep(sec)
        with lock:
            cart.append([item, description])
