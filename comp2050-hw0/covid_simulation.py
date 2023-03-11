#!/usr/bin/env python3

""" File name:   covid19_simulation.py
    Description: This is the main file for COMP2050 Assignment 0 Exercise 4.

                 --- You do not need to modify this file ---

                 python covid19_simulation.py to get usage information.
"""

import copy
import importlib
import os.path
import sys
import time
import traceback
from io import StringIO

import matplotlib.pyplot as plt
import networkx as nx


class Capturing(list):
    """ A class to capture printed output. """

    def __enter__(self):
        """ Allow us to use instances of Capturing with the 'with' keyword.
            Deal with entering the with block.
        """
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        """ Allow us to use instances of Capturing with the 'with' keyword
            Deal with exiting the with block.
        """
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


non_existent_test = "tests/non_existent_test.scn"
test_files = ["exercise4_maps/test1.scn",
              "exercise4_maps/test2.scn", "exercise4_maps/test3.scn"]
test_params = [
    {"threshold": 0.5, "growth": 0.2, "spread": 0.1, "locations": ["l1", "l2"],
     "location": "l1",
     "covid": {"l1": 0, "l2": 0.8},
     "conn": {"l1": set(["l2"]), "l2": set(["l1"])},
     "vloc": "l2", "iloc": "l3",
     "10it": {'l2': 4.95338913792, 'l1': 0}},
    {"threshold": 1, "growth": 0.2, "spread": 0.1, "locations": ["l1", "l2", "l3", "l4"],
     "location": "l1",
     "covid": {"l1": 0, "l2": 1, "l3": 0, "l4": 0.1},
     "conn": {"l1": set(["l2", "l3"]), "l2": set(["l1", "l3"]), "l3": set(["l1", "l2", "l4"]),
              "l4": set(["l3"])},
     "vloc": "l2", "iloc": "l4",
     "10it": {'l4': 2.1405428582400003, 'l2': 7.713105638400002, 'l3': 5.520701214720001, 'l1': 0}},
    {"threshold": 1, "growth": 1, "spread": 1,
     "locations": ["l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9"],
     "location": "l9",
     "covid": {"l0": 0.5, "l1": 0, "l2": 0, "l3": 0, "l4": 0, "l5": 0, "l6": 0,
                 "l7": 0,   "l8": 0, "l9": 0},
     "conn": {"l0": set(["l1", "l5"]), "l1": set(["l0", "l2"]), "l2": set(["l1", "l3"]),
              "l3": set(["l2", "l4"]), "l4": set(["l3", "l9"]), "l5": set(["l0", "l6"]),
              "l6": set(["l5", "l7"]), "l7": set(["l6", "l8"]), "l8": set(["l7", "l9"]),
              "l9": set(["l4", "l8"])},
     "vloc": "l8", "iloc": "l2",
     "10it": {'l6': 31806.0, 'l7': 18411.0, 'l4': 7752.0, 'l5': 43757.0, 'l2': 31806.0,
              'l3': 18411.0, 'l0': 48620.0, 'l1': 43757.0, 'l8': 7752.0, 'l9': 0}
     }
]


class TestingError(Exception):
    """ An error to be raised when testing fails. """


def test_scenario_file(module):
    """ Test the given covid19_scenario module.

        (module) -> None
    """
    print("Testing implementation of covid_scenario.py")
    print("--------------------------------------------------------------------")

    print("Checking for COVID19Scenario class...")
    print("-------------------------------------")
    try:
        ds_class = module.COVID19Scenario
        if type(ds_class) != type:
            print("Failed. COVID19Scenario is not a class.")

            class tc:
                pass
            if type(ds_class) == type(tc):
                print("You have forgotten to make COVID19Scenario subclass object.")
            raise TestingError()
        ds = ds_class()
    except AttributeError:
        print("Failed. COVID19Scenario does not exist.")
        raise TestingError()
    print("Success.")

    print("Testing read_scenario_file method.")
    print("-------------------------------------")
    try:
        rsf = ds.read_scenario_file
        print("Testing on a non-existent file...")
        try:
            if rsf(non_existent_test):
                print("Error: either to you failed to return False when an IOError was raised or",
                      "you created a file called non_existent_test.scn (you should delete it).")
                raise TestingError()
        except IOError:
            print("Error: you are supposed to catch IOErrors and return false.")
            raise TestingError()
        except Exception:
            print("Unexpected error when running on a non-existent file:")
            print(traceback.format_exc())
            raise TestingError()

        print("Success.")

        test_ds = []
        for test, tparams in zip(test_files, test_params):
            print("Testing on file:", test)
            ds_copy = copy.deepcopy(ds)
            try:
                if not ds_copy.read_scenario_file(test):
                    print(
                        "Error:", test, " does not exist or you are returning False inadvertently.")
                    raise TestingError()

                if hasattr(module.COVID19Scenario, 'threshold'):
                    print("Error: you have made threshold a class variable!")
                    print("It should belong to the instance -- i.e. self.threshold = x")
                    raise TestingError()

                if hasattr(module.COVID19Scenario, 'growth'):
                    print("Error: you have made growth a class variable!")
                    print("It should belong to the instance -- i.e. self.growth = x")
                    raise TestingError()

                if hasattr(module.COVID19Scenario, 'spread'):
                    print("Error: you have made spread a class variable!")
                    print("It should belong to the instance -- i.e. self.spread = x")
                    raise TestingError()

                if hasattr(module.COVID19Scenario, 'location'):
                    print("Error: you have made location a class variable!")
                    print("It should belong to the instance -- i.e. self.location = x")
                    raise TestingError()

                if hasattr(module.COVID19Scenario, 'locations'):
                    print("Error: you have made locations a class variable!")
                    print(
                        "It should belong to the instance -- i.e. self.locations = []")
                    raise TestingError()

                if hasattr(module.COVID19Scenario, 'covid'):
                    print("Error: you have made covid a class variable!")
                    print("It should belong to the instance -- i.e. self.covid = {}")
                    raise TestingError()

                if hasattr(module.COVID19Scenario, 'conn'):
                    print("Error: you have made conn a class variable!")
                    print("It should belong to the instance -- i.e. self.conn = {}")
                    raise TestingError()

                test_ds.append(ds_copy)
            except IOError:
                print("Error: you are supposed to catch IOErrors and return false.")
                raise TestingError()
            except TestingError:
                raise TestingError()
            except Exception:
                print("Unexpected error:")
                print(traceback.format_exc())
                raise TestingError()
            try:
                if not isinstance(ds_copy.threshold, float) and not isinstance(ds_copy.threshold, int):
                    print("Error: threshold should be a float or int!")
                    raise TestingError()
                if abs(ds_copy.threshold - tparams["threshold"]) > 0.001:
                    print("Error: threshold has unexpected value: ", ds_copy.threshold,
                          "expected:", tparams["threshold"])
                    raise TestingError()
            except AttributeError:
                print("Error: threshold variable is missing.")
                raise TestingError()

            try:
                if not isinstance(ds_copy.growth, float) and not isinstance(ds_copy.growth, int):
                    print("Error: growth should be a float or int!")
                    raise TestingError()

                if abs(ds_copy.growth - tparams["growth"]) > 0.001:
                    print("Error: growth has unexpected value:", ds_copy.growth,
                          "expected:", tparams["growth"])
                    raise TestingError()
            except AttributeError:
                print("Error: growth variable is missing.")
                raise TestingError()

            try:
                if not isinstance(ds_copy.spread, float) and not isinstance(ds_copy.spread, int):
                    print("Error: spread should be a float or int!")
                    raise TestingError()

                if abs(ds_copy.spread - tparams["spread"]) > 0.001:
                    print("Error: spread has unexpected value: ", ds_copy.spread,
                          "expected:", tparams["spread"])
                    raise TestingError()
            except AttributeError:
                print("Error: spread variable is missing.")
                raise TestingError()

            try:
                if ds_copy.location != tparams["location"]:
                    print("Error: location has unexpected value: ", ds_copy.location,
                          "expected:", tparams["location"])
                    raise TestingError()
            except AttributeError:
                print("Error: location variable is missing.")
                raise TestingError()

            try:
                if not isinstance(ds_copy.locations, list):
                    print("Error: locations is not a list.")
                    raise TestingError()
                for loc in ds_copy.locations:
                    if loc not in tparams["locations"]:
                        print("Unexpected location:", loc)
                        raise TestingError()
                for loc in tparams["locations"]:
                    if loc not in ds_copy.locations:
                        print("Missing location:", loc)
                        raise TestingError()
            except AttributeError:
                print("Error: locations variable is missing.")
                raise TestingError()

            try:
                if not isinstance(ds_copy.covid, dict):
                    print("Error: covid is not a dictionary.")
                    raise TestingError()
                for loc, dis in ds_copy.covid.items():
                    if loc not in tparams["covid"]:
                        print("Unexpected covid location:", loc)
                        raise TestingError()

                    if not isinstance(dis, float) and not isinstance(dis, int):
                        print("Error: the covid at location",
                              loc, "should be a float or int!")
                        raise TestingError()

                    if abs(tparams["covid"][loc] - dis) > 0.001:
                        print("Invalid covid at location:", loc, "expected:",
                              tparams["covid"][loc])
                        raise TestingError()
                for loc, dis in tparams["covid"].items():
                    if loc not in ds_copy.covid:
                        print(
                            "Missing covid location (locations should have 0 covid by default):", loc)
                        raise TestingError()
            except AttributeError:
                print("Error: covid variable is missing.")
                raise TestingError()

            try:
                if not isinstance(ds_copy.conn, dict):
                    print("Error: conn is not a dictionary.")
                    raise TestingError()

                for loc, locs in ds_copy.conn.items():
                    if loc not in tparams["conn"]:
                        print("Unexpected conn location:", loc)
                        raise TestingError()

                    if not isinstance(locs, set):
                        print("Error: location", loc, "should have a *set* of connected",
                              "locations in the conn dictionary.")
                        raise TestingError()
                    if locs != tparams["conn"][loc]:
                        print(
                            "There is an invalid set of connections at location:", loc)
                        print("We expected:", tparams["conn"][loc])
                        print("We got:", locs)
                        raise TestingError()

                for loc, dis in tparams["conn"].items():
                    if loc not in ds_copy.conn:
                        print("Missing location in conn dictionary:", loc)
                        raise TestingError()

            except AttributeError:
                print("Error: conn dictionary is missing.")
                raise TestingError()
    except AttributeError:
        print("Failed. read_scenario_file does not exist.")
        raise TestingError()
    print("Success.")

    print("Testing valid_moves method.")
    print("-------------------------------------")
    try:
        vm = ds.valid_moves
    except AttributeError:
        print("Failed. valid_moves does not exist.")
        raise TestingError()

    for tid, test_file in enumerate(test_files):
        tparams = test_params[tid]
        ds = test_ds[tid]

        try:
            correct_vm = tparams["conn"][tparams["location"]]
            correct_vm.add(tparams["location"])
            valid_moves = ds.valid_moves()
            if not isinstance(valid_moves, list):
                print("Error: valid_moves is supposed to return a list.")
                raise TestingError()
            if set(valid_moves) != correct_vm:
                print("Error: valid moves for test:", test_file, "loc:", ds.location,
                      "is wrong. Did you remember that agents can move to their",
                      "current locations?")
                print("We expected:", sorted(correct_vm))
                print("We got:", sorted(valid_moves))

                raise TestingError()
        except Exception:
            print("Unexpected error when running valid_moves for test:",
                  test_file, "location:", ds.location)
            print(traceback.format_exc())
            raise TestingError()
    print("Success.")

    print("Testing move method.")
    print("-------------------------------------")
    try:
        mm = ds.move
    except AttributeError:
        print("Failed. move does not exist.")
        raise TestingError()

    for tid, test_file in enumerate(test_files):
        tparams = test_params[tid]
        ds = copy.deepcopy(test_ds[tid])

        # Invalid move first
        try:
            ds.move(tparams["iloc"])
            raise TestingError()
        except ValueError:
            pass
        except Exception:
            print("Unexpected error when running move method with an invalid location:",
                  tparams["iloc"], "for test:", test_file)
            print(traceback.format_exc())
            print("We Expected a ValueError to be raised when an invalid move was made.")
            raise TestingError()

        # Valid move
        ds.covid[tparams["vloc"]] = 100
        try:
            ds.move(tparams["vloc"])
        except Exception:
            print("Unexpected error when running move to", tparams["vloc"],
                  "for test:", test_file)
            print(traceback.format_exc())
            raise TestingError()
        if ds.covid[tparams["vloc"]] != 0:
            print("Error: moving to", tparams["vloc"],
                  "did not clear covid there in test:", test_file)
            raise TestingError()
        if ds.location != tparams["vloc"]:
            print("Error: moving to", tparams["vloc"], "failed to change the location",
                  "in test:", test_file)
            raise TestingError()
    print("Success.")

    print("Testing spread_covid method.")
    print("-------------------------------------")
    try:
        sd = ds.spread_covid
    except AttributeError:
        print("Failed. spread_covid does not exist.")
        raise TestingError()

    for tid, test_file in enumerate(test_files):
        tparams = test_params[tid]
        ds = test_ds[tid]
        try:
            for it in range(10):
                ds.spread_covid()
        except Exception:
            print("Unexpected error when running spread_covid for test:", test_file)
            print(traceback.format_exc())
            raise TestingError()

        try:
            ed = tparams["10it"]
            for loc in tparams["locations"]:
                if loc == tparams["location"]:
                    if ds.covid[loc] != 0:
                        print("Error: we expect there to always be zero covid",
                              "at the current location:", test_file, "instead there is:",
                              ds.covid[loc])
                        raise TestingError()
                else:
                    if abs(ds.covid[loc] - ed[loc]) > 0.01:
                        print("Error: after 10 iterations there is the wrong",
                              "covid", ds.covid[loc], "expected", ed[loc],
                              "(0.01 epsilon) at location:", loc, "test:", test_file)
                        raise TestingError()
        except AttributeError:
            print("Error: you must have deleted covid when running spread_covid",
                  "for test:", test_file)

    print("All tests passed. Good job!")
    print("These tests are thorough, but not exhaustive.")
    print("At the end of the day, the correctness of your code depends on you following instructions.")
    print("Make sure you check your code again, comment your file appropriately,",
          "and then proceed to the next part of the exercise.")


def print_summary(scenario):
    """ Print a summary of the covid spread and current location in the
        given scenario.

        (COVID19Scenario) -> None
    """
    print("The locations have the following covid:")
    total_covid = 0
    tokens = []
    for loc in scenario.locations:
        covid = scenario.covid[loc]
        total_covid += covid
        if covid >= scenario.threshold:
            status = "(spreading)"
        else:
            status = "()"
        tokens.append(' '.join([loc, str(covid), status]))
    print(','.join(tokens))
    print("Total covid patients:", total_covid)
    return total_covid


def show_graph(graph):
    graph.graph = nx.Graph()
    for node, covid in graph.covid.items():
        graph.graph.add_node(node, label=node + ": " + str(covid))

    for node in graph.conn.keys():
        graph.graph.add_edges_from([(node, neighbor)
                                    for neighbor in list(graph.conn[node])])
    plt.clf()
    nx.draw(graph.graph, pos=nx.circular_layout(graph.graph), with_labels=True, font_weight='bold',
            labels={k: "{}\n{:.2f}".format(k, v)
                    for k, v in graph.covid.items()},
            node_size=1300,
            node_color=["b" if loc == graph.location else "g" if d <= 0 else "r" for loc, d in graph.covid.items()])
    plt.text(-1, 0.8,
             "Spread: " + str(graph.spread) +
             "\nGrowth: " + str(graph.growth) +
             "\nThreshold: " + str(graph.threshold))
    plt.draw()
    # Needed since GUI events happen while main code is sleeping
    plt.pause(0.01)
    input("Press [Enter] in the terminal to continue.")


def on_keyboard(event):
    if event.key == 'right':
        plt.show(block=False)
    if event.key == 'escape':
        exit()


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        description='Horseman No. 2 - a covid19 simulator')
    parser.add_argument('-t', '--test', default=False, action='store_true',
                        help='Activates TESTING mode (default: deactivated)')
    parser.add_argument('-s', '--scenario', default=None,
                        type=str, help='Path to scenario (.scn) file')
    parser.add_argument('-a', '--agent', default='COVID19EradicationAgent',
                        type=str, help='Agent to be used (default: COVID19EradicationAgent)')
    parser.add_argument('-H', '--horizon', default=100, type=int,
                        help='Maximum number of steps in the simulation (default: 100)')
    parser.add_argument('-n', '--num_sims', default=1, type=int,
                        help='Number of simulations to run (default: 1)')
    parser.add_argument('-v', '--viz', default=False, action='store_true',
                        help='Draw a graph to visualise how covid is spread. '
                             'When this is enabled, you need to press Enter in the terminal to move along the animation.')

    args = parser.parse_args()

    if args.scenario is None and not args.test:
        print("[Fatal]: Scenario file was not specified!")
        parser.print_help()
        sys.exit(1)

    return args


def main():
    """ Run the simulation on the scenario file given in the command line.

        () -> None
    """

    args = parse_arguments()

    try:
        with Capturing() as output:
            import covid_scenario
    except ImportError:
        print("Error covid_scenario.py does not exist.")
        sys.exit()
    except Exception:
        print("Error: exception when importing covid_scenario:")
        print(traceback.format_exc())
        sys.exit()

    if output:
        print("Error covid_scenario.py produced output when imported.")
        sys.exit()

    if args.test:
        try:
            test_scenario_file(covid_scenario)
        except TestingError:
            pass
    else:
        try:
            ds = covid_scenario.COVID19Scenario()
            if not ds.read_scenario_file(args.scenario):
                print("Error: the supplied scenario file does not exist:",
                      args.scenario)
                sys.exit()
        except Exception:
            print(
                "Unexpected error while loading the specified covid scenario:", args.scenario)
            print(traceback.format_exc())
            print("Are you sure you tested covid_scenario correctly?")
            sys.exit()

        agent_name = args.agent
        print("Trying to load agent:", agent_name)
        try:
            agent_module = importlib.import_module("covid_curing_agents")
            base_class = agent_module.COVID19CuringAgent
        except ImportError:
            print("Error loading agent from covid_curing_agents.py")
            print("Make sure the file exists.")
            sys.exit()
        except Exception:
            print("Unexpected error while trying to import covid_curing_agents.py:")
            print(traceback.format_exc())
            print("What did you do in that file?")
            sys.exit()

        if agent_name not in agent_module.__dict__:
            print("There is no such agent as",
                  agent_name, "in covid_curing_agents.py")
            sys.exit()

        agent_class = agent_module.__dict__[agent_name]
        if not issubclass(agent_class, base_class):
            print("Error:", agent_name, "is not an instance of a COVID19CuringAgent.")
            sys.exit()

        try:
            agent = agent_class(list(ds.locations), copy.deepcopy(ds.conn))
        except Exception:
            print("Unknown error while trying to create a new:", agent_name)
            print(traceback.format_exc())
            sys.exit()

        print("Agent loaded.")

        try:
            iterations = args.horizon
            if iterations < 0:
                raise ValueError()
        except ValueError:
            print("Error: invalid number of iterations:", sys.argv[3])
            sys.exit()

        simulations_data = {}
        simulations_data['runs'] = []
        simulations_data['average_score'] = 0.0
        print_summary(ds)
        print("Agent location:", ds.location)
        if args.viz:
            plt.show()
            show_graph(ds)

        try:
            import random
            random.seed(938729021)
            start_time = time.time()
            for j in range(0, args.num_sims):
                # This two lines won't do anything. We can't change
                # PYTHONHASHSEED dynamically during run time. See
                # https://stackoverflow.com/q/25684349. This means that if a
                # student uses sets, the random order when accessing elements
                # in a set might change the simulation result between each run.
                hash_seed = random.randint(1, 4294967295)
                os.environ['PYTHONHASHSEED'] = str(hash_seed)

                print(f"Starting simulation {j+1} out of {args.num_sims}.")
                ds = covid_scenario.COVID19Scenario()
                ds.read_scenario_file(args.scenario)

                for i in range(iterations):
                    print("\nSimulation Step:", i)

                    valid_moves = ds.valid_moves()
                    move = agent.choose_move(ds.location, list(valid_moves),
                                             dict(ds.covid), ds.threshold, ds.growth, ds.spread)

                    print("Selected move:", move)

                    ds.move(move)
                    ds.spread_covid()
                    total_covid = print_summary(ds)

                    if args.viz:
                        show_graph(ds)

                    if total_covid < 0.001:
                        print("You cure all covid19 patients! Good job.")
                        break
                    if total_covid >= 100000:
                        print("Total covid19 patients went over 100000.")
                        print("Covid19 has taken over Vietnam and its surroundings,")
                        print("we are all gonna die!!!.")
                        break
                sim_data = {}
                sim_data['last_step'] = i
                sim_data['final_covid'] = total_covid
                sim_data['score'] = 0.0
                if total_covid < 100000:
                    if i < args.horizon - 1:
                        sim_data['score'] = args.horizon - i
                    else:
                        sim_data['score'] = 1.0 - \
                            float(total_covid)/float(100000)
                simulations_data['runs'].append(sim_data)
                simulations_data['average_score'] += sim_data['score']
            end_time = time.time()
            simulations_data['runtime'] = end_time - start_time
            simulations_data['average_score'] /= float(args.num_sims)

            import json
            print(simulations_data)
            with open('{}.results.json'.format(os.path.basename(args.scenario).replace('.scn', '')), 'w') as output:
                output.write(json.dumps(simulations_data,
                                        sort_keys=True, indent=4))
            print("Simulation finished in {}".format(end_time - start_time))

        except Exception:
            print("Error: unexpected exception while running the simulation.")
            print(traceback.format_exc())
            sys.exit()


if __name__ == "__main__":
    main()