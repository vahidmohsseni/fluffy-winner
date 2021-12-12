import requests

port = 5000
base_url = "http://localhost:" + str(port)


def send_sensor_data():
    data = {"location_id": 1,
            "plant_id": 1,
            "moisture_level": 40,
            "ph_level": 6.5,
            "temperature": 19}
    resp = requests.post(base_url + "/sensor", data=data)
    return resp.json()


def get_data_for_init():
    resp = requests.get(base_url + "/init_sim")
    return resp.json()


if __name__ == "__main__":
    print(send_sensor_data())
    # print(get_data_for_init())
