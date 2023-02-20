import requests
import sys

FPGA = sys.argv[1]

FPGA = FPGA[:-2]

url = 'https://www.xilinx.com/support/packagefiles/' + FPGA[3] + '7packages/' + FPGA + 'pkg.txt'
filename = sys.argv[2] + "pinout.txt"
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)
