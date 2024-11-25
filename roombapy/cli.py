"""CLI to manage Roomba vacuums and mops."""

from __future__ import annotations

import sys
import time
from collections import deque
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from collections.abc import Iterable

import orjson

from roombapy import (
    RoombaConnectionError,
    RoombaDiscovery,
    RoombaFactory,
    RoombaInfo,
    RoombaMessage,
    RoombaPassword,
)

try:
    import click
    from tabulate import tabulate
except ImportError:
    print("Roombapy CLI requires 'click' and 'tabulate' dependencies")  # noqa: T201
    print("Install roombapy[cli] instead of just roombapy")  # noqa: T201
    sys.exit(1)

PLACEHOLDER = "-"


def _repr_bots(bots: Iterable[RoombaInfo], *, raw: bool = False) -> str:
    if raw:
        return "\n".join([str(bot) for bot in bots])
    headers = ["Robot name", "IP", "MAC", "BLID", "Password"]
    table = [
        [bot.robot_name, bot.ip, bot.mac, bot.blid, bot.password]
        for bot in bots
    ]
    alignment = ("center", "left", "left", "left", "center")
    return tabulate(
        tabular_data=table,
        headers=headers,
        tablefmt="mixed_grid",
        colalign=alignment,
    )


def _comma_and(iterable: list[str]) -> str:
    parts = ", ".join(iterable[:-1])
    if parts:
        parts += " and " + iterable[-1]
    else:
        parts = iterable[0]
    return parts


@click.group()
def cli() -> None:
    """CLI to manage Roomba vacuums and mops."""


@cli.command()
@click.argument(
    "ip",
    type=str,
    required=False,
)
@click.option(
    "-r",
    "--raw",
    is_flag=True,
    help="Display raw output",
    required=True,
    default=False,
)
def discover(ip: str | None, *, raw: bool) -> None:
    """Discover Roomba devices on the local network."""
    roomba_discovery = RoombaDiscovery()
    discovered = []
    if ip is not None:
        if bot := roomba_discovery.get(ip):
            discovered = [bot]
    else:
        discovered = list(roomba_discovery.get_all())

    for bot in discovered:
        if password := RoombaPassword(bot.ip).get_password():
            bot.password = password
        else:
            bot.password = PLACEHOLDER

    if discovered:
        click.echo("Discovered robots:")
        click.echo(_repr_bots(discovered, raw=raw))

        if passwordless_bots := [
            bot for bot in discovered if bot.password == PLACEHOLDER
        ]:
            names = _comma_and([bot.robot_name for bot in passwordless_bots])
            click.echo(f"Note: Password for {names} couldn't be obtained.")
    else:
        click.echo("No robots found.")


@cli.command()
@click.argument(
    "ip",
    type=str,
    required=True,
)
@click.option(
    "-b",
    "--blid",
    type=str,
    required=False,
    help="Robot BLID (login)",
)
@click.option(
    "-p",
    "--password",
    type=str,
    required=False,
    help="Robot password",
)
@click.option(
    "-d",
    "--debounce",
    type=int,
    required=False,
    default=0,
    help="Debounce similar N messages",
)
def connect(
    ip: str, blid: str | None, password: str | None, debounce: int = 0
) -> None:
    """Connect to a Roomba device."""
    # Discover BLID/password, if possible
    login: str | None
    if bot := RoombaDiscovery().get(ip):
        if obtained_password := RoombaPassword(bot.ip).get_password():
            bot.password = obtained_password
        # Explicitly supplied credentials take precedence over discovered ones
        login = blid or bot.blid
        password = password or bot.password
    else:
        login = blid

    # To avoid connection error with MQTT server inside roomba
    time.sleep(1)

    if not all((login, password)):
        click.echo(f"There are no credentials for {ip}", err=True)
        # Add hint how to obtain password here
        click.echo(f"Use roombapy connect {ip} -b <blid> -p <password>")
        sys.exit(1)
    if password is None:
        click.echo(f"Missing password for {ip}", err=True)
        # Add hint how to obtain password here
        click.echo(f"Use roombapy connect {ip} -p <password>")
        sys.exit(1)
    if login is None:
        click.echo(f"Missing blid for {ip}", err=True)
        # How this even possible?
        click.echo(f"Use roombapy connect {ip} -b <blid> -p {password}")
        sys.exit(1)

    roomba = RoombaFactory.create_roomba(ip, login, password)

    def printer(buffer_size: int) -> Callable[[RoombaMessage], None]:
        buffer: deque[bytes] = deque(maxlen=buffer_size)

        def inner(message: RoombaMessage) -> None:
            serialized = orjson.dumps(message)
            if serialized not in set(buffer):
                click.echo(serialized)
            buffer.append(serialized)

        return inner

    roomba.register_on_message_callback(printer(debounce))
    try:
        roomba.connect()
    except RoombaConnectionError:
        sys.exit(1)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Graceful shutdown
        roomba.disconnect()
    finally:
        sys.exit(0)


if __name__ == "__main__":
    cli()
