import json
import time
from multiprocessing import Pool
import requests


def load_para():
    with open("config.json", 'r') as f:
        return json.load(f)


def send_request(img_url, end_point, thread_num):
    body = {
        "img_url": img_url
    }
    start_time = time.time()
    response = requests.post(end_point, data=json.dumps(body))
    end_time = time.time()
    print([thread_num, start_time, end_time, (end_time - start_time), response.text])


def run():
    config = load_para()
    end_point = config['ecs_endpoint'] if config["target"] == "ecs" else config['lambda_endpoint']
    print(end_point)
    data = [[config["img_url"], end_point, i] for i in range(config["request_number"])]
    with Pool(processes=config["request_number"]) as pool:
        pool.starmap(send_request, data)


if __name__ == "__main__":
    run()
