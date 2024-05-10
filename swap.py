import base58
import base64
import json
import asyncio
import sys

from solders import message
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

from solana.rpc.types import TxOpts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Processed

from jupiter import Jupiter, Jupiter_DCA, get_checksum_address

# Retrieve the variable passed from JavaScript
private_key = sys.argv[1]
input_mint = sys.argv[2]
amount = sys.argv[3]
output_mint = sys.argv[4]

print(private_key)
print(output_mint)

private_key = Keypair.from_bytes(base58.b58decode(private_key)) # Private key as string
# private_key = Keypair.from_bytes(base58.b58decode(get_checksum_address("PRIVATE_KEY"))) # Private key as string
# client = AsyncClient("https://api.mainnet-beta.solana.com")
client = AsyncClient("https://jupiter-fe.helius-rpc.com/")
jupiter = Jupiter(client, private_key)


"""
EXECUTE A SWAP
"""
transaction_data = asyncio.run(jupiter.swap(
        # input_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        # output_mint="So11111111111111111111111111111111111111112",
        # amount=900_000,
        input_mint,
        output_mint,
        amount,
        slippage_bps=50,
    ))

# Returns str: serialized transactions to execute the swap.

raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(transaction_data))
signature = private_key.sign_message(message.to_bytes_versioned(raw_transaction.message))
signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
result = asyncio.run(client.send_raw_transaction(txn=bytes(signed_txn), opts=opts))
transaction_id = json.loads(result.to_json())['result']
# print(f"Transaction sent: https://explorer.solana.com/tx/{transaction_id}")
print(f"{transaction_id}")
