import time
import threading

class Valve:
    def __init__(self, name, open_tag, open_fb_tag, close_fb_tag, plc_io):
        self.name = name
        self.open_tag = open_tag
        self.open_fb_tag = open_fb_tag
        self.close_fb_tag = close_fb_tag
        self.plc_io = plc_io
        self.last_command = False

    def simulate_behavior(self):
        try:
            open_cmd = self.plc_io.read_tag(self.open_tag)

            if open_cmd and not self.last_command:
                # Rising edge: command to open
                print(f"{self.name}: Open command detected.")
                threading.Thread(target=self._simulate_open).start()

            elif not open_cmd and self.last_command:
                # Falling edge: command to close
                print(f"{self.name}: Close command detected.")
                threading.Thread(target=self._simulate_close).start()

            self.last_command = open_cmd
        except Exception as e:
            print(f"[{self.name}] simulate_behavior error: {e}")

    def _simulate_open(self):
        time.sleep(0.3)  # simulate delay
        self.plc_io.write_tag(self.open_fb_tag, True)
        self.plc_io.write_tag(self.close_fb_tag, False)
        print(f"{self.name}: Opened - Feedback updated.")

    def _simulate_close(self):
        time.sleep(0.3)  # simulate delay
        self.plc_io.write_tag(self.open_fb_tag, False)
        self.plc_io.write_tag(self.close_fb_tag, True)
        print(f"{self.name}: Closed - Feedback updated.")