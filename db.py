import mysql.connector
from configuration import get_param
import uuid


class Request:
    def __init__(self, email, requested_date, key):
        self.email = email
        self.requested_date = requested_date
        self.key = key


class DBConfig:
    def __init__(self, path):
        self.host = get_param(path, 'DB', 'host')
        self.port = int(get_param(path, 'DB', 'port'))
        self.user = get_param(path, 'DB', 'user')
        self.password = get_param(path, 'DB', 'password')
        self.database = get_param(path, 'DB', 'database')


def create_unique_key():
    key = uuid.uuid4().hex
    return key


def insert_request(config, request):
    connection = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database
    )
    cursor = connection.cursor()
    confirmed = 0
    active = 1
    query_template = "INSERT INTO Requests (Email, RequestedDate, UnKey, Confirmed, Active) VALUES ('{}', '{}', '{}', '{}', '{}')"
    query = query_template.format(request.email, request.requested_date, request.key, confirmed, active)
    cursor.execute(query)
    connection.commit()
    connection.close()


def read_requests(config, start_date, end_date):
    connection = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database
    )
    cursor = connection.cursor()
    str_a = start_date.strftime('%Y-%m-%d')
    str_b = end_date.strftime('%Y-%m-%d')
    sql_query = "SELECT Email, RequestedDate, UnKey FROM Requests WHERE RequestedDate BETWEEN '{}' AND '{}'".format(str_a, str_b)
    print(sql_query)
    cursor.execute(sql_query)
    requests = []
    for row in cursor:
        (email, requested_date, key) = row
        request = Request(email, requested_date.date(), key)
        requests.append(request)
    connection.close()
    print("Received {} requests".format(len(requests)))
    return requests


def find_request_by_key(config, key):
    connection = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database
    )
    cursor = connection.cursor()
    query = "SELECT Email, RequestedDate, UnKey FROM Requests Where UnKey = '{}'".format(key)
    cursor.execute(query)
    row = cursor.fetchone()
    request = None
    if row is not None:
        email, requested_date, key = row
        request = Request(email, requested_date.date(), key)
    connection.close()
    return request


def confirm_request(config, key):
    connection = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database
    )
    cursor = connection.cursor()
    query = "UPDATE Requests SET Confirmed = '1' Where UnKey = '{}'".format(key)
    cursor.execute(query)
    connection.commit()
    connection.close()
    return "Good"




if __name__ == '__main__':
    path = "~/jw-tour.ini"
    config = DBConfig(path)