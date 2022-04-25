import asyncio
import datetime
import os
# import random
import requests
import time

from pontis.core.const import NETWORK, ORACLE_ADDRESS
from pontis.core.utils import str_to_felt
from pontis.publisher.client import PontisPublisherClient
from starkware.crypto.signature.signature import sign
from starkware.cairo.lang.vm.crypto import pedersen_hash

DECIMALS = 18
P = 2 ** 251 + 17 * 2 ** 192 + 1
SLEEP_INTERVAL = 30

# def hex_to_felt(val):
#     return int(val, 16)

def hex_to_felt(val):
    return hex_to_int(val) % P

def hex_to_int(val):
    return int(val, 16)

def splitRandomness(val):
    return val[:32], val[32:]

async def main():
    PUBLISHER_PRIVATE_KEY = int(os.environ.get("PUBLISHER_PRIVATE_KEY"))
    PUBLISHER = "randomfeedooooor"
    KEY = "rand1"

    url = "https://drand.cloudflare.com"
    request_path = "/public/latest"
    method = "GET"
    headers = {"Accept": "application/json"}
    response = requests.request(method, url + request_path, headers=headers)
    response.raise_for_status()
    result = response.json()
    randomness = result["randomness"]
    part1, part2 = splitRandomness(randomness)
    randomnessFelt = pedersen_hash(hex_to_int(part1), hex_to_int(part2))
    # randomnessFelt = hex_to_felt(randomness)
    print(f"[INFO] drand result {result}")
    print(f"[INFO] randomness {randomness}, randomnessFelt {randomnessFelt}")

    # random_number = random.randrange(FELT_SIZE)
    timestamp = int(
                datetime.datetime.now(datetime.timezone.utc)
                .replace(tzinfo=datetime.timezone.utc)
                .timestamp()
            )

    # Step 1. Register publisher by providing the signed publisher to Pontis
    # team
    # signed = sign(str_to_felt(PUBLISHER), PUBLISHER_PRIVATE_KEY)
    # print(f"Signed {signed}")

    client = PontisPublisherClient(
        ORACLE_ADDRESS, PUBLISHER_PRIVATE_KEY, PUBLISHER, network=NETWORK
    )

    await client.publish(KEY, randomnessFelt, timestamp)

    print(f"Submitted random number {randomnessFelt} at timestamp {timestamp} for {PUBLISHER} under key {KEY}")


if __name__ == "__main__":
    while True:
        asyncio.run(main())
        print(f"Sleeping for {SLEEP_INTERVAL} seconds")
        time.sleep(SLEEP_INTERVAL)
