# Connector: https://github.com/PyMySQL/PyMySQL

import pymysql.cursors


class MySQL(object):
    def __init__(self, host, user, password, database, query):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.query = query

    def run(self):
        connection = pymysql.connect(host=self.host,
                                     user=self.user,
                                     password=self.password,
                                     db=self.database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        # TODO: Yet to test!
        query_type = self.query.strip()[0].lower()
        try:
            with connection.cursor() as cursor:
                # Execute the query - Allow only select queries?
                cursor.execute(self.query)
                if query_type == "s":
                    result = cursor.fetchone()
                    print(result)
                elif query_type == "c" or query_type == "u":
                    connection.commit()

        finally:
            connection.close()


