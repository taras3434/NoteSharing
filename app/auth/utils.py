from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Hash password for secure storage.

    Args:
        password (str): Password.

    Returns:
        str: The hashed password.
    """
    return generate_password_hash(password)

def check_password(password_hash, password):
    """
    Verify a unhashed password against the stored hashed password.

    Args:
        password_hash (str): Hashed password.
        password (str): Unhashed password.

    Returns:
        bool: True if the password matches.
    """
    return check_password_hash(password_hash, password)