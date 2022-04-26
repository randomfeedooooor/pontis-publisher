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
# Publish to Pontis
docker build . --tag publish-to-pontis --file ./publish-to-pontis.Dockerfile
docker run --env-file .secrets.env -t publish-to-pontis

# Publish to verifier (work in progress)
docker build . --tag publish-to-verifier --file ./publish-to-verifier.Dockerfile
docker run --env-file .secrets.env -t publish-to-verifier
```

### How to query data

1. Navigate to <https://goerli.voyager.online/contract/0x039d1bb4904cef28755c59f081cc88a576ecdf42240fb73dd44ddd003848ce33#readContract>
1. Use `get_value` with `key=491260896305`

## Tasks

- [x] V0: Publish a constant number
- [x] V1: Publish a random number
- [x] V2: Use <https://drand.love/>
- [x] V3: Make script run continuously
- [ ] V4: Write verifier for drand (skipped because [https://github.com/0xNonCents/cairo-bls12-381](https://github.com/0xNonCents/cairo-bls12-381) isn't usable yet. bls12-381 tests take 35 mins to run in native cairo so we attempted to run in [oriac](https://github.com/xJonathanLEI/oriac) but fails [here](https://github.com/xJonathanLEI/oriac/blob/master/src/cairo/lang/vm/cairo_runner.rs#L634))
- [ ] V5: Write a Cairo proxy contract that accepts drand and proxies it to Pontis
- [ ] V6: Add a method `setPublicKey(publicKey: felt)` to contract (put this in contract storage)
- [ ] V7: Add a method `setAlpha(alpha: felt)` and `getAlpha()` to contract
- [ ] V8: Add a method to accept a proof and random number (random number = 1)(assume "verification" of proof is always true)
- [ ] V8: Accept `setAlpha(alpha: felt)` from drand relayer
