import requests
import time
import random

def get_request(u):
    count = 0
    while count < 10:
        try:
            r = requests.get(u)
            break
        except:
            count += 1
            if count > 10:
                print("failed to make request")
                return None
                break
            time.sleep(random.randint(5,10))
    return r
