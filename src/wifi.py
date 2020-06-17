from subprocess import run


MIN_POWER = 60
MAX_COUNT = 4


class AccessPoint:
    LIST_CMD = 'nmcli dev wifi list'.split()
    UP_CMD = 'nmcli connection up'.split()

    def __init__(self, signal_value, ssid):
        self.signal_value = signal_value
        self.ssid = ssid

    @staticmethod
    def list_better(min_power=MIN_POWER, max_count=MAX_COUNT):
        cproc = run(AccessPoint.LIST_CMD, text=True, capture_output=True)
        lines = cproc.stdout.splitlines()
        sig_idx = lines[0].index('SIGNAL')
        ssid_idx_s = lines[0].index('SSID')
        ssid_idx_e = lines[0].index('MODE')
        access_points = []
        for count, line in enumerate(lines[1:], start=1):
            sig_value = int(line[sig_idx: sig_idx + 3])
            ssid_value = line[ssid_idx_s: ssid_idx_e].strip()
            if sig_value >= min_power:
                access_points.append(AccessPoint(sig_value, ssid_value))
            if count >= max_count:
                break

        return access_points

    def up(self):
        cproc = run(AccessPoint.UP_CMD + [self.ssid, ], text=True, capture_output=True)

    def down(self):
        pass
