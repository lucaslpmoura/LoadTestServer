from concurrent.futures import ThreadPoolExecutor
import requests
import time

addr = "162.35.172.66"
port = "8080"
URL = f"http://{addr}:{port}/"


req_rate = 1 # req/s
req_interval = 1 / req_rate # s/req (intervalo entre req.)

T = 60 # tempo em segundos do teste
N = req_rate * T # numero de requsições totais

def request():
    try:
        requests.get(URL, timeout=10)
    except requests.RequestException:
        pass


print ("Starting test...")
with ThreadPoolExecutor(max_workers=100) as executor:
    next = time.perf_counter()

    while True:
        executor.submit(request)
        next += req_interval

        '''
        Caso a resposta venha antes do intervalo, dorme a thread.
        Caso contrário, continua.
        '''
        sleep = next - time.perf_counter()
        if sleep > 0:
            time.sleep(sleep)
        else:
            next = time.perf_counter()

        N = N - 1
        if(N % 10 == 0):
            print(f"{N} request remaining.")

        if N <= 0:
            break

print(f"Finished test after {N} requests.")