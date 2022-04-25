from starkware.crypto.signature.signature import get_random_private_key, private_to_stark_key

private = get_random_private_key()
stark = private_to_stark_key(private)
print(private)
print(stark)
