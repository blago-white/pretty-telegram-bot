import psycopg2


def execute_query(postgres_connection: psycopg2.connect, sqlquery: str):

    with postgres_connection.cursor() as con:

        con.execute(sqlquery)

        try:
            data = con.fetchall()
            return data

        except:
            postgres_connection.commit()
