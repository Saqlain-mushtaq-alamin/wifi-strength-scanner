import subprocess
import re


class WifiScanner:
    NETSH_CMD = ["netsh", "wlan", "show", "interfaces"]

    @staticmethod
    def scan():
        """
        Runs 'netsh wlan show interfaces' and extracts useful WiFi data.
        Returns:
            dict with keys: ssid, bssid, signal, radio, channel
        """
        try:
            output = subprocess.check_output(
                WifiScanner.NETSH_CMD, shell=True, text=True, encoding="utf-8"
            )
        except Exception as e:
            raise RuntimeError("Failed to run netsh command") from e

        return WifiScanner.parse_output(output)

    @staticmethod
    def parse_output(text):
        """
        Parses NETSH output using regex.
        """
        data = {}

        patterns = {
            "ssid": r"SSID\s*:\s*(.*)",
            "bssid": r"BSSID\s*:\s*(.*)",
            "rssi": r"Rssi\s*:\s*(-?\d+)",
            "signal": r"Signal\s*:\s*(\d+)%",   # returns percent
            "radio": r"Radio type\s*:\s*(.*)",
            "channel": r"Channel\s*:\s*(\d+)",
            "band": r"Band\s*:\s*(\d+GHz)"

        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                data[key] = match.group(1).strip()
            else:
                data[key] = None

        # Convert signal to integer
        if data["signal"] and data["rssi"]:
            data["signal"] = int(data["signal"])
            data["rssi"] = int(data["rssi"])

        return data
