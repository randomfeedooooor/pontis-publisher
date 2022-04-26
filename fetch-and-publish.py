import asyncio
import datetime
import os
# import random
import requests
import time

from pontis.core.const import NETWORK, ORACLE_ADDRESS
from pontis.core.utils import str_to_felt, hash_entry
from pontis.core.entry import Entry
from pontis.publisher.client import PontisPublisherClient
from starkware.crypto.signature.signature import sign
from starkware.cairo.lang.vm.crypto import pedersen_hash
from starkware.crypto.signature.signature import get_random_private_key, private_to_stark_key

import ecvrf

SLEEP_INTERVAL = 30 # seconds
P = 2 ** 251 + 17 * 2 ** 192 + 1

def hex_to_felt(val):
    return hex_to_int(val) % P

def hex_to_int(val):
    return int(val, 16)

def split_randomness(val):
    return val[:32], val[32:]

def debug_publish(client, key, value, timestamp):
    if type(key) == str:
        key = str_to_felt(key)

    entry = Entry(
        key=key, value=value, timestamp=timestamp, publisher=client.publisher
    )
    print(f"entry: {entry}")
    print(f"hash_entry(): {hash_entry(entry)}")
    signature_r, signature_s = sign(hash_entry(entry), client.publisher_private_key)
    print(f"key: {key}\nvalue: {value}\ntimestamp: {timestamp}\npublisher: {client.publisher}\nsignature_r: {signature_r}\nsignature_s: {signature_s}\n")

async def main():

    # Constants
    PUBLISHER_PRIVATE_KEY = int(os.environ.get("PUBLISHER_PRIVATE_KEY"))
    PUBLISHER = "randomfeedooooor"
    KEY = "rand1"

    # Register publisher by providing the signed publisher to Pontis team
    # signed = sign(str_to_felt(PUBLISHER), PUBLISHER_PRIVATE_KEY)
    # print(f"Signed publisher {signed}")

    # Initialize client
    client = PontisPublisherClient(
        ORACLE_ADDRESS, PUBLISHER_PRIVATE_KEY, PUBLISHER, network=NETWORK
    )

    # Get random number from drand and conver to felt
    url = "https://drand.cloudflare.com"
    request_path = "/public/latest"
    method = "GET"
    headers = {"Accept": "application/json"}
    response = requests.request(method, url + request_path, headers=headers)
    response.raise_for_status()
    result = response.json()
    randomness = result["randomness"]
    part1, part2 = split_randomness(randomness)
    randomnessFelt = pedersen_hash(hex_to_int(part1), hex_to_int(part2))
    print(f"[INFO] drand result {result}")
    print(f"[INFO] randomness {randomness}")
    print(f"[INFO] randomnessFelt {randomnessFelt}")

    # Initial random seed from python
    private_key = get_random_private_key()

    # The public key generated from the private key through stark
    # is different from public key geenrated by ecvrf
    # stark_key = private_to_stark_key(private_key)

    private_key = private_key.to_bytes(32, 'big')
    public_key = ecvrf.get_public_key(private_key)

    # Drand randomnessFelt as alpha (octet string)
    alpha_string = randomnessFelt.to_bytes(32, 'big')
    alpha_octet = alpha_string[0:8]

    # status returns valid or invalid upon completion
    p_status, pi_string = ecvrf.ecvrf_prove(private_key, alpha_octet)
    b_status, beta_string = ecvrf.ecvrf_proof_to_hash(pi_string)

    print('p_status: ', p_status)
    print('pi_string: ', pi_string)
    print('b_status: ', b_status)
    print('beta_string: ', beta_string)

    # Check verify internally to make sure pi and beta are correct
    result, beta_string2 = ecvrf.ecvrf_verify(public_key, pi_string, alpha_octet)
    print('result: ', result)
    print('beta_string2: ', beta_string2)
    if p_status == "VALID" and b_status == "VALID" and result == "VALID" and beta_string == beta_string2:
        print("COMMITMENT VERIFIED")
    else:
        print("COMMITMENT NOT VERIFIED")


    timestamp = int(
                datetime.datetime.now(datetime.timezone.utc)
                .replace(tzinfo=datetime.timezone.utc)
                .timestamp()
            )

    await client.publish(KEY, beta_string, timestamp)
    debug_publish(client, KEY, beta_string, timestamp)
    print(f"Submitted random number {beta_string} at timestamp {timestamp} for {PUBLISHER} under key {KEY}")


if __name__ == "__main__":
    while True:
        asyncio.run(main())
        print(f"Sleeping for {SLEEP_INTERVAL} seconds")
        time.sleep(SLEEP_INTERVAL)
