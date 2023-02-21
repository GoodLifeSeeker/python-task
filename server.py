import requests

from flask import Flask, request

from constants import (
    LOGIN_ENDPOINT,
    LOGIN_HEADERS,
    LOGIN_PAYLOAD,
    VEHICLES_ENDPOINT,
    COLOR_ENDPOINT
)

app = Flask(__name__)


def get_access_token(url, payload, headers):
    """Sends post request with given payload and headers to given endpoint's
    url and returns recieved access token."""
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["oauth"]["access_token"]


def api_modify(response):
    """Modifies api response by replacing None-values with empty string
    values. It is necessary because some of the values with the same dict
    key have different type, but in that way it will be easier to work with
    the data.

    For example we need concatenate 2 ctrings in get_color_data() func, but
    some of that values are None type."""
    for element in response:
        for key in element.keys():
            if element[key] is None:
                element[key] = ""
    return response


def get_color_data(cars_list, headers):
    """Creates endpoint's url with 'labelIds' value. Sends get request with
    given headers to that url recieves color data, replaces 'labelIds' value
    withe the color code. Returns modified list of dicts."""
    for car in cars_list:
        if car["labelIds"] != "":
            endpoint = COLOR_ENDPOINT + car["labelIds"]
            color_api_response = requests.get(endpoint, headers=headers)
            color_code = color_api_response.json()[0]["colorCode"]
            car["labelIds"] = color_code
    return cars_list


def is_in_api(csv_dict, api_dict):
    """Checks if the car from csv list is in api response."""
    counter = 0
    for key in csv_dict.keys():
        if csv_dict[key] == api_dict[key]:
            counter += 1
    if counter == len(csv_dict):
        return True
    return False


def merge_data(csv_cars, api_cars):
    """Merges csv data with api responce using intersection principle. If all
    values from csv line are equal to the values in api dict, then this car is
    positive to be added in final list to return to the client."""
    json_to_return = []
    for csv_car in csv_cars:
        for api_car in api_cars:
            if is_in_api(csv_car, api_car):
                json_to_return.append(api_car)
    return json_to_return


def hu_filter(merged_list):
    """Filters out any data which has empty 'hu' field."""
    list_filtered = filter(lambda d: d["hu"] != "", merged_list)
    list_filtered = list(list_filtered)
    return list_filtered


@app.route("/api/upload", methods=["POST"])
def upload():
    """Processes the request from client and returns to it ready-to-work list
    of dictionaries."""

    # Getting csv data
    csv_cars = request.get_json()

    # Getting access data
    access_token = get_access_token(
        LOGIN_ENDPOINT,
        LOGIN_PAYLOAD,
        LOGIN_HEADERS
    )
    vehicles_headers = {"Authorization": f"Bearer {access_token}"}

    # Getting and working with api response
    api_response = requests.get(VEHICLES_ENDPOINT, headers=vehicles_headers)
    api_response = api_response.json()
    api_response = api_modify(api_response)
    api_response = get_color_data(api_response, vehicles_headers)

    # Preparation data to return
    json_to_return = merge_data(csv_cars, api_response)
    json_to_return = hu_filter(json_to_return)
    return json_to_return


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
