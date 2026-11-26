.. _arctic:

Installing arCTIc
=================

**arCTIc**, the AlgoRithm for Charge Transfer Inefficiency (CTI) Correction, is the C++ code that models how charge
moves through a CCD as it is read out, including the effects of CTI. **PyAutoCTI** uses it through the Python package
``arcticpy``.

You need it to fit or simulate CTI. You don't need it to ``import autocti``: **PyAutoCTI** only loads arcticpy when
it clocks charge, so you can install **PyAutoCTI**, explore the workspace and add arcticpy afterwards.

``pip install autocti`` does not install arcticpy. Install it yourself with the steps below.

Install
-------

First install the GSL maths library, which arcticpy needs to build:

.. code-block:: bash

    sudo apt-get install -y libgsl-dev   # Debian / Ubuntu
    brew install gsl                     # macOS

Then, in the same Python environment as **PyAutoCTI**:

.. code-block:: bash

    pip install --upgrade pip setuptools wheel
    pip install "numpy>=2" "cython>=3" scipy matplotlib
    pip install "arcticpy @ git+https://github.com/jkeger/arctic@6f5153582aca00b7b0cc11ab04b2c58a7502400d" --no-build-isolation --no-deps

arcticpy 2.7 is the first version that works with numpy 2. It is not on PyPI yet, so the last line builds it from a
fixed version on GitHub. Once 2.7 is on PyPI, that line becomes:

.. code-block:: bash

    pip install arcticpy==2.7 --no-build-isolation --no-deps

Don't run a plain ``pip install arcticpy``. It installs version 2.6 or older, which downgrades numpy below 2.0 and
breaks the rest of your **PyAutoCTI** install.

Check it worked
---------------

.. code-block:: bash

    python -c "import arcticpy; print('arcticpy OK')"
    pip show arcticpy

``pip show`` should report ``Version: 2.7``.

Why each step is there
----------------------

arcticpy is shipped as C++ source code, not a ready-built package, so pip compiles it on your computer. The extra
flags keep that build from disturbing the rest of your environment:

- **GSL** is a C library arcticpy links against. Without its headers the build stops with a compiler error that
  mentions ``gsl``.
- **--no-build-isolation** builds arcticpy against the numpy already in your environment, instead of pip fetching a
  separate one. In return, the build tools (``setuptools``, ``wheel``, ``numpy`` and ``cython``) must be installed
  first, which is what the first two lines do.
- **--no-deps** stops pip from changing your other packages, including numpy. In return, the packages arcticpy needs
  when it runs (``scipy`` and ``matplotlib``) must be installed by hand, which the second line also does.

The **PyAutoCTI** test and documentation builds install arcticpy the same way. The maintained copy of the recipe is the
`install_arcticpy.sh <https://github.com/PyAutoLabs/PyAutoHeart/blob/main/.github/actions/install-arcticpy/install_arcticpy.sh>`_
script, which also checks for GSL and verifies the import.

If something goes wrong, see the `troubleshooting section <https://pyautocti.readthedocs.io/en/latest/installation/troubleshooting.html>`_
or arCTIc's own `GitHub page <https://github.com/jkeger/arctic>`_.
