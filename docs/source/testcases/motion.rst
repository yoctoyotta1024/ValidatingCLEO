.. _motion:

Motion
======

Test-case based on reproducing similar plot to figure 1 of :cite:`arabas2015` by
plotting superdroplet tracer particles in 2-D divergence free flow.

Compile Program
---------------

First build and compile the test case using the ``./scripts/build_compile.sh`` helper script.
E.g. for a C++threads build in ``/work/bm1183/m300950/validating_cleo/build`` using the gcc
compiler and source directory in ``/home/m/m300950/validating_cleo/src/``:

.. code-block:: console

  $ ./scripts/build_compile.sh \
      threads \
      gcc \
      /home/m/m300950/validating_cleo/src/ \
      /work/bm1183/m300950/validating_cleo/build

Then compile the example with:

.. code-block:: console

  $ ./scripts/compile_only.sh \
      motion \
      threads \
      gcc \
      /home/m/m300950/validating_cleo/src/ \
      /work/bm1183/m300950/validating_cleo/build


Initial conditions
------------------

First use ``scripts/motion/initconds.py`` to generate the configuration files, the initial
superdroplet condition and gridbox binary files. E.g. with pySD module in ``/home/m/m300950/CLEO/``
for a build in ``/work/bm1183/m300950/validating_cleo/build``, and with plots of the initial
conditions, you would run:

.. code-block:: console

  $ python ./scripts/motion/initconds.py \
      /home/m/m300950/CLEO \
      /work/bm1183/m300950/validating_cleo/build \
      /home/m/m300950/validating_cleo/src/motion/config.yaml \
      TRUE TRUE


Run Model
---------

Use ``./scripts/run.sh`` to run the executable (or ``./scripts/run_gpu.sh`` for gpu SLURM settings).
E.g.

.. code-block:: console

  $ ./scripts/run.sh \
      /work/bm1183/m300950/validating_cleo/build \
      threads \
      /work/bm1183/m300950/validating_cleo/build/motion/motion \
      /work/bm1183/m300950/validating_cleo/build/tmp/motion/config_0.yaml


Plot Results
------------

Plot the results of the model run using the python script ``./scripts/motion/plot_results.py``.
E.g.

.. code-block:: console

  $ ./scripts/motion/plot_results.sh \
      /work/bm1183/m300950/bin/envs/validatecleo/bin/python \
      /home/m/m300950/validating_cleo \
      /home/m/m300950/CLEO \
      /work/bm1183/m300950/validating_cleo/build/bin/motion \
      /work/bm1183/m300950/validating_cleo/build/bin/motion
