import asyncio
import os
import random
import datetime
import requests

from pontis.core.const import NETWORK, ORACLE_ADDRESS
from pontis.core.utils import str_to_felt
from pontis.publisher.client import PontisPublisherClient
from starkware.crypto.signature.signature import sign

DECIMALS = 18
FELT_SIZE = 2 ** 252

async def main():
    PUBLISHER_PRIVATE_KEY = int(os.environ.get("PUBLISHER_PRIVATE_KEY"))
    PUBLISHER = "randomfeedooooor"
    KEY = "rand1"

    url = "https://drand.cloudflare.com"
    request_path = "/info"
    method = "GET"
    headers = {"Accept": "application/json"}
    response = requests.request(method, url + request_path, headers=headers)
    response.raise_for_status()
    result = response.json()
    print(f"result {result}")

    random_number = random.randrange(FELT_SIZE)
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

    await client.publish(KEY, random_number, timestamp)

    print(f"Submitted random number {random_number} at timestamp {timestamp} for {PUBLISHER} under key {KEY}")

if __name__ == "__main__":
    asyncio.run(main())
