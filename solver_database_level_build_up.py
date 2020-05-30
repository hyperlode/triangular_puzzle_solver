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
        for level in range(12):  # tabel 1 to and including 11
            self.create_table(self.table_base_name.format(level))

    def db_connect(self, db_path):
        self.db = DatabaseSqlite3Actions( db_path)
    
    def row_count(self,level):
        table_name = self.level_to_table_name(level)
        return self.db.get_row_count(table_name)
        
    def create_table(self, table_name):
        
        create_sequences_for_a_level_table = """CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sequence text ,
            status INTEGER,
            optional INTEGER
        );""".format(table_name)
        self.db.execute_sql(create_sequences_for_a_level_table)
        self.db.commit()

    def add_sequences(self, sequences, status, commit=True):
        for seq in sequences:
            self.add_sequence(seq, status, False)

        if commit:
            self.db.commit()
            # print("commit")
        
    def add_sequence(self, sequence, status, commit=True):
        # sequence is an array of tuples. with (piece_id, piece_orientation)

        # convert to string of list of ints.
       
        table_name = self.sequence_to_table_name(sequence)
        savestr = self.sequence_to_str(sequence)

        sql_base = ''' INSERT INTO {} (sequence, status, optional)
                       VALUES('{}','{}','{}') '''
        sql = sql_base.format(table_name, savestr, status,'')

        self.db.execute_sql(sql)

        if commit:
            self.db.commit()
      
    def change_statuses(self, sequences, status, commit=True):
        for sequence in sequences:
            self.change_status(sequence, status, False)

        if commit:
            self.db.commit()
            
    def change_status(self, sequence, status, commit=True):
        table_name = self.sequence_to_table_name(sequence)
        seqstr = self.sequence_to_str(sequence)

        sql = "UPDATE '{}' SET status = {} WHERE sequence = '{}'".format(table_name, status, seqstr)
        self.db.execute_sql(sql)
        if commit:
            self.db.commit()
           
    def get_sequences(self, desired_status, level, count, mark_as_in_progress=False):
        
        table_name = self.level_to_table_name(level)
        
        with self.db.conn:
            sql = " SELECT * from '{}' where status = {} LIMIT {}".format(
                    table_name,
                    desired_status,
                    count,
                    )

            rows = self.db.execute_sql_return_rows(sql)
            sequences = []
            for row in rows:
                sequence = self.str_to_sequence(row[1])

                if mark_as_in_progress:
                    self.change_status(sequence, TESTING_IN_PROGRESS, False)

                sequences.append(sequence)
            
            if mark_as_in_progress:
                self.db.commit()  # commit status changes.

            return sequences

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
            seq.append((int(p),int(o)))
        return seq

if __name__ == '__main__':
    
    db_path = r"C:\temp\haley_puzzle\Haley_puzzle_board_{}.db".format(0)
    solver_db = HaleyPuzzleBuildUpDatabase(db_path)
    # solver_db.add_sequence([(2, 3), (3, 5), (11, 3), (6, 0), (1, 1), (4, 4), (7, 0), (5, 0), (10, 2), (9, 5)], NOT_TESTED)
    # solver_db.add_sequence([(1,2),(5,4)], TESTING_IN_PROGRESS)
    # solver_db.change_status([(1,2),(3,4)],666)
    print(solver_db.get_sequences(NOT_TESTED,10,4))
    print(solver_db.db.get_all_records("sequences_level_10"))
