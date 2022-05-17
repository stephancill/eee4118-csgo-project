from distutils.command.clean import clean
import telnetlib
import time

HOST = "127.0.0.1"
PORT = 2121
welcome = "CSGO Remote Console Online"
endl = "\n"

class CSGOTelnetClient:
    def __init__(self, host=None, port=None):
        self.host = host or HOST
        self.port = port or PORT
        self.tn = None

    def connect(self):
        self.tn = telnetlib.Telnet(self.host, self.port)
        self.tn.write(str.encode("echo " + welcome + endl))
        self.tn.read_until(b"Online")
        print("Successfully Connected")
    
    def run(self, command):
        print ("running: ", command)
        self.tn.write(str.encode("echo Remote Command: " + command + endl))
        self.tn.write(str.encode(command + endl))
        time.sleep(0.05)

if __name__ == "__main__":
    client = CSGOTelnetClient()
    client.connect()
    client.run("kill")