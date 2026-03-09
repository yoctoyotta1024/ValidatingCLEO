.. _collisions:

Collisions
==========

Test-case based on reproducing figure 2 of :cite:`shima2009`.

Compile Program
---------------

First build and compile the test case using the ``./scripts/build_compile.sh`` helper script.
E.g. for a OpenMP build in ``/work/mh0731/m300950/validating_cleo/build`` using the intel compiler
and source directory in ``/home/m/m300950/validating_cleo/src/``:

.. code-block:: console

  $ ./scripts/build_compile.sh \
      openmp \
      intel \
      /home/m/m300950/validating_cleo/src/ \
      /work/mh0731/m300950/validating_cleo/build

Then compile the example with:

.. code-block:: console

  $ ./scripts/compile_only.sh \
      colls_golovin \
      openmp \
      intel \
      /home/m/m300950/validating_cleo/src/ \
      /work/mh0731/m300950/validating_cleo/build


Initial conditions
------------------

First use ``scripts/collisions/initconds.py`` to generate the configuration files, the initial
superdroplet condition and gridbox binary files. E.g. with pySD module in ``/home/m/m300950/CLEO/``
for a build in ``/work/mh0731/m300950/validating_cleo/build``, and with plots of the initial
conditions, you would run:

.. code-block:: console

  $ python ./scripts/collisions/initconds.py \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build \
      /home/m/m300950/validating_cleo/src/collisions/config.yaml \
      TRUE TRUE


Run Model
---------

Use ``./scripts/run_allcollisions.sh`` to run all the executables.
E.g.

.. code-block:: console

  $ ./scripts/collisions/run_allcollisions.sh \
      /work/mh0731/m300950/validating_cleo/build \
      openmp

Plot Results
------------

Plot the results of the model run using the python script ``./scripts/collisions/plot_results.py``.
E.g.

.. code-block:: console

  $ python ./scripts/collisions/plot_results.py \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build/share/collisions/dimlessGBxboundaries.dat \
      /work/mh0731/m300950/validating_cleo/build/bin/collisions \
      /work/mh0731/m300950/validating_cleo/build/bin/collisions


Breakup Comparison
------------------

To compare the results of the collision test cases including breakup, first build and compile the
breakup excutables ``colls_testikstraub`` and ``colls_testikstraub_fixednfrags`` as above.

The generate the initial conditons similarly but with the ``initconds_compare_breakup.py`` script
and ``config_compare_breakup.yaml``.
E.g.

.. code-block:: console

  $ python ./scripts/collisions/initconds_compare_breakup.py \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build \
      /home/m/m300950/validating_cleo/src/collisions/config_compare_breakup.yaml \
      TRUE TRUE

Similarly use ``./scripts/run_compare_breakup.sh`` to run the executables.
E.g.

.. code-block:: console

  $ ./scripts/collisions/run_compare_breakup.sh \
      /work/mh0731/m300950/validating_cleo/build \
      openmp

Similarly plot the results of the model runs using the python script
``./scripts/collisions/plot_compare_breakup.py``.
E.g.

.. code-block:: console

  $ python ./scripts/collisions/plot_compare_breakup.py`` \
      /home/m/m300950/CLEO \
      /work/mh0731/m300950/validating_cleo/build/share/collisions/dimlessGBxboundaries.dat \
      /work/mh0731/m300950/validating_cleo/build/bin/collisions \
      /work/mh0731/m300950/validating_cleo/build/bin/collisions
