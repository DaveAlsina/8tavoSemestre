import api_gateway

if __name__ == '__main__':
    api = api_gateway.APIGateway()

    # register as user
    api.log_in("user", "password")

    # create a new user
    api.create_user("new_user", "new_password")

    # create a new zone
    api.create_zone({"name": "zone1", "description": "zone1 description"})

    # add a new measurement
    api.add_measurement({"zone": "zone1", "value": 1.5})