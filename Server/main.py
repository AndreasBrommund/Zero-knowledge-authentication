from DB import DatabaseConnection
import DB


def main():

    db = DatabaseConnection("zeroknowledgeauthentication",  "postgres", "127.0.0.1", "")

if __name__ == "__main__":
    main()