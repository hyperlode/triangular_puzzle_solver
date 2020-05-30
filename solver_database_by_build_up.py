import sqlite3
from sqlite3 import Error

import haley_puzzle_create_multithreading_task as haley_puzzle_attempts


'''
https://www.sqlitetutorial.net/sqlite-python/creating-database/
'''

NOT_TESTED = 0
TESTED = 1
TESTING_IN_PROGRESS = 2


#id int NOT NULL AUTO_INCREMENT,



class DatabaseSqlite3Actions():
    def __init__(self, path):
        self.conn = None
        self.create_connection(path)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
           
        except Error as e:
            print(e)
    
    # def create_table(self, create_table_sql):
    #     """ create a table from the create_table_sql statement
    #     :param conn: Connection object
    #     :param create_table_sql: a CREATE TABLE statement
    #     :return:
    #     """
    #     try:
    #         c = self.get_cursor()
    #         c.execute(create_table_sql)
    #     except Error as e:
    #         print(e)

    def get_cursor(self):
        return self.conn.cursor()

    def execute_sql(self, sql):
        cur = self.get_cursor()
        cur.execute(sql)
        return cur

    def execute_sql_return_rows(self, sql):
        cur = self.get_cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data


    def commit(self):
        self.conn.commit()

    def get_all_records(self, tablename):
        sql = "SELECT * FROM {}".format(tablename)
        return self.execute_sql_return_rows(sql)

    def get_row_count(self, table_name):
        result = self.execute_sql("select count(*) from {}".format(table_name))
        row = result.fetchone()
        return row[0]

    def get_rows(self, table, limit=100):
        sql = "SELECT * FROM {} LIMIT {}".format(table, limit)
        cur = self.execute_sql(sql)
        data = cur.fetchall()
        return data

class HaleyPuzzleBuildUpDatabase():
    def __init__(self, db_path):
        self.db_path = db_path
        self.db_connect(self.db_path)


        self.table_base_name = "sequences_level_{}"
        for level in range(11):
            self.create_table(self.table_base_name.format(level))

    def db_connect(self, db_path):
        self.db = DatabaseSqlite3Actions( db_path)
        
    def create_table(self, table_name):
        
        create_sequences_for_a_level_table = """CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sequence text ,
            status INTEGER,
            optional INTEGER
        );""".format(table_name)
        self.db.execute_sql(create_sequences_for_a_level_table)
        self.db.commit()

    def add_sequence(self, sequence, status):
        # sequence is an array of tuples. with (piece_id, piece_orientation)

        # convert to string of list of ints.
       
        table_name = self.sequence_to_table_name(sequence)
        savestr = self.sequence_to_str(sequence)

        sql_base = ''' INSERT INTO {} (sequence, status, optional)
                       VALUES('{}','{}','{}') '''
        sql = sql_base.format(table_name, savestr, status,'')

        self.db.execute_sql(sql)
        self.db.commit()
      
    def change_status(self, sequence, status):
        table_name = self.sequence_to_table_name(sequence)
        seqstr = self.sequence_to_str(sequence)

        sql = "UPDATE '{}' SET status = {} WHERE sequence = '{}'".format(table_name, status, seqstr)
        self.db.execute_sql(sql)
        self.db.commit()
           
    def get_sequence(self, desired_status, level, count):
        
        table_name = self.level_to_table_name(level)

        sql = " SELECT * from '{}' where status = {} LIMIT {}".format(
                table_name,
                desired_status,
                count,
                )
        rows = self.db.execute_sql_return_rows(sql)
        return rows

    def sequence_to_table_name(self, sequence):
        level= len(sequence)
        return self.level_to_table_name(level)

    def level_to_table_name(self, level):
        return self.table_base_name.format(level)
        
    def sequence_to_str(self, sequence):
        savestr = ""        
        for p,o in sequence:
            savestr += "{},{},".format(p,o)
        return savestr[:-1]  # delete last
    
    def str_to_sequence(self, seqstr):
        # expect str like: 1,2,345,6,7,8  --> even length!! (not odd)
        elements = seqstr.split(",")
        seq = []
        for p,o in zip(elements[0::2], elements[1::2]):
            seq.append((p,o))
        return seq

if __name__ == '__main__':
    
    db_path = r"C:\temp\haley_puzzle\Haley_puzzle_board_{}.db".format(0)
    solver_db = HaleyPuzzleBuildUpDatabase(db_path)
    # solver_db.add_sequence([(1,2),(3,4)], TESTING_IN_PROGRESS)
    # solver_db.change_status([(1,2),(3,4)],666)
    # print(solver_db.get_sequence(6677,2,4))