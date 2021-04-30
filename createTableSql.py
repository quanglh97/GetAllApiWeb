
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"GET_API_DATABASE.db"
    conn = None

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS DOMAINS (
                                        id integer PRIMARY KEY,
                                        domain text NOT NULL,
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES DOMAINS (id)
                                );"""

    sql_create_test_table = """CREATE TABLE IF NOT EXISTS test (
                                    id integer PRIMARY KEY,
                                    project_id text NOT NULL,
                                    request text,
                                    response text
                                );"""
    
    sql_create_domain_table = """CREATE TABLE IF NOT EXISTS DOMAIN (
                                    id integer PRIMARY KEY,
                                    domain text NOT NULL
                                    );"""

    sql_create_api_table = """CREATE TABLE IF NOT EXISTS API(
    id integer PRIMARY KEY,
    api du lieuj chua dinh ;...
    )"""
    
    

    conn = create_connection(database)
    # create tables
    # if conn is not None:
    #     # create projects table
    #     create_table(conn, sql_create_projects_table)

    #     # create tasks table
    #     create_table(conn, sql_create_tasks_table)
    # else:
    #     print("Error! cannot create the database connection.")

    #create tables
    if conn is not None:
        create_table(conn, sql_create_domain_table)
    else:
        print("ERROR! cannot create the database connection")
        return

    # #insert data into database
    # thisdict = {
    #     "request": "Fordaskdjhfkajsdf",
    #     "response": "404",
    #     }
    # c = conn.cursor()
    # sql = ''' INSERT INTO test (project_id,request, response)
    #         VALUES(?,?,?) '''
    # c.execute(sql, ('1',thisdict['request'], thisdict['response']))
    # conn.commit()

if __name__ == "__main__":
    main()