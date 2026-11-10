PyAutoCTI: Charge Transfer Inefficiency Modeling
================================================

.. image:: https://raw.githubusercontent.com/PyAutoLabs/PyAutoCTI/main/docs/overview/images/what_is_cti.png
   :width: 600
   :alt: Charge transfer inefficiency in Hubble imaging

**PyAutoCTI** lets you simulate, calibrate and correct charge transfer inefficiency (CTI) in CCD detectors. CTI occurs when defects in the detector trap and release electrons during readout, leaving trails in the image.

Getting Started
---------------

Explore It Yourself
~~~~~~~~~~~~~~~~~~~

- `What is CTI? <https://pyautocti.readthedocs.io/en/latest/overview/overview_1_what_is_cti.html>`_ — learn about CTI and how it affects your data.
- `Install PyAutoCTI <https://pyautocti.readthedocs.io/en/latest/installation/overview.html>`_ — get set up on your computer.
- `Find examples <https://github.com/PyAutoLabs/autocti_workspace#find-your-examples>`_ — explore simulation, calibration and correction in the workspace.

Explore with AI
~~~~~~~~~~~~~~~

The `PyAutoCTI AI Assistant <https://github.com/PyAutoLabs/autocti_assistant>`_ helps you learn about CTI and work through calibration examples through conversation. To get started, paste this prompt into your AI coding agent:

.. code-block:: text

   I want to learn about CTI and use PyAutoCTI
   (https://github.com/PyAutoLabs/PyAutoCTI) with the
   autocti_assistant (https://github.com/PyAutoLabs/autocti_assistant).

   First clone the assistant repository, cd into it and follow its AGENTS.md.
   Explain CTI, then guide me through the introductory calibration demonstration.

See `AI Options <https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md>`_ for tools and setup guidance.

Learn About CTI
---------------

The `overview examples <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/overview>`_ introduce parallel and serial charge transfer, charge injection data, and how to fit and calibrate a CTI model.

The `PyAutoCTI documentation <https://pyautocti.readthedocs.io/en/latest/index.html>`_ covers the software’s features and how to use them in your own analysis. PyAutoCTI uses `arCTIc <https://github.com/jkeger/arctic>`_ to simulate charge transfer through the detector.

Community and Contributing
--------------------------

Ask questions, suggest improvements and share your work in `PyAutoLabs Discussions <https://github.com/orgs/PyAutoLabs/discussions>`_.

To contribute, see the `contribution guide <https://github.com/PyAutoLabs/PyAutoCTI/blob/main/CONTRIBUTING.md>`_.

Citations
---------

If you use PyAutoCTI in your research, see the `citation guide <https://github.com/PyAutoLabs/PyAutoCTI/blob/main/CITATIONS.rst>`_.

License
-------

See the `license <https://github.com/PyAutoLabs/PyAutoCTI/blob/main/LICENSE>`_.
