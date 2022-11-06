from .helpers import random_variable as rv
import math
from collections import deque

ARRIVAL = "Arrival"
DEPARTURE = "Departure"
OBSERVER = "Observer"

def simulate(rho, service_rate, avg_packet_len, total_duration, queue_size = math.inf):
    arrival_rate = service_rate * rho / avg_packet_len
    packets = []
    prev_arrival_time = 0

    # pregenerate arrival and departure events regardless of queue size
    while prev_arrival_time < total_duration:
        arrival_time = rv.get_exponential_rv(arrival_rate) + prev_arrival_time
        packet_length = rv.get_exponential_rv(1 / avg_packet_len)
        service_time = packet_length / service_rate

        packets.append((arrival_time, service_time))
        prev_arrival_time = arrival_time
    
    q = deque()
    departures = []
    arrivals_not_dropped = []

    num_arrivals, num_departures, num_generated = 0, 0, 0
    loss_count = 0
    prev_departure_time = 0

    # simulate packets that actually arrive based on queue size
    for p in packets:
        arrival_time = p[0]
        if arrival_time > total_duration:
            break
    
        while q and prev_departure_time < arrival_time:
            packet = q.popleft()
            departure_time = packet[0] + packet[1] if not q else prev_departure_time + packet[1]
            departures.append(departure_time)
            num_departures += 1
            prev_departure_time = departure_time
        
        if num_arrivals - num_departures < queue_size:
            num_arrivals += 1
            num_generated += 1
            q.append(p)
            arrivals_not_dropped.append(arrival_time)
        else:
            num_generated += 1
            loss_count += 1
    
    # experimentally found observer rate that can sufficiently monitor the simulation
    observe_multiplier = 5
    prev_observe_time = 0
    observers = []
    while prev_observe_time < total_duration:
        observe_time = rv.get_exponential_rv(observe_multiplier * arrival_rate) + prev_observe_time
        observers.append(observe_time)
        prev_observe_time = observe_time
    
    events = []
    for a in arrivals_not_dropped:
        events.append((ARRIVAL, a))
    for d in departures:
        events.append((DEPARTURE, d))
    for o in observers:
        events.append((OBSERVER, o))
    
    events.sort(key= lambda e: e[1])

    num_arrivals, num_departures, num_observers = 0, 0, 0
    in_queue, idle_count = 0, 0

    for eventType, _ in events:
        if eventType == OBSERVER:
            num_observers += 1
            if num_arrivals == num_observers:
                idle_count += 1
            else:
                in_queue += num_arrivals - num_departures
        elif eventType == ARRIVAL:
            num_arrivals += 1
        elif eventType == DEPARTURE:
            num_departures += 1
    
    # calculate metrics to return
    avg_packets_in_queue = in_queue / num_observers
    idle_rate = idle_count / num_observers
    loss_rate = loss_count / num_generated

    return avg_packets_in_queue, idle_rate, loss_rate