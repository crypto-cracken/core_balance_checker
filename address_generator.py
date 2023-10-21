import bip_utils
import hdwallet
from hdwallet.derivations import BIP44Derivation
from hdwallet.cryptocurrencies import LitecoinMainnet, DogecoinMainnet, DashMainnet, BitcoinMainnet


def bip44(my_mnemonic: str, chain: str):
    if chain == "ltc":
        my_chain = LitecoinMainnet
    elif chain == "doge":
        my_chain = DogecoinMainnet
    elif chain == "dash":
        my_chain = DashMainnet
    elif chain == "btc":
        my_chain = BitcoinMainnet
    else:
        return False

    try:
        wallet = hdwallet.BIP44HDWallet(cryptocurrency=my_chain)
        wallet.from_mnemonic(mnemonic=my_mnemonic, language="english", passphrase=None)
        wallet.clean_derivation()
        wallet_derivation: BIP44Derivation = BIP44Derivation(cryptocurrency=my_chain, account=0, change=False, address=0)
        wallet.from_path(path=wallet_derivation)
        address_to_check = wallet.address()
        return address_to_check
    except:
        print(f"Invalid mnemonic: {my_mnemonic}")
        return False


def bip84(my_mnemonic: str):
    try:
        my_seed = bip_utils.Bip39SeedGenerator(my_mnemonic).Generate()
        bip84_wallet = bip_utils.Bip84.FromSeed(my_seed, bip_utils.Bip84Coins.BITCOIN)
        bip84_wallet_1 = (bip84_wallet.Purpose().Coin().Account(0)).Change(bip_utils.Bip44Changes.CHAIN_EXT)
        bip84_wallet_2 = bip84_wallet_1.AddressIndex(0)
        bip84 = bip84_wallet_2.PublicKey()
        address_to_check = bip84.ToAddress()
        return address_to_check
    except:
        print(f"Invalid mnemonic: {my_mnemonic}")
        return False
