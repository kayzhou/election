#-*- coding: utf-8 -*-

"""
Created on 2018-12-20 15:40:26
@author: https://kayzhou.github.io/
"""

# NetworkX performs network analytics (computes scc)

import heapq
import json
import time
from functools import partial
from math import log
from multiprocessing import Pool

import networkx as nx
from tqdm import tqdm


class CollectiveInfluencer(object):
    '''
    for CI
    '''

    def __init__(self, num_ci_threads=1):
        '''
        Constructor
        '''
        self.CORES = num_ci_threads
        self.CP = False
        self.winners = None
        self.winner_deg = None
        self.winners_ci = None

    # Threaded CI routine
    def siteCI(self, graph, ball_rad=2, directed=True, treelike=True,
                           verbose=True, flashy=True, G_q_filename=None):
        start = time.time()
        main_proc_time = 0
        CI_time = 0
        sort_time = 0
        build_in_time = 0

        winners = []
        winner_deg = []
        winners_ci = []

        if G_q_filename is not None:
            G_q_file = open(G_q_filename, 'w')

        # Start thread pool
        pool = Pool(self.CORES)
        f = partial(self.cleanCalcCI, graph, ball_rad=ball_rad, directed=directed, treelike=treelike)

        # Calculate CI for entire graph
        if verbose:
            print('Multitasking with ' + str(self.CORES) + ' threads.\n')

        num_nodes = len(graph.nodes())

        newtime = time.time()
        main_proc_time += newtime - start
        newtime = time.time()

        # Calculate CI
        print("Calculating CI ...")
        # node_CIs = pool.map(f, graph.nodes())
        # pool.close()
        # pool.join()

        node_CIs = {}
        for node in graph.nodes():
            if len(node_CIs) % 1000 == 0:
                print(len(node_CIs))
            this_CI = self.cleanCalcCI(graph, node, ball_rad=ball_rad,
                                    directed=directed, treelike=treelike)
            node_CIs[node] = this_CI

        print("finished!")

        CI_time += time.time() - newtime
        newtime = time.time()

        pile = []
        for node in graph.nodes():
            graph.node[node]['CI'] = node_CIs[node]
            graph.node[node]['start_deg'] = graph.degree(node)
            graph.node[node]['start_CI'] = node_CIs[node]
            pile.append((-1 * node_CIs[node], node))

        # Our hybrid heap/hashmap wizardry
        updated = set()
        heapq.heapify(pile)

        try:
            max_bundle = heapq.heappop(pile)
        except IndexError:
            max_bundle = None

        main_proc_time += time.time() - newtime
        newtime = time.time()

        # Remove influencers until none remain
        while max_bundle is not None and len(winners) < 500:
            print("count(winners) =", len(winners))
            max_CI = max_bundle[0] * -1
            max_node = max_bundle[1]

            # Remove influencer
            main_proc_time += time.time() - newtime
            newtime = time.time()

            max_ball = self.buildInBall(graph, max_node, ball_rad)

            build_in_time += time.time() - newtime
            newtime = time.time()

            winners.append(max_node)
            winner_deg.append(graph.node[max_node]['start_deg'])
            winners_ci.append(max_CI ** (1 / ball_rad))
            #winners_ci.append(graph.node[max_node]['start_CI'])

            if G_q_filename is not None:
                # print q and G(g)
                q = 1 - graph.number_of_nodes() / num_nodes
                gc_nodes = max(nx.strongly_connected_components(graph), key=len)
                nodes_in_gc = [node for node in graph.nodes() if node in gc_nodes]

                print("{:.6f}".format(q) + ', ' + "{:.6f}".format(len(nodes_in_gc) / num_nodes), file=G_q_file)

            graph.remove_node(max_node) # why remove?

            if flashy:
                print('#', end="", flush=True)
                if len(winners) % 100 == 0:
                        print('')

            # Mark nodes inside the ball for deferred CI update
            # (Other CI values will not have changed)
            for ring in max_ball:
                for node in ring:
                    updated.add(node)

            main_proc_time += time.time() - newtime
            newtime = time.time()

            # Find next influencer
            max_bundle = None
            while max_bundle is None and len(pile) > 0:

                # Take the root item
                try:
                    max_bundle = heapq.heappop(pile)
                except IndexError:
                    max_bundle = None
                    break
                max_CI = max_bundle[0] * -1
                max_node = max_bundle[1]


                # Check if it's up-to-date
                if max_node in updated:

                    sort_time += time.time() - newtime
                    newtime = time.time()

                    new_CI = self.cleanCalcCI(graph, max_node, ball_rad=ball_rad, directed=directed, treelike=treelike)

                    CI_time += time.time() - newtime
                    newtime = time.time()

                    updated.remove(max_node)
                    heapq.heappush(pile, (-1 * new_CI, max_node))
                    max_bundle = None
                    continue

                sort_time += time.time() - newtime
                newtime = time.time()

                # Remove it
                if max_CI < 1:
                    break

        # Return your sorted list of influencers
        if verbose:
            print('\nMain proc: ' + str(main_proc_time))
            print('CI time: ' + str(CI_time))
            print('Sort time: ' + str(sort_time))
            print('Build In: ' + str(build_in_time))
            print('\nInfluencers Total: ' + str(len(winners)))
            print('Number of Nodes: ' + str(num_nodes))
            print('\n')

        if G_q_filename is not None:
            G_q_file.close()

        self.winners = winners
        self.winner_deg = winner_deg
        self.winners_ci = winners_ci

        return winners, winner_deg, winners_ci

    # Calculate the CI value for the specified node
    def cleanCalcCI(self, graph, node, ball_rad, directed, treelike):
        # print("Calulate CI value for", node)

        # If this node isn't in the graph, it VERY isn't influential
        if node not in graph:
            return -1

        if graph.degree(node) < 2:
            return 0

        # Build the ball
        visited = {node: 0}
        rings = [[node]] # {} means set?

        for _ring in range(1, ball_rad + 2):
            nextring = []
            for node_n in rings[_ring - 1]:
                for neighb_n in graph.neighbors(node_n):
                    if neighb_n not in visited:
                        nextring.append(neighb_n)
                        visited[neighb_n] = _ring
            rings.append(nextring)

        # CALCULATE THE CI VALUE
        if directed:
            if treelike:
                degsum = sum(graph.out_degree(shell_node) for shell_node in rings[ball_rad])
                ci_value = (graph.out_degree(node) - 1) * degsum
            else:
                ci_value = (graph.out_degree(node) - 1) * len(rings[ball_rad+1])

        else:
            if treelike:
                degsum = 0
                for shell_node in rings[ball_rad]:
                    degsum += (graph.degree(shell_node) - 1)
                ci_value = (graph.degree(node) - 1) * degsum
            else:
                ci_value = (graph.degree(node) - 1) * len(rings[ball_rad+1])

        # Alternate algorithm; *~new and improved~!*
        if self.CP:
            degsum = []
            for n, shell in enumerate(rings[:ball_rad]):
                shelldeg = 0
                for shell_node in shell:
                    shelldeg += (graph.degree(shell_node) - 1)
                degsum.append(shelldeg)

            # l-Factorial algorithm
            tot = 0
            poly = 1
            for n, _ring in enumerate(degsum):
                if _ring > 0:
                    tot += _ring
                poly *= tot
            ci_value = poly

        return ci_value

    # Build the inbound ball for a given node
    def buildInBall(self, graph, node, ball_rad=2):

        # If this node isn't in the graph, it VERY isn't influential
        if node not in graph:
            return []

        ring = 0
        rings = [[node]]
        while ring < ball_rad + 1:
            ring += 1
            nextring = []
            for node_n in rings[ring-1]:
                nextring += self.markInRing(graph, node_n)
            rings.append(nextring)

        # Clean up
        for ring in rings:
            for n in ring:
                del graph.node[n]['inpath']

        return rings

    # Mark the N'th ring of nodes who influence a given node
    def markInRing(self, graph, node):

        # Determine the order of this ring
        if 'inpath' not in graph[node]:
            graph.node[node]['inpath'] = 1
        n = graph.node[node]['inpath'] + 1

        # Look at this node's neighborhood of predecessors
        try:
            neighborhood = graph.predecessors(node)
        except AttributeError:
            neighborhood = graph.neighbors(node)
        outer_neighbors = []

        # If we find a new node, mark it and add it to the new perimeter
        for neighbor in neighborhood:
            if 'inpath' not in graph.node[neighbor]:
                graph.node[neighbor]['inpath'] = n
                outer_neighbors.append(neighbor)

        # Return the new perimeter
        return outer_neighbors

    def save_winners(self):
        json.dump(self.winners, open("data/fake_winners.json", "w"), indent=2)
        json.dump(self.winner_deg, open("data/fake_winner_deg.json", "w"), indent=2)
        json.dump(self.winners_ci, open("data/fake_winners_ci.json", "w"), indent=2)


if __name__ == "__main__":
    # Lebron = CollectiveInfluencer(num_ci_threads=8)
    Lebron = CollectiveInfluencer()
    # G = nx.read_gpickle("data/whole_network.gpickle")
    G = nx.read_gpickle("data/fake_network.gpickle")
    # G = nx.fast_gnp_random_graph(1000, 0.1, directed=True)
    print("loaded graph!")
    Lebron.siteCI(G, ball_rad=2)
    Lebron.save_winners()
