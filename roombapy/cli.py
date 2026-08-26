"""CLI to manage Roomba vacuums and mops.

Same commands and output as version 1, driven by the async client. The
busy-wait in ``connect`` is gone: it blocks on an event instead of spinning.
"""

from __future__ import annotations

import asyncio
import sys
from collections import deque
from typing import TYPE_CHECKING

import orjson

from roombapy.discovery import RoombaDiscovery
from roombapy.getpassword import RoombaPassword
from roombapy.roomba import RoombaClient, RoombaConnectionError

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from roombapy.roomba_info import RoombaInfo
    from roombapy.state import RoombaMessage

try:
    import click
    from tabulate import tabulate
except ImportError:  # pragma: no cover - matches the sync CLI
    sys.stderr.write(
        "Roombapy CLI requires 'click' and 'tabulate' dependencies\n"
        "Install roombapy[cli] instead of just roombapy\n"
    )
    sys.exit(1)


PLACEHOLDER = "-"


def _repr_bots(bots: Iterable[RoombaInfo], *, raw: bool = False) -> str:
    """Render discovered robots as a table, or raw if asked."""
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
    """Join names as "a, b and c"."""
    parts = ", ".join(iterable[:-1])
    if parts:
        parts += " and " + iterable[-1]
    else:
        parts = iterable[0]
    return parts


async def _discover(ip: str | None) -> list[RoombaInfo]:
    """Find robots, then fill in each password."""
    discovery = RoombaDiscovery()
    try:
        if ip is not None:
            bot = await discovery.get(ip)
            discovered = [bot] if bot else []
        else:
            discovered = list(await discovery.get_all())
    finally:
        await discovery.aclose()

    passwords = await asyncio.gather(
        *(RoombaPassword(bot.ip).get_password() for bot in discovered)
    )
    for bot, password in zip(discovered, passwords, strict=True):
        bot.password = password or PLACEHOLDER
    return discovered


@click.group()
def cli() -> None:
    """CLI to manage Roomba vacuums and mops."""


@cli.command()
@click.argument("ip", type=str, required=False)
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
    discovered = asyncio.run(_discover(ip))

    if not discovered:
        click.echo("No robots found.")
        return

    click.echo("Discovered robots:")
    click.echo(_repr_bots(discovered, raw=raw))

    if passwordless := [b for b in discovered if b.password == PLACEHOLDER]:
        names = _comma_and([bot.robot_name for bot in passwordless])
        click.echo(f"Note: Password for {names} couldn't be obtained.")


def _printer(buffer_size: int) -> Callable[[RoombaMessage], None]:
    buffer: deque[bytes] = deque(maxlen=buffer_size)

    def inner(message: RoombaMessage) -> None:
        serialized = orjson.dumps(message)
        if serialized not in set(buffer):
            click.echo(serialized)
        buffer.append(serialized)

    return inner


async def _connect(
    ip: str, blid: str | None, password: str | None, debounce: int
) -> int:
    """Resolve credentials, stream messages until interrupted."""
    login = blid
    discovery = RoombaDiscovery()
    try:
        bot = await discovery.get(ip)
    finally:
        await discovery.aclose()

    if bot is not None:
        if obtained := await RoombaPassword(bot.ip).get_password():
            bot.password = obtained
        login = blid or bot.blid
        password = password or bot.password

    if password is None:
        click.echo(f"Missing password for {ip}", err=True)
        click.echo(f"Use roombapy connect {ip} -p <password>")
        return 1
    if login is None:
        click.echo(f"Missing blid for {ip}", err=True)
        click.echo(f"Use roombapy connect {ip} -b <blid> -p {password}")
        return 1

    client = RoombaClient(ip, login, password)
    client.register_on_message_callback(_printer(debounce))
    try:
        await client.connect()
    except RoombaConnectionError as err:
        click.echo(str(err), err=True)
        return 1

    try:
        # Block until interrupted; no polling.
        await asyncio.Event().wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        await client.disconnect()
    return 0


@cli.command()
@click.argument("ip", type=str, required=True)
@click.option("-b", "--blid", type=str, required=False, help="Robot BLID")
@click.option(
    "-p", "--password", type=str, required=False, help="Robot password"
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
    sys.exit(asyncio.run(_connect(ip, blid, password, debounce)))


if __name__ == "__main__":
    cli()
