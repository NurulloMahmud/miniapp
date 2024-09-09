import hashlib
import hmac


def verify_telegram_auth(data, token):
    secret_key = hashlib.sha256(token.encode()).digest()
    check_hash = data.pop('hash', None)
    if not check_hash:
        return False

    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == check_hash
