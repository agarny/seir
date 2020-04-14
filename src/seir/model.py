import os

import numpy as np
import opencor as oc


class Model:
    """
    SEIR model of Covid-19, as described at
    https://cpb-ap-se2.wpmucdn.com/blogs.auckland.ac.nz/dist/d/75/files/2017/01/Covid19_SEIR_model.pdf.
    """

    def __init__(self):
        # Initialise our SEIR simulation.

        self.simulation = oc.open_simulation(os.path.dirname(__file__) + '/models/seir.sedml')

        # Keep track of various model parameters.

        results = self.simulation.results()

        states = results.states()
        algebraic = results.algebraic()

        self.voi = results.voi()
        self.voi_values = np.array([])

        self.s = states['main/S']
        self.s_values = np.array([])

        self.e = states['main/E']
        self.e_values = np.array([])

        self.i_c = states['main/I_c']
        self.i_c_values = np.array([])

        self.i_p = states['main/I_p']
        self.i_p_values = np.array([])

        self.i_u = states['main/I_u']
        self.i_u_values = np.array([])

        self.r_c = states['main/R_c']
        self.r_c_values = np.array([])

        self.r_u = states['main/R_u']
        self.r_u_values = np.array([])

        self.i = algebraic['main/I']
        self.i_values = np.array([])

        self.r = algebraic['main/R']
        self.r_values = np.array([])

        self.d = algebraic['main/D']
        self.d_values = np.array([])

        self.ifr = algebraic['main/IFR']
        self.ifr_values = np.array([])

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

            self.voi_values = np.append(self.voi_values, run_nb + self.voi.values())
            self.s_values = np.append(self.s_values, self.s.values())
            self.e_values = np.append(self.e_values, self.e.values())
            self.i_c_values = np.append(self.i_c_values, self.i_c.values())
            self.i_p_values = np.append(self.i_p_values, self.i_p.values())
            self.i_u_values = np.append(self.i_u_values, self.i_u.values())
            self.r_c_values = np.append(self.r_c_values, self.r_c.values())
            self.r_u_values = np.append(self.r_u_values, self.r_u.values())
            self.i_values = np.append(self.i_values, self.i.values())
            self.r_values = np.append(self.r_values, self.r.values())
            self.d_values = np.append(self.d_values, self.d.values())
            self.ifr_values = np.append(self.ifr_values, self.ifr.values())

            run_nb += 1

        # Plot the results.

        import matplotlib.pyplot as plt

        plt.clf()  # In case there is already a Matplotlib window.
        plt.gcf().canvas.set_window_title('SEIR model')

        plt.subplot(4, 1, 1)
        plt.plot(self.voi_values, self.s_values, label=self.s.name())
        plt.plot(self.voi_values, self.e_values, label=self.e.name())
        plt.plot(self.voi_values, self.i_p_values, label=self.i_p.name())
        plt.plot(self.voi_values, self.i_values, label=self.i.name())
        plt.plot(self.voi_values, self.r_values, label=self.r.name())
        plt.plot(self.voi_values, self.d_values, label=self.d.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 2)
        plt.plot(self.voi_values, self.i_values, label=self.i.name())
        plt.plot(self.voi_values, self.i_c_values, label=self.i_c.name())
        plt.plot(self.voi_values, self.i_u_values, label=self.i_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 3)
        plt.plot(self.voi_values, self.r_values, label=self.r.name())
        plt.plot(self.voi_values, self.r_c_values, label=self.r_c.name())
        plt.plot(self.voi_values, self.r_u_values, label=self.r_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 4)
        plt.plot(self.voi_values, self.ifr_values, label=self.ifr.name())
        plt.legend(loc='center left')
        plt.xlabel('time (day)')

        plt.show()
