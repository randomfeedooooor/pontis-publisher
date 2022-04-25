# Pontis Publisher

Publishes random numbers to Pontis

## Local Development

clone this repo

```shell
# Copy environment file
cp secrets.env .secrets.env

# Populate secrets
vim secrets.env
```

### How to publish data

```shell
docker build . -t pontis-publisher
docker run --env-file .secrets.env -t pontis-publisher
```

### How to query data

1. Navigate to <https://goerli.voyager.online/contract/0x039d1bb4904cef28755c59f081cc88a576ecdf42240fb73dd44ddd003848ce33#readContract>
1. Use `get_value` with `key=491260896305`

## Tasks

- [x] V0: Publish a constant number
- [x] V1: Publish a random number
- [x] V2: Use <https://drand.love/>
- [x] V3: Make script run continuously
- [ ] V4: Write verifier for drand (skipped because [https://github.com/0xNonCents/cairo-bls12-381](https://github.com/0xNonCents/cairo-bls12-381) isn't usable yet)
- [ ] V5: Write a Cairo proxy contract that accepts drand and proxies it to Pontis
- [ ] V6: Add a method to contract to subscribe to public key (put this in contract storage)
- [ ] V7: Add a method `setAlpha()` and `getAlpha()` to contract
- [ ] V8: Add a method to accept a proof and random number (random number = 1)(assume "verification" of proof is always true)
- [ ] V8: Accept `setAlpha()` from drand
