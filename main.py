import utils
import address_generator
import configparser
import os
import time
import platform
import time
import requests
import random
import concurrent.futures
from itertools import repeat


def get_balance(my_mnemonic: str, my_proxy_list: list, proxy_type: str, usd_price: float, chain: str):
    if chain == "btc":
        address = address_generator.bip84(my_mnemonic)
    else:
        address = address_generator.bip44(my_mnemonic, chain)

    if not address:
        return False

    while True:
        try:
            # set proxies
            proxy = random.choice(my_proxy_list)
            if proxy_type.lower() == "http":
                my_proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            elif proxy_type.lower() == "socks5":
                my_proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
            else:
                print("Wrong proxy type, use 'http' or 'socks5'")
                return False

            # get response
            response = requests.get(
                f"https://api.blockcypher.com/v1/{chain}/main/addrs/{address}",
                proxies=my_proxies,
            )

            # get balance
            if chain == "eth":
                balance = response.json()["balance"] / 1000000000000000000
            else:
                balance = response.json()["balance"] / 100000000
            balance_usd = int(balance * usd_price)

            # save results
            if balance_usd > 1:
                print(f"{my_mnemonic} : {chain.upper()} : {balance_usd}$")
                with open(f"with_balance_{chain}.txt", "a", encoding="utf8") as f:
                    f.write(f"{my_mnemonic} : {address} : {balance_usd}$\n")

            # break if successful, repeat and change proxy if failed
            break
        except Exception as e:
            time.sleep(1)
            continue

    with open(f"checked_{chain}.txt", "a", encoding="utf8") as f:
        f.write(f"{my_mnemonic}\n")


def get_usd_price(chain: str) -> float:
    usd_price = float(requests.get(f"https://coincodex.com/api/coincodex/get_coin/{chain}").json()["last_price_usd"])
    print(f"{chain.upper()} price: {usd_price}$")
    time.sleep(1)
    return usd_price


if __name__ == "__main__":
    # set title
    title = "Crypto Cracken Balance Checker V1.1.0"
    system_type = platform.system()
    if system_type == "Windows":
        os.system("title " + title)
    elif system_type == "Linux":
        print(f"\33]0;{title}\a", end="", flush=True)

    # parse config
    config = configparser.ConfigParser()
    config.read(utils.get_file_path("settings.ini"))
    threads = int(config["MAIN"]["threads"])
    proxy_type = config["MAIN"]["proxy_type"]
    check_eth = config["CHAINS"].getboolean("check_eth")
    check_btc = config["CHAINS"].getboolean("check_btc")
    check_ltc = config["CHAINS"].getboolean("check_ltc")
    check_doge = config["CHAINS"].getboolean("check_doge")
    check_dash = config["CHAINS"].getboolean("check_dash")

    # parse mnemonics
    mnemonics = set()
    with open("seeds.txt", "r", encoding="utf8") as f:
        for line in f:
            mnemonics.add(line.strip())
    print(f"Found seeds: {len(mnemonics)}")

    # parse mnemonics
    proxy_list = set()
    with open("proxies.txt", "r", encoding="utf8") as f:
        for line in f:
            proxy_list.add(line.strip())
    print(f"Found proxies: {len(proxy_list)}")

    # get usd prices
    print("Getting usd prices...")
    usd_prices = {}
    if check_eth:
        usd_prices["eth"] = get_usd_price("eth")
    if check_btc:
        usd_prices["btc"] = get_usd_price("btc")
    if check_ltc:
        usd_prices["ltc"] = get_usd_price("ltc")
    if check_doge:
        usd_prices["doge"] = get_usd_price("doge")
    if check_dash:
        usd_prices["dash"] = get_usd_price("dash")

    mnemonics = list(mnemonics)
    proxy_list = list(proxy_list)

    # check balance
    if check_eth:
        print("Checking ETH")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["eth"]),
                repeat("eth"),
            )

    if check_btc:
        print("Checking BTC")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["btc"]),
                repeat("btc"),
            )

    if check_ltc:
        print("Checking LTC")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["ltc"]),
                repeat("ltc"),
            )

    if check_doge:
        print("Checking DOGE")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["doge"]),
                repeat("doge"),
            )

    if check_dash:
        print("Checking DASH")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["dash"]),
                repeat("dash"),
            )
