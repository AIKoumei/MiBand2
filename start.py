# import sys
# import time
# import argparse
# from datetime import datetime
# from base import MiBand2
# from constants import ALERT_TYPES


# parser = argparse.ArgumentParser()
# parser.add_argument('-s', '--standard',  action='store_true',help='Shows device information')
# parser.add_argument('-r', '--recorded',  action='store_true',help='Shows previews recorded data')
# parser.add_argument('-l', '--live',  action='store_true',help='Measures live heart rate')
# parser.add_argument('-i', '--init',  action='store_true',help='Initializes the device')
# parser.add_argument('-m', '--mac', required=True, help='Mac address of the device')
# parser.add_argument('-t', '--set_current_time', action='store_true',help='Set time')
# args = parser.parse_args()


# MAC = args.mac # sys.argv[1]

# band = MiBand2(MAC, debug=True)
# band.setSecurityLevel(level="medium")


# band.send_alert(ALERT_TYPES.NONE)
# time.sleep(3)
# band.send_alert(ALERT_TYPES.MESSAGE)

# band.disconnect()
