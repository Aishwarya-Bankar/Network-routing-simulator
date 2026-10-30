"""
Network Routing Simulator
-------------------------
Routers are connected by links, and each link has a cost
(think of cost as delay or distance). This program finds the
cheapest path between two routers using Dijkstra's algorithm,
the idea behind link-state routing protocols such as OSPF.
"""

import heapq  # gives us a priority queue (always returns the smallest item first)


# ---------- 1. Build the network ----------

def add_link(network, router1, router2, cost):
    """Connect two routers with a link (works in both directions)."""
    network.setdefault(router1, {})[router2] = cost
    network.setdefault(router2, {})[router1] = cost


def remove_link(network, router1, router2):
    """Remove a link to simulate a failure. Returns True if it existed."""
    if router2 in network.get(router1, {}):
        del network[router1][router2]
        del network[router2][router1]
        return True
    return False


def sample_network():
    """A small network of 6 routers to start with."""
    network = {}
    add_link(network, "A", "B", 4)
    add_link(network, "A", "C", 2)
    add_link(network, "B", "C", 1)
    add_link(network, "B", "D", 5)
    add_link(network, "C", "D", 8)
    add_link(network, "C", "E", 10)
    add_link(network, "D", "E", 2)
    add_link(network, "D", "F", 6)
    add_link(network, "E", "F", 3)
    return network


# ---------- 2. Dijkstra's algorithm ----------

def dijkstra(network, source):
    """
    Find the cheapest cost from `source` to every other router.
    Returns two dictionaries:
      distance[router]  -> total cost from source to that router
      previous[router]  -> the router just before it on the best path
    """
    distance = {router: float("inf") for router in network}
    previous = {router: None for router in network}
    distance[source] = 0

    queue = [(0, source)]  # (cost so far, router)

    while queue:
        current_cost, router = heapq.heappop(queue)  # cheapest router first

        if current_cost > distance[router]:
            continue  # we already found a better way to this router

        for neighbor, link_cost in network[router].items():
            new_cost = current_cost + link_cost
            if new_cost < distance[neighbor]:  # found a cheaper path
                distance[neighbor] = new_cost
                previous[neighbor] = router
                heapq.heappush(queue, (new_cost, neighbor))

    return distance, previous


def get_path(previous, source, destination):
    """Walk backwards from destination to source to build the path."""
    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path if path[0] == source else None  # None means unreachable


# ---------- 3. Show things to the user ----------

def show_network(network):
    print("\nRouters and links:")
    for router in sorted(network):
        links = ", ".join(f"{n}(cost {c})" for n, c in sorted(network[router].items()))
        print(f"  {router} -> {links if links else 'no links'}")


def find_route(network):
    source = input("Source router: ").strip().upper()
    destination = input("Destination router: ").strip().upper()

    if source not in network or destination not in network:
        print("Router not found in the network.")
        return

    distance, previous = dijkstra(network, source)
    path = get_path(previous, source, destination)

    if path is None:
        print(f"No route from {source} to {destination}.")
    else:
        print(f"Best route: {' -> '.join(path)}")
        print(f"Total cost: {distance[destination]}")


def main():
    network = sample_network()

    while True:
        print("\n===== Network Routing Simulator =====")
        print("1. Show network")
        print("2. Find shortest route")
        print("3. Remove a link (simulate failure)")
        print("4. Add a link")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_network(network)
        elif choice == "2":
            find_route(network)
        elif choice == "3":
            r1 = input("First router: ").strip().upper()
            r2 = input("Second router: ").strip().upper()
            if remove_link(network, r1, r2):
                print(f"Link {r1}-{r2} removed.")
            else:
                print("That link does not exist.")
        elif choice == "4":
            r1 = input("First router: ").strip().upper()
            r2 = input("Second router: ").strip().upper()
            try:
                cost = int(input("Link cost (a number): "))
                add_link(network, r1, r2, cost)
                print(f"Link {r1}-{r2} added with cost {cost}.")
            except ValueError:
                print("Cost must be a whole number.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose 1-5.")


if __name__ == "__main__":
    main()
