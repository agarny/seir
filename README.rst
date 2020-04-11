SEIR
====

An `OpenCOR <https://opencor.ws/>`_-based Python script to model Covid-19 using the `SEIR model <https://cpb-ap-se2.wpmucdn.com/blogs.auckland.ac.nz/dist/d/75/files/2017/01/Covid19_SEIR_model.pdf>`_.

Install/upgrade
---------------

From OpenCOR's ``Python Console`` window::

 !pip install -U git+https://github.com/ABI-Covid-19/seir.git

Uninstall
---------

From OpenCOR's ``Python Console`` window::

 !pip uninstall -y seir

Use
---

From OpenCOR's ``Python Console`` window::

 import seir  # Import the SEIR module.

 m = seir.Model()  # Create an instance of the SEIR model.

 m.run()  # Run the simulation for 300 days (default).
 m.run(150)  # Re-run the simulation for 150 days.
 m.run(450)  # Re-run the simulation for 450 days.

For the first simulation, you should get something like:

.. image:: res/screenshot.png
