import importlib
import sys

from pyteal_helpers import program
from pyteal_helpers import utils

if __name__ == "__main__":
    outdir = sys.argv[1]

    module = sys.argv[2]

    contract = importlib.import_module(module)
    print(f"contract: {contract.__name__}")

    contract_args = sys.argv[3:]
    print(f"contract_args: {contract_args}")

    file_name = f"{contract.__name__.split('.')[-1]}_{'_'.join(contract_args)}"
    print(f"file name: {file_name}")

    pyteal = contract.create(*contract_args)

    algod_client = utils.get_algod_client()

    sig = program.signature(algod_client, pyteal)

    print(f"Logic Signature Address: {sig.address}")

    with open(f"{outdir}/{file_name}.teal", "w") as h:
        h.write(sig.teal)
