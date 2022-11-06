import simulator.simulator as simulator
import math
import argparse

parser = argparse.ArgumentParser(description="Discrete M/M/K queue simulator")

parser.add_argument("--rho", type=float, default=0.95)
parser.add_argument("--packet_length", type=int, default=2000)
parser.add_argument("--service_rate", type=float, default=1e6)
parser.add_argument("--queue_size", type=int, default=math.inf)
parser.add_argument("--simulation_time", type=int, default=2000)

args = parser.parse_args()

service_rate = args.service_rate
avg_packet_length = args.packet_length
rho = args.rho
queue_size = args.queue_size
simulation_time = args.simulation_time

print(simulator.simulate(rho, service_rate, avg_packet_length, simulation_time, queue_size))