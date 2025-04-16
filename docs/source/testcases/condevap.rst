.. _condevap:

Condensation/Evaporation
========================

Test-case based on reproducing figure 7 of :cite:`arabasshima2017`.

Compile Program
---------------

First build and compile the test case using the ``./scripts/build_compile.sh`` helper script.
E.g. for a serial build in ``/work/bm1183/m300950/validating_cleo/build`` using the intel compiler
and source directory in ``/home/m/m300950/validating_cleo/src/``:

.. code-block:: console

  $ ./scripts/build_compile.sh \
      serial \
      intel \
      /home/m/m300950/validating_cleo/src/ \
      /work/bm1183/m300950/validating_cleo/build

Then compile the example with:

.. code-block:: console

  $ ./scripts/compile_only.sh \
      condevap \
      serial \
      intel \
      /home/m/m300950/validating_cleo/src/ \
      /work/bm1183/m300950/validating_cleo/build


Initial conditions
------------------

First use ``scripts/condevap/initconds.py`` to generate the configuration files, the initial
superdroplet condition and gridbox binary files. E.g. with pySD module in ``/home/m/m300950/CLEO/``
for a build in ``/work/bm1183/m300950/validating_cleo/build``, and with plots of the initial
conditions, you would run:

.. code-block:: console

  $ python ./scripts/condevap/initconds.py \
      /home/m/m300950/CLEO \
      /work/bm1183/m300950/validating_cleo/build \
      /home/m/m300950/validating_cleo/src/condevap/config.yaml \
      TRUE TRUE


Run Model
---------

Use ``./scripts/run.sh`` to run the executable (or ``./scripts/run_gpu.sh`` for gpu SLURM settings).
E.g.

.. code-block:: console

  $ ./scripts/run.sh \
      /work/bm1183/m300950/validating_cleo/build \
      serial \
      /work/bm1183/m300950/validating_cleo/build/condevap/condevap \
      /work/bm1183/m300950/validating_cleo/build/tmp/condevap/config_0.yaml


Plot Results
------------

Plot the results of the model run using the python script ``./scripts/condevap/plot_results.py``.
E.g.

.. code-block:: console

  $ python ./scripts/condevap/plot_results.py \
      /home/m/m300950/CLEO \
      /work/bm1183/m300950/validating_cleo/build/share/condevap/dimlessGBxboundaries.dat \
      /work/bm1183/m300950/validating_cleo/build/bin/condevap \
      /work/bm1183/m300950/validating_cleo/build/bin/condevap
