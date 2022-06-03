#!/usr/bin/env python3

import mercury

def stats_received(stats):
    print({"temp" : stats.temperature})
    print({"antenna" : stats.antenna})
    print({"protocol" : stats.protocol})
    print({"frequency" : stats.frequency})

reader = mercury.Reader("tmr:///dev/ttyUSB1")

reader.set_region("EU3")
reader.set_read_plan(antennas=[1], protocol="GEN2", bank=["epc"], read_power=2000)

reader.enable_stats(stats_received)
reader.start_reading(lambda tag: print(tag.epc))
input("Press Enter to continue...")
reader.stop_reading()
