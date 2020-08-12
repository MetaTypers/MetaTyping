import duckdb
import pandas as pd


# DB connections
def connect_db():
    con = duckdb.connect(database='words.db', read_only=False)
    return con

def connect_db_from_script():
    con = duckdb.connect(database='../words.db', read_only=False)
    return con

# CREATE TABLE
def create_word_stats(con):
    con.execute('''
    CREATE TABLE IF NOT EXISTS word_stats(
        word       VARCHAR,
        word_list  INTEGER,
        wpm        INTEGER,
        wpm_space  INTEGER,
        accuracy   BOOLEAN,
        capital    BOOLEAN,
        symbols    BOOLEAN,
        date       DATE
    )''')

# DROP TABLE
def drop_word_stats(con):
    con.execute("DROP TABLE IF EXISTS word_stats")

# BULK INSERT RECORDS
def load_df():
    df = pd.read_pickle('word_stats.pkl')
    return df

def insert_df(con, df):
    con.register('word_stats_view', df)
    con.execute('INSERT INTO word_stats SELECT * FROM word_stats_view')

def bulk_insert_word_stats():
    con = connect_db()
    create_word_stats(con)
    df = load_df()
    insert_df(con, df)
    con.close()

# QUERY SEARCHES
def slowest_word_by_list(con, word_list):
    # WHERE word_list == {word_list} ORDER BY wpm
    con.execute(f"SELECT word, count(word) AS ct FROM word_stats GROUP BY word ORDER BY ct")
    word_list = con.fetchall()
    print(word_list)

def pandas_view(con):
    df = con.execute("SELECT word, count(word) AS ct FROM word_stats GROUP BY word ORDER BY ct").fetchdf()
    print(df)

def query_count(con):
    con.execute("SELECT COUNT(*) FROM word_stats")
    print(con.fetchall())

# testing scripts
def main():
    con = connect_db_from_script()
    #drop_word_stats(con)
    # create_word_stats(con)
    #con.execute("SELECT * FROM word_stats")
    # slowest_word_by_list(con, 1)
    pandas_view(con)
    con.close()

if __name__ == "__main__":
    main()