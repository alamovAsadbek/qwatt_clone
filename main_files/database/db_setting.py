import psycopg2


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = psycopg2.connect('database.db')
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            self.connection.rollback()
        else:
            self.connection.commit()

        if self.connection is not None:
            self.connection.close()

        if self.cursor is not None:
            self.cursor.close()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query, params=None):
        self.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        self.execute(query, params)
        return self.cursor.fetchone()


def execute_query(query, params=None, fetch=None):
    try:
        with Database() as db:
            if fetch == "all":
                return db.fetchall(query, params)
            elif fetch == "one":
                return db.fetchone(query, params)
            else:
                db.execute(query, params)
    except Exception as e:
        print(f"Exception occurred while executing: {e}")

# query_ = 'INSERT INTO users (first_name, last_name, gmail, gender, password) VALUES (%s, %s, %s, %s, %s);'
# params_ = ('John', 'Doe', 'gmail@gamil.com', 'male', 'password',)
# execute_query(query_, params_)

