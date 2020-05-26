import sqlite3
from sqlite3 import Error

import haley_puzzle_create_multithreading_task as haley_puzzle_attempts

'''
https://www.sqlitetutorial.net/sqlite-python/creating-database/
'''


create_attempts_table = """CREATE TABLE IF NOT EXISTS attempts (
    id int ,
	sequence text PRIMARY KEY,
	is_tested integer,
    is_solution integer,
    seconds_epoch_requested integer,
    requester text
);"""

#id int NOT NULL AUTO_INCREMENT,

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
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

def add_attempt(conn, attempt_string, manual_id=None):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO attempts(id, sequence, is_tested, is_solution, seconds_epoch_requested, requester)
              VALUES(? ,?,?,?,?,?) '''
    cur = conn.cursor()

    if manual_id is not None:
        data = (manual_id, attempt_string,0,0,0,'')
    else:
        data = (attempt_string,0,0,0,'')
    cur.execute(sql, data)
    return cur

def commit(conn):
    conn.commit()

def get_all_records(conn, table):
    sql = "SELECT * FROM {}".format(table)
    cur = execute_sql(conn, sql)
    data = cur.fetchall()
    return data

def execute_sql(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    return cur



def setup_haley_puzzle_attempts_no_boards():
    conn = create_connection(r"D:\Temp\puzzle_haley\attempts_no_boards.db")

   
    # all used pieces indeces
    used_pieces = [1,2,3,4,5,6,7,8,9,10,11]

    # create tables
    if conn is None:
        print("Error! cannot create the database connection.")
        raise Error
    create_table(conn, create_attempts_table)

    attemps_iterator = haley_puzzle_attempts.PermutationAsString(used_pieces)
    
    for i, sequence in enumerate(attemps_iterator):
        try:
            add_attempt(conn, sequence, i)
        except sqlite3.IntegrityError:
           
            pass
            
    commit(conn)

    # records = get_all_records(conn, "attempts")
    
def setup_haley_puzzle_attempts():
     # conn = create_connection(r"C:\temp\haley_puzzle\pythonsqlite.db")
    conn = create_connection(r"D:\Temp\puzzle_haley\attempts.db")

   
    # all used pieces indeces
    used_pieces = [1,2,3,4,5,6,7,8,9,10,11]

    # board indeces 
    boards = ['a','b','c','d','e']
            
    # create tables
    if conn is None:
        print("Error! cannot create the database connection.")
        raise Error
    create_table(conn, create_attempts_table)
    
    # sql_set_auto_increment = "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'attempts'"
    # sql_set_auto_increment = "UPDATE sqlite_sequence SET seq = 666 WHERE name = 'attempts';"
    # execute_sql(conn, sql_set_auto_increment)


    # INSERT INTO sqlite_sequence (name,seq) SELECT '<table>', <n> WHERE NOT EXISTS 
    #         (SELECT changes() AS change FROM sqlite_sequence WHERE NOT EXISTS SELECT name from sqlite_sequence WHERE name = 'table');

    # add_attempt(conn, "test", 666)


    attemps_iterator = haley_puzzle_attempts.PermutationAsString(used_pieces, boards)
    
    

    # for i in range(110):
    #     try:
    #         add_attempt(conn, next(attemps_iterator), i)
    #     except sqlite3.IntegrityError:
           
    #         pass
    for i, sequence in enumerate(attemps_iterator):
        try:
            add_attempt(conn, sequence, i)
        except sqlite3.IntegrityError:
           
            pass
            
    commit(conn)

    records = get_all_records(conn, "attempts")
    # for r in records[:110]:
    #     print(r)
        
if __name__ == '__main__':
   # conn = create_connection(r"C:\temp\haley_puzzle\pythonsqlite.db")
    # conn = create_connection(r"D:\Temp\puzzle_haley\attempts.db")

    setup_haley_puzzle_attempts_no_boards()

    # result = execute_sql(conn, "select count(*) from attempts")

    # num_of_rows = result[0][0]
    # print(num_of_rows)