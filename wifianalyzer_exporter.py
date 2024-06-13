import argparse
import time
from prometheus_client import start_http_server, Gauge
from wifi_manger import WifiManager

# Define Prometheus metrics
wifi_ap_info = Gauge(
    "wifi_ap_info",
    "Information about available Wi-Fi APs",
    [
        "ssid",
        "bssid",
        "mode",
        "channel",
        "frequency",
        "rate",
        "bandwidth",
        "security",
        "wpa_flags",
        "rsn_flags",
        "device",
        "active",
    ],
)


def scan_wifi():

    wm = WifiManager()
    scan_results = wm.scan_oneshot()

    return scan_results


def collect_wifi_data():
    scan_results = scan_wifi()

    for ap in scan_results:
        wifi_ap_info.labels(
            ssid=ap["ssid"],
            bssid=ap["bssid"],
            mode=ap["mode"],
            channel=ap["channel"],
            frequency=ap["frequency"],
            rate=ap["rate"],
            bandwidth=ap["bandwidth"],
            security=ap["security"],
            wpa_flags=ap["wpa-flags"],
            rsn_flags=ap["rsn-flags"],
            device=ap["device"],
            active=ap["active"],
        ).set(ap["signal"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prometheus exporter for WiFi access points using wifi_wrapper."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9106,
        help="Port to expose metrics on (default: 9106)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Time interval in seconds between scans (default: 30)",
    )
    parser.add_argument(
        "--listen-address",
        type=str,
        default="0.0.0.0",
        help="Listen address (default: 0.0.0.0)",
    )

    args = parser.parse_args()

    print(f"Started wifianalyzer_exporter {args.listen_address}:{args.port}")
    print(f"Interval between scans: {args.interval} seconds")

    # Start the Prometheus HTTP server
    start_http_server(port=args.port, addr=args.listen_address)

    # Continuously collect and update Wi-Fi data
    while True:
        collect_wifi_data()
        time.sleep(args.interval)  # Adjust the sleep interval as needed
