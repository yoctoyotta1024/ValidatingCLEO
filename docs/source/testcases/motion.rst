.. _motion:

Motion
======

Test-case based on reproducing similar plot to figure 1 of :cite:`arabas2015` by
plotting superdroplet tracer particles in 2-D divergence free flow.

Compile Program
---------------

First build and compile the test case using the ``./scripts/build_compile.sh`` helper script.
E.g. for a C++threads build in ``/work/mh0731/m300950/validating_cleo/build`` using the gcc
compiler and source directory in ``/home/m/m300950/validating_cleo/src/``:

.. code-block:: console

  $ ./scripts/build_compile.sh \
      threads \
      gcc \
      /home/m/m300950/validating_cleo/src/ \
      /work/mh0731/m300950/validating_cleo/build

Then compile the example with:

.. code-block:: console

  $ ./scripts/compile_only.sh \
      motion \
      threads \
      gcc \
      /home/m/m300950/validating_cleo/src/ \
      /work/mh0731/m300950/validating_cleo/build


Initial conditions
------------------

First use ``scripts/motion/initconds.py`` to generate the configuration files, the initial
superdroplet condition and gridbox binary files. E.g. with pySD module in ``/home/m/m300950/CLEO/``
for a build in ``/work/mh0731/m300950/validating_cleo/build``, and with plots of the initial
conditions, you would run:

.. code-block:: console

  $ python ./scripts/motion/initconds.py \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build \
      /home/m/m300950/validating_cleo/src/motion/config.yaml \
      TRUE TRUE


Run Model
---------

Use ``./scripts/run.sh`` to run the executable (or ``./scripts/run_gpu.sh`` for gpu SLURM settings).
E.g.

.. code-block:: console

  $ ./scripts/run.sh \
      /work/mh0731/m300950/validating_cleo/build \
      threads \
      /work/mh0731/m300950/validating_cleo/build/motion/motion \
      /work/mh0731/m300950/validating_cleo/build/tmp/motion/config_0.yaml


Plot Results
------------

Plot the results of the model run using the python script ``./scripts/motion/plot_results.py``.
E.g.

.. code-block:: console

  $ ./scripts/motion/plot_results.sh \
      /home/m/m300950/mamba/envs/validatecleo/bin/python \
      /home/m/m300950/validating_cleo \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build/bin/motion \
      /work/mh0731/m300950/validating_cleo/build/bin/motion

Running with Terminal Velocity
------------------------------

To run the same model but with droplet growth via condensation/evaporation followed by them falling
with their terminal velocity, repeat as above but using the ``motion_with_tvel`` executable
and the ``config_with_tvel.yaml`` config file.

*Note*: A run with the ``motion_with_tvel`` executable using the ``config_with_tvel.yaml``
config will overwrite the input files and results of the former ``motion`` run, so make sure to move
the results of the first run to a different directory before running the second run.

.. code-block:: console

  $ ./scripts/compile_only.sh \
      motion_with_tvel \
      threads \
      gcc \
      /home/m/m300950/validating_cleo/src/ \
      /work/mh0731/m300950/validating_cleo/build

  $ python ./scripts/motion/initconds.py \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build \
      /home/m/m300950/validating_cleo/src/motion/config_with_tvel.yaml \
      TRUE TRUE

  $ ./scripts/run.sh \
      /work/mh0731/m300950/validating_cleo/build \
      threads \
      /work/mh0731/m300950/validating_cleo/build/motion/motion_with_tvel \
      /work/mh0731/m300950/validating_cleo/build/tmp/motion/config_0.yaml

  $ ./scripts/motion/plot_results.sh \
      /home/m/m300950/mamba/envs/validatecleo/bin/python \
      /home/m/m300950/validating_cleo \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build/bin/motion_with_tvel \
      /work/mh0731/m300950/validating_cleo/build/bin/motion_with_tvel
