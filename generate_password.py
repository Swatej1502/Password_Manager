import random
import string

class strongpassword:

    def generate_strong_password(min_length=8, max_length=16):
        # Define character sets
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        special_characters = string.punctuation

        # Create a pool of characters to choose from
        all_characters = lowercase_letters + uppercase_letters + digits + special_characters

        # Generate a random length for the password
        length = random.randint(min_length, max_length)

        # Ensure each character set is included in the password
        password = [random.choice(lowercase_letters),
                    random.choice(uppercase_letters),
                    random.choice(digits),
                    random.choice(special_characters)]

        # Add random characters from the pool to complete the password
        password += [random.choice(all_characters) for _ in range(length - 4)]

        # Shuffle the password to ensure randomness
        random.shuffle(password)
        return ''.join(password)
