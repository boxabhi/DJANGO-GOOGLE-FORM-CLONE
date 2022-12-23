import random
import string

def generate_random_string(N=20)->str:
    token = ''.join(random.choice(string.ascii_letters + string.digits)  for x in range(N)) 
    return token