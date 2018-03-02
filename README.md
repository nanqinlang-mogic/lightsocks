# lightsocks-nanqinlang
[![Build Status](https://github.com/nanqinlang/SVG/blob/master/build%20passing.svg)](https://github.com/nanqinlang/lightsocks-nanqinlang)
[![language](https://github.com/nanqinlang/SVG/blob/master/language-python-blue.svg)](https://github.com/nanqinlang/lightsocks-nanqinlang)
[![author](https://github.com/nanqinlang/SVG/blob/master/author-nanqinlang-lightgrey.svg)](https://github.com/nanqinlang/lightsocks-nanqinlang)

A modified version, based on `Python 3.6 asyncio` environment.

origin： https://github.com/linw1995/lightsocks-python

## environment
requires for `typing`, run this following to install dependences:
```bash
pip install -r requirements.txt
```

## usage
there are the steps to use this proxy:
### server
the server file is `~/ls/lsserver.py`
```bash
$ python lsserver.py -h
usage: lsserver.py [-h] [--version] [--save CONFIG] [-c CONFIG]
                   [-s SERVER_ADDR] [-p SERVER_PORT] [-k PASSWORD] [--random]

A light tunnel proxy that helps you bypass firewalls

optional arguments:
  -h, --help      show this help message and exit
  --version       show version information

Proxy options:
  --save CONFIG   path to dump config
  -c CONFIG       path to config file
  -s SERVER_ADDR  server address, default: 0.0.0.0
  -p SERVER_PORT  server port, default: 443
  -k PASSWORD     password
  --random        generate a random password to use
```
```bash
$ python lsserver.py --random --save config.json
generate random password
dump config file into 'config.json'
Listen to 0.0.0.0:443

Please use:

lslocal -u "http://hostname:port/#vJjC3tW5l4nG7C3dHZ7hc77cIYrE2q0ikrWQw2MsRa9rqVlDU9vFTF5Hu6PX367kV6qRPU_z-Y_0sio4DAVV-1bmFrfoYoEHmmWkH9L1UDLZqOv8oYvPbe-miAg5Ow58aheFPitEeTX2bmhYC8nQFf1kA5lxpyc0Ljc2W2Du7TESlFIB8aJ7kz-DnczTXcsUv1oYlhpR-AbKf_DI8jMN_tRNdF-szgIJEQrqZ7alvfrNhCCVQNZ-EIIpSOOfXI7nnMC42B48h3egGzBsSpvpaXCNRhME4mEmePd2HFSrD0ty0SUAhjpvTv9BweUZgHrHKLG6Qi-zjLC0JEngI3VmfQ=="

to config lslocal
```

### client
the client file is `~/ls/lslocal.py`
```bash
$ python lslocal.py -h
usage: lslocal.py [-h] [--version] [--save CONFIG] [-c CONFIG] [-u URL]
                  [-s SERVER_ADDR] [-p SERVER_PORT] [-b LOCAL_ADDR]
                  [-l LOCAL_PORT] [-k PASSWORD]

A light tunnel proxy that helps you bypass firewalls

optional arguments:
  -h, --help      show this help message and exit
  --version       show version information

Proxy options:
  --save CONFIG   path to dump config
  -c CONFIG       path to config file
  -u URL          url contains server address, port and password
  -s SERVER_ADDR  server address
  -p SERVER_PORT  server port, default: 443
  -b LOCAL_ADDR   local binding address, default: 127.0.0.1
  -l LOCAL_PORT   local port, default: 1082
  -k PASSWORD     password
```
```bash
$ python lslocal.py -u "http://remoteAddr:remotePort/#password" --save config.json
dump config file into 'config.json'
Listen to 127.0.0.1:1082
```