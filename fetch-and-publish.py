import asyncio
import os
from hashlib import sha256
from datetime import datetime

from pontis.core.const import NETWORK, ORACLE_ADDRESS
from pontis.core.utils import str_to_felt
from pontis.publisher.client import PontisPublisherClient
from starkware.crypto.signature.signature import sign

DECIMALS = 18

async def main():
    PUBLISHER_PRIVATE_KEY = int(os.environ.get("PUBLISHER_PRIVATE_KEY"))
    PUBLISHER = "randomfeedooooor"
    KEY = "rand1"
    RANDOM_NUMBER = 422
    timestamp = 3

    # Step 1. Register publisher by providing the signed publisher to Pontis
    # team
    # signed = sign(str_to_felt(PUBLISHER), PUBLISHER_PRIVATE_KEY)
    # print(f"Signed {signed}")

    client = PontisPublisherClient(
        ORACLE_ADDRESS, PUBLISHER_PRIVATE_KEY, PUBLISHER, network=NETWORK
    )

    await client.publish(KEY, RANDOM_NUMBER, timestamp)

    print(f"Submitted random number {RANDOM_NUMBER} for {PUBLISHER} under key {KEY} at timestamp {timestamp}")

if __name__ == "__main__":
    asyncio.run(main())
