from openai import OpenAI
from dotenv import dotenv_values
import mariadb
import struct
from colorama import Fore, Style, init
import sys

# Initialize colorama
init(autoreset=True)

# Load environment variables
config = dotenv_values('.env')

# Initialize OpenAI with API key
api = OpenAI(api_key=config['OPENAI_API_KEY'])

# Define your embedding engine
EMBEDDING_ENGINE = 'text-embedding-ada-002'

# Database connection configuration
db_config = {
    'host': config['MARIADB_HOST'],
    'port': int(config['MARIADB_PORT']),
    'user': config['MARIADB_USER'],
    'password': config['MARIADB_PASSWORD'],
    'database': config['MARIADB_DATABASE'],
}


def get_embedding(query):
    """
    This function takes a text string and returns its embedding.
    """
    try:
        response = api.embeddings.create(
            input=[query],
            model=EMBEDDING_ENGINE,
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"{Fore.RED}Failed to generate embedding: {e}")
        return None


def fetch_documents(embedding):
    """
    This function takes an embedding and queries the database for the most
    relevant documents based on vector distance.
    """
    try:
        conn = mariadb.connect(**db_config)
        cur = conn.cursor()

        # Convert the embedding to a binary representation for MariaDB
        binary_repr = bytearray()
        for dim in embedding:
            binary_repr += bytearray(struct.pack("f", dim))

        hex_repr = binary_repr.hex()

        sql_query = f"""
        SELECT document, VEC_DISTANCE(embedding, x'{hex_repr}') dist
        FROM articles
        ORDER BY dist
        LIMIT 3
        """

        cur.execute(sql_query, (f"x'{hex_repr}'",))
        rows = cur.fetchall()

        return rows
    except mariadb.Error as e:
        print(f"{Fore.RED}Database error: {e}")
        return []
    finally:
        conn.close()


def main():
    print(f"{Fore.CYAN}Welcome to the Q&A app.")
    user_query = input(f"{Fore.GREEN}Enter your question: {Style.RESET_ALL}")

    embedding = get_embedding(user_query)
    if embedding:
        documents = fetch_documents(embedding)
        if documents:
            print(f"{Fore.YELLOW}Top 3 relevant documents:")
            for doc in documents:
                print(f"{Fore.LIGHTMAGENTA_EX}{doc[0]} - Distance: {doc[1]}")
        else:
            print(f"{Fore.RED}No documents found.")
    else:
        print(f"{Fore.RED}Could not process your query.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program terminated by user.")
        sys.exit()
