import random, string
from faker import Faker 

faker = Faker()

class RandomData:
    @staticmethod
    def get_username() -> str:
        return ''.join(faker.random_letters(length=random.randint(3,15)))

    
    @staticmethod
    def get_password() -> str:
        upper = [letter.upper() for letter in faker.random_letters(length=3)]
        lower = [letter.lower() for letter in faker.random_letters(length=3)]
        digits = [str(faker.random_digit()) for _ in range(3)]
        special = [random.choice("!@#$%^")]
        password_chars = upper + lower + digits + special
        random.shuffle(password_chars)
        return ''.join(password_chars)

    @staticmethod
    def get_balance() -> float:
        return round(random.uniform(1, 5000), 2)

    @staticmethod
    def get_invalid_balance() -> float:
        invalid_floats = [-1, -0.01, 5008, 'infddd']
        return random.choice(invalid_floats)
    
    @staticmethod
    def get_name() -> str:
        def random_word(length: int):
            return ''.join(random.choices(string.ascii_letters, k=length)).capitalize()
        first = random_word(random.randint(3, 8))
        last = random_word(random.randint(4, 10))
        return f"{first} {last}"

    
