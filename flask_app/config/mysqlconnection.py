# MySQL connection will go here
import pymysql.cursors
import os

class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host=os.environ.get('DATA_BASE_HOST'),
            user=os.environ.get('DATA_BASE_USER'),
            password=os.environ.get('DATA_BASE_PASSWORD'),  
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        try:
            with self.connection.cursor() as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)

                if query.strip().lower().startswith('select'):
                    result = cursor.fetchall()
                    return result
                else:
                    return cursor.lastrowid
                
        except Exception as e:
            print(f"Query execution error: {e}")
            return False
        finally:
            self.connection.close()




