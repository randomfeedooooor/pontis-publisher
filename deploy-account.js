const starknet = require("starknet")
const fs = require("fs")
const Json = require("json-bigint");

const { parse } = Json({
  alwaysParseAsBig: true,
  useNativeBigInt: true,
  protoAction: 'preserve',
  constructorAction: 'preserve',
});

const privateKey = <PRIVATE_KEY>
const starkKeyPair = starknet.ec.getKeyPair(privateKey);
const starkKeyPub = starknet.ec.getStarkKey(starkKeyPair);
compiledArgentAccount = parse(fs.readFileSync("./argent-account.txt", "utf-8"))

async function foo() {
    const accountResponse = await starknet.defaultProvider.deployContract({
        contract: compiledArgentAccount,
        addressSalt: starkKeyPub,
    });

    console.log(accountResponse)
}

foo();
