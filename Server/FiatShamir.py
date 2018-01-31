import crypt_math
from DB import DatabaseConnection
import DB


class FiatShamir:
    def __init__(self, index=None, key_size=1024):

        self.db = DatabaseConnection()

        if index:
            self.index = index
            self.__load_from_db()
        else:
            self.__new_instance(key_size)

        print(self.index)
        print(self.n)

    def __load_from_db(self):
        index = DB.get_fiat_shamir(self.index, self.db)
        self.n = int.from_bytes(bytes(index), byteorder='big')

    def __new_instance(self, key_size):
        p, q = crypt_math.generate_primes(key_size)
        self.n = p * q
        self.index = DB.new_fiat_shamir(hex(self.n), self.db)
