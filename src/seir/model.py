import os
from enum import Enum, auto

import matplotlib.pyplot as plt
import numpy as np
import opencor as oc


class Model:
    """
    SEIR model of Covid-19, as described at
    https://cpb-ap-se2.wpmucdn.com/blogs.auckland.ac.nz/dist/d/75/files/2017/01/Covid19_SEIR_model.pdf.
    """

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

    def __init__(self):
        # Create (i.e. open) our SEIR simulation.

        self.__simulation = oc.open_simulation(os.path.dirname(__file__) + '/models/seir.sedml')

        # Initialise (i.e. reset) our simulation.

        self.__reset()

    def __reset(self):
        # Reset our SEIR simulation and clear all of its results (in case
        # another simulation has already been run).

        self.__simulation.reset()
        self.__simulation.clear_results()

        # Keep track of various model parameters.

        results = self.__simulation.results()

        states = results.states()
        algebraic = results.algebraic()

        self.__voi = self.Parameter(self.Parameter.Kind.VOI, results.voi())

        self.__s = self.Parameter(self.Parameter.Kind.STATE, states['main/S'])
        self.__e = self.Parameter(self.Parameter.Kind.STATE, states['main/E'])
        self.__i_c = self.Parameter(self.Parameter.Kind.STATE, states['main/I_c'])
        self.__i_p = self.Parameter(self.Parameter.Kind.STATE, states['main/I_p'])
        self.__i_u = self.Parameter(self.Parameter.Kind.STATE, states['main/I_u'])
        self.__r_c = self.Parameter(self.Parameter.Kind.STATE, states['main/R_c'])
        self.__r_u = self.Parameter(self.Parameter.Kind.STATE, states['main/R_u'])

        self.__i = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/I'])
        self.__r = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/R'])
        self.__d = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/D'])
        self.__ifr = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/IFR'])

        self.parameters = {
            self.__voi.name(): self.__voi,
            self.__s.name(): self.__s,
            self.__e.name(): self.__e,
            self.__i_c.name(): self.__i_c,
            self.__i_p.name(): self.__i_p,
            self.__i_u.name(): self.__i_u,
            self.__r_c.name(): self.__r_c,
            self.__r_u.name(): self.__r_u,
            self.__i.name(): self.__i,
            self.__r.name(): self.__r,
            self.__d.name(): self.__d,
            self.__ifr.name(): self.__ifr,
        }

    def run(self, sim_duration=300):
        # Make sure that we were given a valid simulation duration.

        if sim_duration <= 0:
            print('The simulation duration (', sim_duration, ') must be greater than 0 (days).', sep='')

            return

        # Reset and run our SEIR simulation.

        self.__reset()

        run_nb = 0

        while sim_duration > 0:
            # Run the simulation one day at a time.

            self.__simulation.data().set_ending_point(1 if sim_duration >= 1 else sim_duration)

            self.__simulation.run()

            sim_duration -= 1

            # Update our simulation results using the results of the current
            # simulation.

            self.__voi._Parameter__append_values(run_nb + self.__voi._Parameter__parameter.values())
            self.__s._Parameter__append_values(self.__s._Parameter__parameter.values())
            self.__e._Parameter__append_values(self.__e._Parameter__parameter.values())
            self.__i_c._Parameter__append_values(self.__i_c._Parameter__parameter.values())
            self.__i_p._Parameter__append_values(self.__i_p._Parameter__parameter.values())
            self.__i_u._Parameter__append_values(self.__i_u._Parameter__parameter.values())
            self.__r_c._Parameter__append_values(self.__r_c._Parameter__parameter.values())
            self.__r_u._Parameter__append_values(self.__r_u._Parameter__parameter.values())
            self.__i._Parameter__append_values(self.__i._Parameter__parameter.values())
            self.__r._Parameter__append_values(self.__r._Parameter__parameter.values())
            self.__d._Parameter__append_values(self.__d._Parameter__parameter.values())
            self.__ifr._Parameter__append_values(self.__ifr._Parameter__parameter.values())

            run_nb += 1

    def plot(self):
        # Plot the results.

        plt.clf()  # In case there is already a Matplotlib window.
        plt.gcf().canvas.set_window_title('SEIR model')

        plt.subplot(4, 1, 1)
        plt.plot(self.__voi.values(), self.__s.values(), label=self.__s.name())
        plt.plot(self.__voi.values(), self.__e.values(), label=self.__e.name())
        plt.plot(self.__voi.values(), self.__i_p.values(), label=self.__i_p.name())
        plt.plot(self.__voi.values(), self.__i.values(), label=self.__i.name())
        plt.plot(self.__voi.values(), self.__r.values(), label=self.__r.name())
        plt.plot(self.__voi.values(), self.__d.values(), label=self.__d.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 2)
        plt.plot(self.__voi.values(), self.__i.values(), label=self.__i.name())
        plt.plot(self.__voi.values(), self.__i_c.values(), label=self.__i_c.name())
        plt.plot(self.__voi.values(), self.__i_u.values(), label=self.__i_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 3)
        plt.plot(self.__voi.values(), self.__r.values(), label=self.__r.name())
        plt.plot(self.__voi.values(), self.__r_c.values(), label=self.__r_c.name())
        plt.plot(self.__voi.values(), self.__r_u.values(), label=self.__r_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 4)
        plt.plot(self.__voi.values(), self.__ifr.values(), label=self.__ifr.name())
        plt.legend(loc='center left')
        plt.xlabel('time (day)')

        plt.show()
