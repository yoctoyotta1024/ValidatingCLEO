.. _getstart:

Getting Started
===============

Clone ValidatingCLEO's GitHub repository:

.. code-block:: console

  $ git clone https://github.com/yoctoyotta1024/ValidatingCLEO.git

and then create an environment with the necessary dependencies installed (using micromamba, or
conda as listed in the environment.yml):

.. code-block:: console

  $ conda env create --file environment.yml --prefix [name for your environment]
  $ conda activate [name of your environment]

Finally install the pre-commit hooks:

.. code-block:: console

  $ pre-commit install

which will be used when you try to commit something or you execute ``pre-commit run``. You can learn
more about the powers of pre-commit from `their documentation <https://pre-commit.com>`_.

For now, CLEO's python packages are not readily installable and so you will have to clone the
CLEO repository to somewhere in your filesystem and checkout to CLEO version v0.39.1:

.. code-block:: console

  $ git clone https://github.com/yoctoyotta1024/CLEO.git
  $ cd CLEO && git checkout -b v0.39.1

That's it, you're done! Now maybe you want to compile and run one of the test cases in ``src/``.
