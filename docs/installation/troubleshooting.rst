.. _troubleshooting:

Troubleshooting
===============

arcticpy
--------

Most installation problems come from arcticpy, the package that runs arCTIc. Its install steps are on the
`arCTIc page <https://pyautocti.readthedocs.io/en/latest/installation/arctic.html>`_. These are the usual errors.

**GSL not found.** The build stops with a compiler error mentioning ``gsl/gsl_*.h``, or a ``gsl`` library it cannot
find. Install GSL and run the arcticpy install again:

.. code-block:: bash

    sudo apt-get install -y libgsl-dev   # Debian / Ubuntu
    brew install gsl                     # macOS

**numpy was downgraded.** If ``pip`` replaced numpy 2 with numpy 1.x while installing arcticpy, you ran a plain
``pip install arcticpy``, which fetched version 2.6 or older. Put numpy back, then follow the arCTIc page:

.. code-block:: bash

    pip uninstall -y arcticpy
    pip install "numpy>=2"

**Cannot import 'setuptools.build_meta'.** The build tools are missing. Recent Python versions no longer include
``setuptools`` in a new virtual environment. Run ``pip install --upgrade pip setuptools wheel`` and try again.

**No module named scipy or matplotlib when importing arcticpy.** The install uses ``--no-deps``, so these are
installed separately: ``pip install scipy matplotlib``.

**Last resort: arcticpy without GSL.** If you cannot install GSL at all, an older package built without it exists:

.. code-block:: bash

    pip install arcticpy_no_gsl

It predates arcticpy 2.7 and has not been tested with numpy 2 or the current **PyAutoCTI**. Like a plain
``pip install arcticpy``, it may downgrade numpy below 2.0, so use it only when the recipe on the arCTIc page is not
an option, and check ``pip show numpy`` afterwards.

Current Working Directory
-------------------------

**PyAutoCTI** scripts assume that the ``autocti_workspace`` directory is the Python working directory. This means
that, when you run an example script, you should run it from the ``autocti_workspace`` as follows:

.. code-block:: bash

    cd path/to/autocti_workspace (if you are not already in the autocti_workspace).
    python3 scripts/dataset_fit/modeling/start_here.py

The reasons for this are so that **PyAutoCTI** can:

 - Load configuration settings from config files in the ``autocti_workspace/config`` folder.
 - Load example data from the ``autocti_workspace/dataset`` folder.
 - Output the results of models fits to your hard-disk to the ``autocti/output`` folder.
 - Import modules from the ``autocti_workspace``, for example ``from autocti_workspace.transdimensional import pipelines``.

If you have any errors relating to importing modules, loading data or outputting results it is likely because you
are not running the script with the ``autocti_workspace`` as the working directory!

Matplotlib Backend
------------------

Matplotlib uses the default backend on your computer, as set in the config file:

.. code-block:: bash

    autocti_workspace/config/visualize/general.ini

If unchanged, the backend is set to 'default', meaning it will use the backend automatically set up for Python on
your system.

.. code-block:: bash

    general:
      backend: default

There have been reports that using the default backend causes crashes when running the test script below (either the
code crashes without a error or your computer restarts). If this happens, change the config's backend until the test
works (TKAgg has worked on Linux machines, Qt5Agg has worked on new MACs). For example:

.. code-block:: bash

    general:
      backend: TKAgg

Support
-------

If you are still having issues with installation or using **PyAutoCTI** in general, please raise an issue on the
`autocti_workspace issues page <https://github.com/Jammy2211/autocti_workspace/issues>`_ with a description of the
problem and your system setup (operating system, Python version, etc.).