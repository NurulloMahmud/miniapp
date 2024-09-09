import hashlib
import hmac
import urllib.parse

def verify_telegram_auth(init_data, token):
    """
    Verifies the Telegram Mini App initialization data received from the frontend.
    """
    # Parse the init_data string
    params = dict(urllib.parse.parse_qsl(init_data))  # Converting the init data to a dictionary
    check_hash = params.pop('hash', None)

    if not check_hash:
        return False  # No hash found, invalid

    # Creating a secret key from the bot token
    secret_key = hashlib.sha256(token.encode()).digest()

    # Prepare data_check_string by sorting parameters alphabetically and concatenating them
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(params.items())])

    # Recalculate the hash using HMAC and compare it with the received check_hash
    recalculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return recalculated_hash == check_hash, params  # Return True if hash matches and parsed data
