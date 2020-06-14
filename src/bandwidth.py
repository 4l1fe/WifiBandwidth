from typing import List
from  dataclasses import dataclass
from datetime import datetime, timedelta

import iperf3

from db import tresults
from wifi import AccessPoint


DURATION = 3
T_OUTPUT = 1
T_INPUT = 2


def utc_timestamp(timesecs):
    return datetime.fromtimestamp(timesecs) - timedelta(hours=7)


def get_public_servers() -> List:
    # return [('iperf.volia.net', 5201), ]
    return [('speedtest.wtnet.de', 5201), ]
    # return [('iperf.biznetnetworks.com', 5201), ]


@dataclass
class Bandwidth:
    server: str
    port: int
    duration: int = DURATION

    def output(self):
        return self._run(False)

    def input(self):
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
    for ap in AccessPoint.list_better(max_count=2):
        ap.up()
        print('Test ', ap.ssid, ap.signal_value)

        tr_o = bw.output()
        tresults.insert(type=T_OUTPUT, json=tr_o.text, sig_value=ap.signal_value, ssid=ap.ssid)
        print('Output: ', tr_o.sent_MB_s, tr_o.received_MB_s)

        tr_i = bw.input()
        tresults.insert(type=T_INPUT, json=tr_i.text, sig_value=ap.signal_value, ssid=ap.ssid)
        print('Input: ', tr_i.sent_MB_s, tr_i.received_MB_s)


if __name__ == '__main__':
    main()