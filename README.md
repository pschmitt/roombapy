# roombapy

[![CI](https://github.com/pschmitt/roombapy/actions/workflows/ci.yaml/badge.svg)](https://github.com/pschmitt/roombapy/actions/workflows/ci.yaml)
[![PyPI](https://img.shields.io/pypi/v/roombapy)](https://pypi.org/project/roombapy/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/roombapy)](https://pypi.org/project/roombapy/)
[![PyPI - License](https://img.shields.io/pypi/l/roombapy)](./LICENSE)

Unofficial iRobot Roomba python library (SDK).

Fork of [NickWaterton/Roomba980-Python](https://github.com/NickWaterton/Roomba980-Python)

This library was created for the [Home Assistant Roomba integration](https://www.home-assistant.io/integrations/roomba/).

## Installation

```shell
pip install roombapy[cli]
```

# Notes

This library is only for firmware 2.x.x [Check your robot version!](http://homesupport.irobot.com/app/answers/detail/a_id/529)

Only local connections are supported.

## How to discover your robots and obtain credentials

```shell
roombapy discover <optional ip address>
```
This will find your Roomba in local network, and obtain credentials _automagically_ whether possible.

## Event stream

To get event stream from iRobot, use:

```shell
roombapy connect <ip> -p <password>
```

Output is suitable for piping into tools like `jq`.

## Development

To improve your development experience, you can install pre-commit hooks via the following command.
With every commit it will run a set of checks, making sure it meets the quality standards.

```shell
pre-commit install
```
