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
        A model parameter, i.e. either a state variable or an algebraic variable.
        """

        class Kind(Enum):
            VOI = auto()
            STATE = auto()
            ALGEBRAIC = auto()

        def __init__(self, kind, parameter):
            # Initialise our model parameter.

            self._kind = kind
            self._parameter = parameter
            self._values = np.array([])

        def kind(self):
            # Return our kind.

            return self._kind

        def name(self):
            # Return our name.

            return self._parameter.name()

        def values(self):
            # Return our values.

            return self._values

        def _append_values(self, values):
            # Append the given values to our internal values.

            self._values = np.append(self._values, values)

    def __init__(self):
        # Initialise our SEIR simulation.

        self.simulation = oc.open_simulation(os.path.dirname(__file__) + '/models/seir.sedml')

        # Keep track of various model parameters.

        results = self.simulation.results()

        states = results.states()
        algebraic = results.algebraic()

        self.voi = self.Parameter(self.Parameter.Kind.VOI, results.voi())

        self.s = self.Parameter(self.Parameter.Kind.STATE, states['main/S'])
        self.e = self.Parameter(self.Parameter.Kind.STATE, states['main/E'])
        self.i_c = self.Parameter(self.Parameter.Kind.STATE, states['main/I_c'])
        self.i_p = self.Parameter(self.Parameter.Kind.STATE, states['main/I_p'])
        self.i_u = self.Parameter(self.Parameter.Kind.STATE, states['main/I_u'])
        self.r_c = self.Parameter(self.Parameter.Kind.STATE, states['main/R_c'])
        self.r_u = self.Parameter(self.Parameter.Kind.STATE, states['main/R_u'])

        self.i = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/I'])
        self.r = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/R'])
        self.d = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/D'])
        self.ifr = self.Parameter(self.Parameter.Kind.ALGEBRAIC, algebraic['main/IFR'])

    def run(self, sim_duration=300):
        # Make sure that we were given a valid simulation duration.

        if sim_duration <= 0:
            print('The simulation duration (', sim_duration, ') must be greater than 0 (days).', sep='')

            return

        # Reset and run our SEIR simulation.

        self.simulation.reset()  # In case another simulation had already been run.

        run_nb = 0

        while sim_duration > 0:
            # Run the simulation one day at a time.

            self.simulation.data().set_ending_point(1 if sim_duration >= 1 else sim_duration)

            self.simulation.run()

            sim_duration -= 1

            # Update our simulation results using the results of the current
            # simulation.

            self.voi._append_values(run_nb + self.voi._parameter.values())
            self.s._append_values(self.s._parameter.values())
            self.e._append_values(self.e._parameter.values())
            self.i_c._append_values(self.i_c._parameter.values())
            self.i_p._append_values(self.i_p._parameter.values())
            self.i_u._append_values(self.i_u._parameter.values())
            self.r_c._append_values(self.r_c._parameter.values())
            self.r_u._append_values(self.r_u._parameter.values())
            self.i._append_values(self.i._parameter.values())
            self.r._append_values(self.r._parameter.values())
            self.d._append_values(self.d._parameter.values())
            self.ifr._append_values(self.ifr._parameter.values())

            run_nb += 1

    def plot(self):
        # Plot the results.

        plt.clf()  # In case there is already a Matplotlib window.
        plt.gcf().canvas.set_window_title('SEIR model')

        plt.subplot(4, 1, 1)
        plt.plot(self.voi.values(), self.s.values(), label=self.s.name())
        plt.plot(self.voi.values(), self.e.values(), label=self.e.name())
        plt.plot(self.voi.values(), self.i_p.values(), label=self.i_p.name())
        plt.plot(self.voi.values(), self.i.values(), label=self.i.name())
        plt.plot(self.voi.values(), self.r.values(), label=self.r.name())
        plt.plot(self.voi.values(), self.d.values(), label=self.d.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 2)
        plt.plot(self.voi.values(), self.i.values(), label=self.i.name())
        plt.plot(self.voi.values(), self.i_c.values(), label=self.i_c.name())
        plt.plot(self.voi.values(), self.i_u.values(), label=self.i_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 3)
        plt.plot(self.voi.values(), self.r.values(), label=self.r.name())
        plt.plot(self.voi.values(), self.r_c.values(), label=self.r_c.name())
        plt.plot(self.voi.values(), self.r_u.values(), label=self.r_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 4)
        plt.plot(self.voi.values(), self.ifr.values(), label=self.ifr.name())
        plt.legend(loc='center left')
        plt.xlabel('time (day)')

        plt.show()
