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

def query_word_recommendation(query):
    list_type, metric, amount = query = query
    con = connect_db()
    df = con.execute(f'''
    SELECT word, AVG({metric}::DOUBLE) as metric
    from word_stats
    WHERE word_list = {list_type} AND capital = 'false' AND symbols = 'false'
    GROUP BY word ORDER BY metric 
    LIMIT {amount}
    ''').fetchdf()
    con.close()
    return df['word'].tolist()

def query_count(con):
    con.execute("SELECT COUNT(*) FROM word_stats")
    print(con.fetchall())

# testing scripts
def main():
    con = connect_db_from_script()
    #drop_word_stats(con)
    # create_word_stats(con)
    query_count(con)
    con.close()

if __name__ == "__main__":
    main()