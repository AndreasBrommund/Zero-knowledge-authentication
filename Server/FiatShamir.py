import crypt_math
from DB import DatabaseConnection
import DB


class FiatShamir:
    def __init__(self, index=None, key_size=1024):

        self.db = DatabaseConnection()

        if index:
            self.id = index
            self.__load_from_db()
        else:
            self.__new_instance(key_size)

        print(self.id)
        print(self.n)

    def __load_from_db(self):
        self.n = DB.get_fiat_shamir(self.id, self.db)

    def __new_instance(self, key_size: int):
        p, q = crypt_math.generate_primes(key_size)
        self.n = p * q
        self.id = DB.new_fiat_shamir(self.n, self.db)

    def new_user(self, user_name, user_public_key):

        if not (1 <= user_public_key <= self.n - 1):
            print("User_public_key need to fulfill: 1 <= user_public_key <= n-1")
            return -1

        d, _, _ = crypt_math.extended_euclidean_algorithm(user_public_key, self.n)
        if d != 1:
            print("gcd(user_public_key,n) need to be equal to 1.")
            return -1

        exist = DB.public_key_exist(user_public_key, self.db)
        if exist:
            print("The user_public_key is not unique ")
            return -1

        user_id = DB.new_user(user_name, user_public_key, self.id, self.db)

        return user_id
