import subprocess
from utils import run_command
import argparse


class WifiManager:
    def __init__(self, filter_ssid=None) -> None:
        self.filter_ssid = filter_ssid

    def __process_scan_results(self, results: str) -> list:
        output = []
        rows = results.split("\n")

        for row in rows:
            # discard the last empty row
            if not row:
                continue

            # extract the ssid
            # 00:00:00:00:00:00 :17 characters
            bssid = row[:17]
            row = row[18:]
            row = row.split(":")

            ssid = row[0]

            if self.filter_ssid is not None:
                if self.filter_ssid not in ssid:
                    continue

            output.append({
                'ssid': ssid,
                'bssid': bssid,
                'mode': row[1],
                'channel': row[2],
                'frequency': row[3],
                'rate': row[4],
                'bandwidth': row[5],
                'signal': 0 - int(row[6]),
                'security': row[7],
                'wpa-flags': row[8],
                'rsn-flags': row[9],
                'device': row[10],
                'active': row[11]
            })
        return output

    def scan_oneshot(self) -> list:
        output_bytes = run_command("nmcli --terse --escape no --fields \
            BSSID,SSID,MODE,CHAN,FREQ,RATE,BANDWIDTH,SIGNAL,SECURITY,WPA-FLAGS,RSN-FLAGS,DEVICE,ACTIVE \
            device wifi \
            ")
        output_str = output_bytes.decode()

        return self.__process_scan_results(output_str)


def main():
    parser = argparse.ArgumentParser(description='Wifi Analyzer Exporter')
    parser.add_argument('--filter-ssid', metavar='SSID',
                        help='Monitor only this selected SSID (Optional).')

    args = parser.parse_args()

    wa = WifiManager(filter_ssid=args.filter_ssid)
    print(wa.scan_oneshot())


if __name__ == '__main__':
    main()
