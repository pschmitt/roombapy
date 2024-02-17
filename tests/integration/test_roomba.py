from tests.conftest import get_message


def test_roomba_with_data(roomba):
    roomba.on_message(
        None,
        None,
        get_message(
            "topic",
            b'{"state":{"reported":{"cleanSchedule":{"cycle":["none",'
            b'"none","none","none","none","none","none"],"h":'
            b'[9,11,11,11,11,11,9],"m":[0,0,0,0,0,0,0]},"language":0'
            b',"cleanMissionStatus":{"cycle":"none","phase":"charge",'
            b'"expireM":0,"rechrgM":0,"error":0,"notReady":0,"mssnM":108'
            b',"sqft":0,"initiator":"","nMssn":209},"dock":{"known":true}'
            b',"bin":{"present":true,"full":false},"batteryType":"lith",'
            b'"batPct":100,"mobilityVer":"7375","bootloaderVer":"36",'
            b'"soundVer":"13"}}}',
        ),
    )
    roomba.on_message(
        None,
        None,
        get_message(
            "topic",
            b'{"state":{"reported":{"signal":{"rssi":-38,"snr":52}}}}',
        ),
    )

    state = roomba.master_state

    assert state
    assert state["state"]["reported"]["bin"]["present"]
    assert not state["state"]["reported"]["bin"]["full"]
    assert state["state"]["reported"]["batPct"] == 100
