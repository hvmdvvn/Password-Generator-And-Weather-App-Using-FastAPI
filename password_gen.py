import random
import string
import click

def random_password(length=12):
    """Generate a random password of specified length."""

    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")

    # Ensure the password has at least one lowercase, one uppercase, one digit, and one special character
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice(string.punctuation)

    # Fill the rest of the password length with a mix of all character types
    all_characters = string.ascii_letters + string.digits + string.punctuation
    remaining_length = length - 4
    remaining_characters = ''.join(random.choices(all_characters, k=remaining_length))

    # Combine all characters and shuffle them to ensure randomness
    password_list = list(lowercase + uppercase + digit + special + remaining_characters)
    random.shuffle(password_list)

    return ''.join(password_list)


@click.command()
@click.option('--length', default=12, help='Length of the password to generate.')
def generate_password(length):
    """Generate a random password of specified length."""
    try:
        password = random_password(length)
        print(f"Generated Password: {password}")
    except ValueError as ve:
        print(ve)

if __name__ == "__main__":
    generate_password()


