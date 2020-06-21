from typing import List
from dataclasses import dataclass
from collections import namedtuple

import iperf3

from db import tresults
from wifi import AccessPoint, MIN_POWER, MAX_COUNT


DURATION = 3
T_OUTPUT = 1
T_INPUT = 2


def get_public_servers() -> List:
    return [('speedtest.hostkey.ru', 5203), ]


TestedAP = namedtuple('TestedAP', 'ap sent_in received_in sent_out received_out')


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


def main(min_power, max_count):
    srv, port = get_public_servers()[0]
    bw = Bandwidth(srv, port)
    tested_ap = []
    for ap in AccessPoint.list_better(min_power=min_power, max_count=max_count):
        ap.up()
        print('Test ', ap.ssid, ap.signal_value)

        tr_i = bw.input()
        tresults.insert(type=T_INPUT, json=tr_i.text, sig_value=ap.signal_value, ssid=ap.ssid)
        print('Input: ', tr_i.sent_Mbps, tr_i.received_Mbps)

        tr_o = bw.output()
        tresults.insert(type=T_OUTPUT, json=tr_o.text, sig_value=ap.signal_value, ssid=ap.ssid)
        print('Output: ', tr_o.sent_Mbps, tr_o.received_Mbps)

        tested_ap.append(TestedAP(ap, tr_i.sent_Mbps, tr_i.received_Mbps, tr_o.sent_Mbps, tr_o.received_Mbps))

    _ap, *speed = sorted(tested_ap, reverse=True, key=lambda tap: tap.sent_in + tap.received_in)[0]
    if _ap is not ap:
        print('Activate ', _ap.ssid, _ap.signal_value)
        _ap.up()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-mp', '--min-power', type=int, default=MIN_POWER)
    parser.add_argument('-mc', '--max-count', type=int, default=MAX_COUNT)
    args = parser.parse_args()

    main(args.min_power, args.max_count)