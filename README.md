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

## Library usage

```python
import asyncio
from roombapy import RoombaClient


async def main() -> None:
    async with RoombaClient("192.168.1.50", blid, password) as robot:
        robot.register_on_message_callback(print)
        await robot.send_command("start")
        await asyncio.sleep(60)


asyncio.run(main())
```

`connect()` either establishes a session or raises. Losing it afterwards is
the library's problem, not yours: a supervised reconnect with exponential
backoff runs until `disconnect()`. Register with
`register_on_connection_state_callback` to reflect availability.

A rejected credential is the exception — `RoombaAuthError` stops the
supervisor, because a wrong password does not become right by retrying.

### Typed state, if you want it

`master_state` stays `dict[str, Any]`, exactly as before. Alongside it,
`reported` is a typed view of the same dictionary — no parsing, no copy:

```python
robot.reported.get("cleanMissionStatus", {}).get("phase")  # checked by mypy
robot.master_state["state"]["reported"]  # unchanged, still Any
```

`reported` is empty until the robot's first MQTT message arrives, so index
it with `.get()` rather than `[]` right after `connect()` — the fields
themselves are typed, but their presence is not guaranteed until a message
has been received. Coverage is also deliberately partial beyond that: a key
that is not declared is simply not typed, which is the right outcome for
firmware-specific fields.

## Live position (newer robots)

900-series robots publish their position into the shadow. Newer ones do
not — they answer when asked, over a request/response channel that
nobody had documented until field captures from four robots across three
firmware families settled it.

```python
# One reading
pose = await client.get_position()
if pose is not None:
    print(pose.x, pose.y, pose.theta)  # metres, metres, radians

# A stream
async for pose in client.watch_position():
    print(pose.x, pose.y)
```

**One stream, both generations.** `watch_position()` polls where it has
to and reads the shadow where it can: a 900-series publishes its
position, so it is never asked for one. `RobotPosition` is always
**metres and radians**, origin at the dock, x-axis along the direction
the robot faces when docked — a consumer does not need to know which
generation it has.

`pose.source` says anyway, because the cost differs: listening to a
shadow is free, while every requested pose is a round trip.

This is a different thing from `watch()`, which yields raw shadow
messages — everything the robot reports, unparsed. `watch_position()`
yields one kind of thing, already interpreted, and only when there is
one.

Three things worth knowing before building on it:

- **`get_position()` returns `None` when the robot has no fix.** That is
  a real state, not a failure — a Braava jet m6 answered that way for a
  whole mission while a vacuum on the same account returned coordinates.
- **`theta` wraps at π.** A field capture went from `3.06` to `-2.63`
  across one turn. Anything computing heading deltas has to handle it;
  the library reports what arrived rather than normalising.
- **`watch_position()` raises `RrtpUnsupportedError`** after repeated
  silence. Older generations do not implement the request, and an empty
  stream would look like a finished mission instead of an unsupported
  robot.

The default poll interval is 1 Hz. 2 Hz was verified — 100 of 100
requests answered on a moving robot — but that was a stress test, and a
77-minute mission at that rate is roughly 9,200 requests against 4,600.
At 1 Hz the point spacing is around 125 mm, comparable to the 132 mm a
900-series publishes unprompted.

**One poller serves every watcher**, at the shortest interval any of
them asked for. A second caller asking for a faster rate restarts it;
when that caller leaves, it drops back. The robot allows one local
connection, so two callers running their own loops would double its
load without either noticing.

Do **not** gate any of this on `cap.pose`. Neither the firmware nor the
vendor app ever compares that value, and lewis hard-codes it to 2;
support is established by asking and handling silence.

## Upgrading from 1.x

Version 2 is asynchronous throughout, and breaking.

| 1.x | 2.0 |
|---|---|
| `RoombaFactory.create_roomba(...)` | `RoombaClient(address, blid, password)` |
| `Roomba(remote_client, continuous=…, delay=…)` | `RoombaClient(...)`; `continuous`/`delay` are gone |
| `RoombaRemoteClient` | internal; construct `RoombaClient` directly |
| `roomba.connect()` / `.disconnect()` | `await` them |
| `.send_command()` / `.set_preference()` | `await` them |
| `roomba.roomba_connected` | `robot.connected` |
| `RoombaDiscovery().get_all()` | `await` it; takes a `timeout` |
| `RoombaPassword(ip).get_password()` | `await` it; takes a `timeout` |
| `periodic_connection()`, `stop_connection` | removed with the thread |

`master_state`, the state machine and every constant table are unchanged.

Two behaviour changes worth knowing before you upgrade:

- **Authentication failures raise.** In 1.x a rejected password arrived via
  `on_connect` and merely left `roomba_connected` False, so callers polled a
  flag. `connect()` now raises `RoombaAuthError`.
- **Room-scoped commands are checked.** `send_command("start", {"regions":
  []})` raises `RoombaScopeError`. An empty list does not mean "no rooms" to
  the robot — it means the key is omitted and the whole house is cleaned.
  Omit `regions` entirely if that is what you want.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and packaging.

If you have [Nix](https://nixos.org) with flakes enabled, the quickest way to get a full
dev environment (uv, a matching Python interpreter, and mosquitto for the integration
tests) is:

```shell
nix develop
```

Otherwise, install [uv](https://docs.astral.sh/uv/getting-started/installation/) yourself
and run:

```shell
uv sync --all-extras --dev
```

To improve your development experience, you can install pre-commit hooks via the following command.
With every commit it will run a set of checks, making sure it meets the quality standards.

```shell
uv run pre-commit install
```

Run the test suite with:

```shell
uv run pytest
```
