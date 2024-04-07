import struct

import mariadb
import tqdm
from dotenv import dotenv_values
from openai import OpenAI


config = dotenv_values('.env')

# We load the API KEY from the .env file.
api = OpenAI(api_key=config['OPENAI_API_KEY'])

EMBEDDING_ENGINES = (
    'text-embedding-ada-002',
    'text-embedding-3-small',
    'text-embedding-3-large',
)

# Database connection parameters
config = {
    'host': config['MARIADB_HOST'],
    'port': int(config['MARIADB_PORT']),
    'user': config['MARIADB_USER'],
    'password': config['MARIADB_PASSWORD'],
    'database': config['MARIADB_DATABASE'],
}


try:
    # Connect to MariaDB
    conn = mariadb.connect(**config, default_file='foo')

    # Create a cursor object
    cur = conn.cursor()

    # SQL query to select all text from a table
    sql_query = "SELECT description, example, url FROM mysql.help_topic"

    # Execute the query
    cur.execute(sql_query)

    # Fetch all the rows
    rows = cur.fetchall()

    # Print each row
    for row in tqdm.tqdm(rows):
        (description, example, url) = row

        input = f'Description: {description}, Example: {example} URL: {url}'
        try:
            response = api.embeddings.create(
                input=[input],
                # You can choose a different model to compare performance
                model=EMBEDDING_ENGINES[0],
            )
        except Exception:
            # There may be OpenAI errors. For simplicity we ignore those errors
            continue

        embedding = response.data[0].embedding

        # convert each float in the embedding to a bytearray
        binary_repr = bytearray()
        for dim in embedding:
            binary_repr += bytearray(struct.pack("f", dim))

        q = "INSERT INTO articles (document, embedding) values (?, ?)"

        cur.execute(q, (f"'{input}'", bytes(binary_repr)))


except mariadb.Error as e:
    print(e, input)
finally:
    # Close the connection
    if conn:
        conn.close()
