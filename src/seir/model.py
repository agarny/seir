import os
from enum import Enum, auto

import matplotlib.pyplot as plt
import moh_data.main as md
import numpy as np
import opencor as oc


class Model:
    """
    SIRD model of Covid-19
    """

    __moh_data = None

    class Parameter:
        """
        A model parameter, i.e. either a VOI, a state variable or an algebraic
        variable.
        """

        class Kind(Enum):
            VOI = auto()
            STATE = auto()
            ALGEBRAIC = auto()

        def __init__(self, kind, parameter):
            # Initialise our model parameter.

            self.__kind = kind
            self.__parameter = parameter
            self.__values = np.array([])

        def kind(self):
            # Return our kind.

            return self.__kind

        def name(self):
            # Return our name.

            return self.__parameter.name()

        def values(self):
            # Return our values.

            return self.__values

        def __append_values(self, values):
            # Append the given values to our internal values.

            self.__values = np.append(self.__values, values)

    def __init__(self, use_moh_data=True):
        # Retrieve some data from the MoH, if needed.

        if use_moh_data and Model.__moh_data == None:
            Model.__moh_data = md.Basic()

        # Create (i.e. open) our SIRD simulation.

        self.__use_moh_data = use_moh_data
        self.__simulation = oc.open_simulation(os.path.dirname(__file__) + '/models/sird.sedml')

        # Initialise (i.e. reset) our simulation.

        self.reset()

    def reset(self):
        # Reset our SIRD simulation and clear all of its results (in case
        # another simulation has already been run).

        self.__simulation.reset()
        self.__simulation.clear_results()

        # Keep track of various model parameters.

        data = self.__simulation.data()
        self.__data_states = data.states()

        results = self.__simulation.results()
        states = results.states()

        self.__voi = self.Parameter(self.Parameter.Kind.VOI, results.voi())

        self.__s = self.Parameter(self.Parameter.Kind.STATE, states['main/S'])
        self.__i = self.Parameter(self.Parameter.Kind.STATE, states['main/I'])
        self.__r = self.Parameter(self.Parameter.Kind.STATE, states['main/R'])
        self.__d = self.Parameter(self.Parameter.Kind.STATE, states['main/D'])

        self.parameters = {
            self.__voi.name(): self.__voi,
            self.__s.name(): self.__s,
            self.__i.name(): self.__i,
            self.__r.name(): self.__r,
            self.__d.name(): self.__d,
        }

    def run(self, sim_duration=100):
        # Make sure that we were given a valid simulation duration.

        if sim_duration <= 0:
            print('The simulation duration (', sim_duration, ') must be greater than 0 (days).', sep='')

            return

        # Run our SIRD simulation.

        for i in range(sim_duration):
            # Output the data from the MoH.

            if self.__use_moh_data:
                try:
                    moh_i_r_d = Model.__moh_data.get_cumulative_total_cases_on_day(i)
                    moh_r = Model.__moh_data.get_cumulative_recovered_cases_on_day(i)
                    moh_d = Model.__moh_data.get_cumulative_dead_cases_on_day(i)

                    print('Day ', i, ': I=', moh_i_r_d - moh_r - moh_d, ' R=', moh_r, ' D=', moh_d, sep='')
                except:
                    pass

            # Run the simulation one day at a time.

            self.__simulation.data().set_ending_point(1 if sim_duration >= 1 else sim_duration)

            self.__simulation.run()

            # Update our simulation results using the results of the current
            # simulation.

            self.__voi._Parameter__append_values(i + self.__voi._Parameter__parameter.values())
            self.__s._Parameter__append_values(self.__s._Parameter__parameter.values())
            self.__i._Parameter__append_values(self.__i._Parameter__parameter.values())
            self.__r._Parameter__append_values(self.__r._Parameter__parameter.values())
            self.__d._Parameter__append_values(self.__d._Parameter__parameter.values())

    def plot(self):
        # Plot the results.

        plt.clf()  # In case there is already a Matplotlib window.
        plt.gcf().canvas.set_window_title('SIRD model')

        plt.plot(self.__voi.values(), self.__s.values(), '#0071bd', label=self.__s.name())
        plt.plot(self.__voi.values(), self.__i.values(), '#d9521a', label=self.__i.name())
        plt.plot(self.__voi.values(), self.__r.values(), '#edb020', label=self.__r.name())
        plt.plot(self.__voi.values(), self.__d.values(), '#7e2f8e', label=self.__d.name())
        plt.legend(loc='best')
        plt.xlabel('time (day)')

        plt.show()
