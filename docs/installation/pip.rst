.. _pip:

Installation with pip
=====================

Install
-------

We strongly recommend that you install **PyAutoCTI** in a
`Python virtual environment <https://www.geeksforgeeks.org/python-virtual-environment/>`_, with the link attached
describing what a virtual environment is and how to create one.

.. code-block:: bash

    pip install --upgrade pip

The latest version of **PyAutoCTI** is installed via pip as follows (specifying the version as shown below ensures
the installation has clean dependencies):

.. code-block:: bash

    pip install autocti

If this raises no errors **PyAutoCTI** is installed!

arCTIc
------

arCTIc is the C++ code that clocks charge through a CCD, and **PyAutoCTI** uses it through the Python package
``arcticpy``. You can ``import autocti`` without it, so it is fine to skip this step while you look around, but
fitting or simulating CTI needs it.

``arcticpy`` is built from source on your computer, so it needs the GSL maths library first:

.. code-block:: bash

    sudo apt-get install -y libgsl-dev   # Debian / Ubuntu
    brew install gsl                     # macOS

Then install arcticpy 2.7:

.. code-block:: bash

    pip install --upgrade pip setuptools wheel
    pip install "numpy>=2" "cython>=3" scipy matplotlib
    pip install "arcticpy @ git+https://github.com/jkeger/arctic@6f5153582aca00b7b0cc11ab04b2c58a7502400d" --no-build-isolation --no-deps

arcticpy 2.7 is not on PyPI yet, so the last line builds it from a fixed version on GitHub.
Once it is on PyPI, that line becomes ``pip install arcticpy==2.7 --no-build-isolation --no-deps``. A plain
``pip install arcticpy`` installs an older version that does not work with numpy 2, so don't use it.

Check it worked:

.. code-block:: bash

    python -c "import arcticpy; print('arcticpy OK')"

The `arCTIc page <https://pyautocti.readthedocs.io/en/latest/installation/arctic.html>`_ explains each step, and
the `troubleshooting section <https://pyautocti.readthedocs.io/en/latest/installation/troubleshooting.html>`_ covers
the common errors.

Numba
-----

Numba (https://numba.pydata.org)  is an optional library which makes **PyAutoCTI** run a lot faster, which we
strongly recommend users have installed.

You can install numba via the following command:

.. code-block:: bash

    pip install numba

Some users have experienced difficulties installing numba, which is why it is an optional library. If your
installation is not successful, you can use **PyAutoCTI** without it installed for now, to familiarize yourself
with the software and determine if it is the right software for you.

If you decide that **PyAutoCTI** is the right software, then I recommend you commit the time to getting a
successful numba install working, with more information provided `at this readthedocs page <https://pyautocti.readthedocs.io/en/latest/installation/numba.html>`_

Workspace
---------

Next, clone the ``autocti workspace`` (the line ``--depth 1`` clones only the most recent branch on
the ``autocti_workspace``, reducing the download size):

.. code-block:: bash

   cd /path/on/your/computer/you/want/to/put/the/autocti_workspace
   git clone https://github.com/Jammy2211/autocti_workspace --depth 1
   cd autocti_workspace

Run the ``welcome.py`` script to get started!

.. code-block:: bash

   python3 welcome.py

It should be clear that **PyAutoCTI** runs without issue.

If there is an error check out the `troubleshooting section <https://pyautocti.readthedocs.io/en/latest/installation/troubleshooting.html>`_.