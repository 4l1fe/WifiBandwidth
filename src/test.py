from typing import List
from  dataclasses import dataclass
from datetime import datetime, timedelta

import iperf3

from db import tresults


DURATION = 3
T_OUTPUT = 1
T_INPUT = 2


def utc_timestamp(timesecs):
    return datetime.fromtimestamp(timesecs) - timedelta(hours=7)


def get_public_servers() -> List:
    return [('iperf.volia.net', 5201), ]
    # return [('iperf.worldstream.nl', 5201), ]
    # return [('iperf.biznetnetworks.com', 5201), ]


def get_wifi_networks() -> List:
    return []


@dataclass
class Bandwidth:
    server: str
    port: int
    duration: int = DURATION

    def output(self) -> iperf3.TestResult:
        return self._run(False)

    def input(self) -> iperf3.TestResult:
        return self._run(True)

    def _make_client(self):
        cl = iperf3.Client()
        cl.server_hostname = self.server
        cl.port = self.port
        cl.duration = self.duration
        return cl

    def _run(self, reverse) -> iperf3.TestResult:
        cl = self._make_client()
        cl.reverse = reverse
        result = cl.run()
        if result.error:
            raise ValueError(result.error)
        return result


def main():
    srv, port = get_public_servers()[0]
    # get_wifi_networks()
    bw = Bandwidth(srv, port)

    tr_o = bw.output()
    tresults.insert(type=T_OUTPUT, json=tr_o.text, uts_timestamp=utc_timestamp(tr_o.timesecs),
                    sent=tr_o.sent_MB_s, received=tr_o.received_MB_s)

    tr_i = bw.input()
    tresults.insert(type=T_INPUT, json=tr_i.text, uts_timestamp=utc_timestamp(tr_i.timesecs),
                    sent=tr_o.sent_MB_s, received=tr_o.received_MB_s)


if __name__ == '__main__':
    main()