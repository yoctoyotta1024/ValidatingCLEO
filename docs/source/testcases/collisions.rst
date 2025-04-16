.. _collisions:

Collisions
==========

Test-case based on reproducing figure 2 of :cite:`shima2009`.

Compile Program
---------------

First build and compile the test case using the ``./scripts/build_compile.sh`` helper script.
E.g. for a OpenMP build in ``/work/bm1183/m300950/validating_cleo/build`` using the intel compiler
and source directory in ``/home/m/m300950/validating_cleo/src/``:

.. code-block:: console

  $ ./scripts/build_compile.sh \
      openmp \
      intel \
      /home/m/m300950/validating_cleo/src/ \
      /work/bm1183/m300950/validating_cleo/build

Then compile the example with:

.. code-block:: console

  $ ./scripts/compile_only.sh \
      colls_golovin \
      openmp \
      intel \
      /home/m/m300950/validating_cleo/src/ \
      /work/bm1183/m300950/validating_cleo/build


Initial conditions
------------------

First use ``scripts/collisions/initconds.py`` to generate the configuration files, the initial
superdroplet condition and gridbox binary files. E.g. with pySD module in ``/home/m/m300950/CLEO/``
for a build in ``/work/bm1183/m300950/validating_cleo/build``, and with plots of the initial
conditions, you would run:

.. code-block:: console

  $ python ./scripts/collisions/initconds.py \
      /home/m/m300950/CLEO \
      /work/bm1183/m300950/validating_cleo/build \
      /home/m/m300950/validating_cleo/src/collisions/config.yaml \
      TRUE TRUE


Run Model
---------

Use ``./scripts/run.sh`` to run the executable (or ``./scripts/run_gpu.sh`` for gpu SLURM settings).
E.g.

.. code-block:: console

  $ ./scripts/collisions/run_allcollisions.sh \
      /work/bm1183/m300950/validating_cleo/build \
      openmp

Plot Results
------------

Plot the results of the model run using the python script ``./scripts/collisions/plot_results.py``.
E.g.

.. code-block:: console

  $ python ./scripts/collisions/plot_results.py \
      /home/m/m300950/CLEO \
      /work/bm1183/m300950/validating_cleo/build/share/collisions/dimlessGBxboundaries.dat \
      /work/bm1183/m300950/validating_cleo/build/bin/collisions \
      /work/bm1183/m300950/validating_cleo/build/bin/collisions
