# Seed Checker

## Supported Chains
- [x] ETH
- [x] BTC
- [x] LTC
- [x] Doge
- [x] Dash

## Installation
- pip install -r requirements.txt
- python3 main.py
- В proxy.txt добавить ваши прокси в формате ip:port или username:password@ip:port
- В input.txt добавить то, что вы будете чекать - адреса, сидки или приватный ключи

## Settings
- Что-бы настроить софт откройте settings.ini текстовым редактором
- threads - number of threads (don't use too many, 50 threads maximum)
- proxy_type - socks5 or http (ipv4 required)
- input_type - что вы будете чекать (address/seeds/privkeys)
- CHAINS - какие сети чекать (yes/no)