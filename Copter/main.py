import sys
import flight_lib as fl

lat, lon = float(sys.argv[1]), float(sys.argv[2])
self_lat, self_lon = fl.get_coordinates()

fl.take_off()
fl.goto(lat, lon)
fl.throw_off()
fl.goto(self_lat, self_lon)
fl.land()
