import mysql.connector
from configuration import get_param


class Request:
    def __init__(self, email, requested_date):
        self.email = email
        self.requested_date = requested_date


class DBConfig:
    def __init__(self, path):
        self.host = get_param(path, 'DB', 'host')
        self.port = int(get_param(path, 'DB', 'port'))
        self.user = get_param(path, 'DB', 'user')
        self.password = get_param(path, 'DB', 'password')
        self.database = get_param(path, 'DB', 'database')


def insert_request(config, email, requested_date):
    connection = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database
    )
    cursor = connection.cursor()
    query = "INSERT INTO Requests (Email, RequestedDate) VALUES ('{}' , '{}')".format(email, requested_date)
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
    sql_query = "SELECT Email, RequestedDate FROM Requests WHERE RequestedDate BETWEEN '{}' AND '{}'".format(str_a, str_b)
    print(sql_query)
    cursor.execute(sql_query)
    requests = []
    for (email, requested_date) in cursor:
        requests.append(Request(email, requested_date.date()))
    connection.close()
    print("Received {} requests".format(len(requests)))
    return requests





if __name__ == '__main__':
    path = "~/jw-tour.ini"
    config = DBConfig(path)