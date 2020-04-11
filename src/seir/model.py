import opencor as oc


class Model:
    """
    SEIR model of Covid-19, as described at
    https://cpb-ap-se2.wpmucdn.com/blogs.auckland.ac.nz/dist/d/75/files/2017/01/Covid19_SEIR_model.pdf.
    """

    def __init__(self, sim_duration=300):
        # Initialise our SEIR simulation.

        self.simulation = oc.open_simulation(
            'https://raw.githubusercontent.com/ABI-Covid-19/seir/master/models/seir.sedml')

        self.set_sim_duration(sim_duration)

    def set_sim_duration(self, sim_duration):
        # Set the duration of our SEIR simulation.

        self.simulation.data().set_ending_point(sim_duration)

    def run(self):
        # Reset and run our SEIR simulation.

        self.simulation.reset()  # In case another simulation had already been run.
        self.simulation.run()

        # Retrieve the results of the simulation.

        results = self.simulation.results()

        voi = results.voi()
        states = results.states()
        algebraic = results.algebraic()

        s = states['main/S']
        e = states['main/E']
        i_c = states['main/I_c']
        i_p = states['main/I_p']
        i_u = states['main/I_u']
        r_c = states['main/R_c']
        r_u = states['main/R_u']

        i = algebraic['main/I']
        r = algebraic['main/R']
        d = algebraic['main/D']
        ifr = algebraic['main/IFR']

        # Plot the results.

        import matplotlib.pyplot as plt

        plt.clf()  # In case there is already a Matplotlib window.
        plt.gcf().canvas.set_window_title('SEIR model')

        plt.subplot(4, 1, 1)
        plt.plot(voi.values(), s.values(), label=s.name())
        plt.plot(voi.values(), e.values(), label=e.name())
        plt.plot(voi.values(), i_p.values(), label=i_p.name())
        plt.plot(voi.values(), i.values(), label=i.name())
        plt.plot(voi.values(), r.values(), label=r.name())
        plt.plot(voi.values(), d.values(), label=d.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 2)
        plt.plot(voi.values(), i.values(), label=i.name())
        plt.plot(voi.values(), i_c.values(), label=i_c.name())
        plt.plot(voi.values(), i_u.values(), label=i_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 3)
        plt.plot(voi.values(), r.values(), label=r.name())
        plt.plot(voi.values(), r_c.values(), label=r_c.name())
        plt.plot(voi.values(), r_u.values(), label=r_u.name())
        plt.legend(loc='center left')

        plt.subplot(4, 1, 4)
        plt.plot(voi.values(), ifr.values(), label=ifr.name())
        plt.legend(loc='center left')
        plt.xlabel('time (day)')

        plt.show()
