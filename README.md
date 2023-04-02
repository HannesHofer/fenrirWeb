[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
# Fenrir routing service

## Introduction
Fenrir provides a user friendly way to route all traffic from configured trough a VPN tunnel.

FenrirWeb is a webinterface for viewing/ configuring fenrir.
Configuration is stored in `/var/cache/fenrir/fenrir.db`

## Installation
Fenrir is a pure python3 application. (3.6+)

### pip releases
```sh
> pip install fenrirweb
> fenrirweb --help
```
# Usage
Usage is documented in integrated help module.
```sh
> fenrir --help
```
## examples
### run fenrir web in debug mode
```sh
fenrirweb --debug
```
