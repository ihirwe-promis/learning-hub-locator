import mysql.connector


def connect_database():

    connection = mysql.connector.connect(
        host="mysql-267997fe-alustudent-08b3.a.aivencloud.com",
        user="avnadmin",
        port=19949,
        password="MY_PASSWORD",
        database="learning_hub"
    )

    return connection
