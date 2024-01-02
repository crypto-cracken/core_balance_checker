import blocksmith
import hdwallet
from hdwallet.derivations import BIP44Derivation
from hdwallet.cryptocurrencies import EthereumMainnet, LitecoinMainnet, DogecoinMainnet, DashMainnet, BitcoinMainnet
import traceback


def bip44(my_mnemonic: str, chain: str, depth: int) -> list[str]:
    addresses = []

    if chain == "eth":
        my_chain = EthereumMainnet
    elif chain == "ltc":
        my_chain = LitecoinMainnet
    elif chain == "doge":
        my_chain = DogecoinMainnet
    elif chain == "dash":
        my_chain = DashMainnet
    elif chain == "btc":
        my_chain = BitcoinMainnet

    for i in range(depth):
        try:
            wallet = hdwallet.BIP44HDWallet(cryptocurrency=my_chain)
            wallet.from_mnemonic(mnemonic=my_mnemonic, language="english", passphrase=None)
            wallet.clean_derivation()
            wallet_derivation: BIP44Derivation = BIP44Derivation(cryptocurrency=my_chain, account=0, change=False, address=i)
            wallet.from_path(path=wallet_derivation)
            address_to_check = wallet.address()
            addresses.append(address_to_check)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(f"Invalid mnemonic: {my_mnemonic}")

    return addresses


def get_from_privkey(privkey: str):
    try:
        address = blocksmith.BitcoinWallet.generate_address(privkey)
        return address
    except:
        return False
