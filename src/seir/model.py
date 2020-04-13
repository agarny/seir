import numpy as np
import opencor as oc


class Model:
    """
    SEIR model of Covid-19, as described at
    https://cpb-ap-se2.wpmucdn.com/blogs.auckland.ac.nz/dist/d/75/files/2017/01/Covid19_SEIR_model.pdf.
    """

    def __init__(self):
        # Initialise our SEIR simulation.

        self.simulation = oc.open_simulation(
            'https://raw.githubusercontent.com/ABI-Covid-19/seir/master/models/seir.sedml')

    def run(self, sim_duration=300):
        # Make sure that we were given a valid simulation duration.

        if sim_duration <= 0:
            print('The simulation duration (', sim_duration, ') must be greater than 0 (days).', sep='')

            return

        # Reset and run our SEIR simulation.

        self.simulation.reset()  # In case another simulation had already been run.

        run_nb = 0

        results = self.simulation.results()

        states = results.states()
        algebraic = results.algebraic()

        voi = results.voi()
        voi_values = np.array([])

        s = states['main/S']
        s_values = np.array([])

        e = states['main/E']
        e_values = np.array([])

        i_c = states['main/I_c']
        i_c_values = np.array([])

        i_p = states['main/I_p']
        i_p_values = np.array([])

        i_u = states['main/I_u']
        i_u_values = np.array([])

        r_c = states['main/R_c']
        r_c_values = np.array([])

        r_u = states['main/R_u']
        r_u_values = np.array([])

        i = algebraic['main/I']
        i_values = np.array([])

        r = algebraic['main/R']
        r_values = np.array([])

        d = algebraic['main/D']
        d_values = np.array([])

        ifr = algebraic['main/IFR']
        ifr_values = np.array([])

        while sim_duration > 0:
            # Run the simulation one day at a time.

            self.simulation.data().set_ending_point(1 if sim_duration >= 1 else sim_duration)

            self.simulation.run()

            sim_duration -= 1

            # Update our simulation results using the results of the current
            # simulation.

            voi_values = np.append(voi_values, run_nb + voi.values())
            s_values = np.append(s_values, s.values())
            e_values = np.append(e_values, e.values())
            i_c_values = np.append(i_c_values, i_c.values())
            i_p_values = np.append(i_p_values, i_p.values())
            i_u_values = np.append(i_u_values, i_u.values())
            r_c_values = np.append(r_c_values, r_c.values())
            r_u_values = np.append(r_u_values, r_u.values())
            i_values = np.append(i_values, i.values())
            r_values = np.append(r_values, r.values())
            d_values = np.append(d_values, d.values())
            ifr_values = np.append(ifr_values, ifr.values())

            run_nb += 1

        # Plot the results.

        import matplotlib.pyplot as plt

        plt.clf()  # In case there is already a Matplotlib window.
        plt.gcf().canvas.set_window_title('SEIR model')

        plt.subplot(4, 1, 1)
        plt.plot(voi_values, s_values, label=s.name())
        plt.plot(voi_values, e_values, label=e.name())
        plt.plot(voi_values, i_p_values, label=i_p.name())
        plt.plot(voi_values, i_values, label=i.name())
        plt.plot(voi_values, r_values, label=r.name())
        plt.plot(voi_values, d_values, label=d.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 2)
        plt.plot(voi_values, i_values, label=i.name())
        plt.plot(voi_values, i_c_values, label=i_c.name())
        plt.plot(voi_values, i_u_values, label=i_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 3)
        plt.plot(voi_values, r_values, label=r.name())
        plt.plot(voi_values, r_c_values, label=r_c.name())
        plt.plot(voi_values, r_u_values, label=r_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 4)
        plt.plot(voi_values, ifr_values, label=ifr.name())
        plt.legend(loc='center left')
        plt.xlabel('time (day)')

        plt.show()
