import utils
import address_generator
import configparser
import time
import os
import requests
import random
import concurrent.futures
from itertools import repeat


def get_balance(my_mnemonic: str, depth: int, input_type: str, my_proxy_list: list, proxy_type: str, usd_price: float, chain: str):
    addresses = []

    if input_type == "seeds":
        addresses = address_generator.bip44(my_mnemonic, chain, depth)
    elif input_type == "privkeys":
        if chain == "btc":
            address = address_generator.get_from_privkey(my_mnemonic)
            addresses.append(address)
        else:
            return False
    else:
        addresses.append(my_mnemonic)

    addresses = [i for i in addresses if i]
    if len(addresses) == 0:
        return False

    for address in addresses:
        while True:
            try:
                # set proxies
                proxy = random.choice(my_proxy_list)
                if proxy_type.lower() == "http":
                    my_proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                elif proxy_type.lower() == "socks5":
                    my_proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
                else:
                    print(utils.bcolors.RED + "Wrong proxy type, use 'http' or 'socks5'" + utils.bcolors.END)
                    return False

                # get response
                response = requests.get(
                    f"https://api.blockcypher.com/v1/{chain}/main/addrs/{address}",
                    proxies=my_proxies,
                    timeout=10,
                )

                # get balance
                if chain == "eth":
                    balance = response.json()["balance"] / 1000000000000000000
                else:
                    balance = response.json()["balance"] / 100000000
                total_balance = int(balance * usd_price)

                # save results
                output = "+--------------------+--------------------------------------------------------------------+\n"
                if input_type == "seeds" or input_type == "privkeys":
                    output += f"| Mnemonic...........| {my_mnemonic}\n"
                output += f"| Address............| {address}\n"
                output += f"| Chain..............| {chain.upper()}\n"
                output += f"| Balance............| {total_balance}$\n"

                if total_balance > 1:
                    utils.save_result(output, chain, True)
                else:
                    utils.save_result(output, chain, False)

            except Exception as e:
                print(utils.bcolors.RED + f"ERROR (Banned Proxy):\n{e}\n" + utils.bcolors.END)
                time.sleep(3)
                continue

            break


def get_usd_price(chain: str) -> float:
    usd_price = float(requests.get(f"https://coincodex.com/api/coincodex/get_coin/{chain}").json()["last_price_usd"])
    print(f"{chain.upper()} price: {usd_price}$")
    time.sleep(1)
    return usd_price


if __name__ == "__main__":
    # set title
    utils.set_title("Core Balance Checker")

    # parse config
    config = configparser.ConfigParser()
    config.read(utils.get_file_path("settings.ini"))
    threads = int(config["MAIN"]["threads"])
    proxy_type = config["MAIN"]["proxy_type"]
    input_type = config["MAIN"]["input_type"]
    depth = int(config["MAIN"]["depth"])
    check_eth = config["CHAINS"].getboolean("check_eth")
    check_btc = config["CHAINS"].getboolean("check_btc")
    check_ltc = config["CHAINS"].getboolean("check_ltc")
    check_doge = config["CHAINS"].getboolean("check_doge")
    check_dash = config["CHAINS"].getboolean("check_dash")

    # parse mnemonics
    mnemonics = set()
    with open("input.txt", "r", encoding="utf8") as f:
        for line in f:
            mnemonics.add(line.strip())
    print(f"Found seeds: {len(mnemonics)}")

    # parse proxy
    proxy_list = set()
    with open("proxy.txt", "r", encoding="utf8") as f:
        for line in f:
            proxy_list.add(line.strip())
    print(f"Found proxies: {len(proxy_list)}")

    mnemonics = list(mnemonics)
    proxy_list = list(proxy_list)

    # results
    dir = utils.get_file_path(f"results")
    if not os.path.exists(dir):
        os.makedirs(dir)

    # get usd prices
    print("")
    utils.set_title("Getting usd prices...")
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
    print("")

    # check balance
    if check_eth:
        utils.set_title("Checking ETH")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(depth),
                repeat(input_type),
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["eth"]),
                repeat("eth"),
            )

    if check_btc:
        utils.set_title("Checking BTC")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(depth),
                repeat(input_type),
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["btc"]),
                repeat("btc"),
            )

    if check_ltc:
        utils.set_title("Checking LTC")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(depth),
                repeat(input_type),
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["ltc"]),
                repeat("ltc"),
            )

    if check_doge:
        utils.set_title("Checking DOGE")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(depth),
                repeat(input_type),
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["doge"]),
                repeat("doge"),
            )

    if check_dash:
        utils.set_title("Checking DASH")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                get_balance,
                mnemonics,
                repeat(depth),
                repeat(input_type),
                repeat(proxy_list),
                repeat(proxy_type),
                repeat(usd_prices["dash"]),
                repeat("dash"),
            )
