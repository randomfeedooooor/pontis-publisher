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

1. Navigate to <https://goerli.voyager.online/contract/0x039d1bb4904cef28755c59f081cc88a576ecdf42240fb73dd44ddd003848ce33#readContract>=
1. Use `get_value` with `key=491260896305``

## Links

1. <https://cairo-utils-web.vercel.app/>
1. <https://rocky-volleyball-654.notion.site/Pontis-f5103d8ecc9d49a6844323819570c1b6>
1. <https://hub.docker.com/r/42labs/pontis-publisher/>
