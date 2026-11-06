========
Plotting
========

Create figures and subplots of **PyAutoCTI** datasets, fits and non-linear search results.

The plotting API is **functional**: import ``autocti.plot`` and call a plot function directly, passing it the
dataset or fit to plot. There are no ``Plotter`` classes to configure first.

.. code-block:: python

   import autocti.plot as aplt

   aplt.subplot_imaging_ci(dataset=dataset)
   aplt.subplot_fit_ci(fit=fit, output_path="output", output_format="png")

By default a figure is shown interactively. Pass ``output_path`` and ``output_format`` (e.g. ``"png"`` or
``"pdf"``) to write it to disk instead.

**Examples / Tutorials:**

- `autocti_workspace: plot tutorials <https://github.com/PyAutoLabs/autocti_workspace/tree/main/notebooks/plot>`_

Dataset 1D [aplt]
-----------------

Plot a one-dimensional CTI dataset (``Dataset1D``) and its fit (``FitDataset1D``).

.. currentmodule:: autocti.plot

**Dataset:**

.. autosummary::
   :toctree: _autosummary

   figure_dataset_1d_data
   subplot_dataset_1d
   subplot_dataset_1d_list

**Fit:**

.. autosummary::
   :toctree: _autosummary

   figure_fit_dataset_1d
   subplot_fit_dataset_1d
   subplot_fit_dataset_1d_list
   fits_fit_dataset_1d

Charge Injection Imaging [aplt]
-------------------------------

Plot charge injection imaging (``ImagingCI``) and its fit (``FitImagingCI``), either the whole frame or one
region of it (e.g. the parallel FPR or EPER).

**Dataset:**

.. autosummary::
   :toctree: _autosummary

   figure_imaging_ci_data_region
   figure_pre_cti_data_residual_map
   subplot_imaging_ci
   subplot_imaging_ci_region
   subplot_imaging_ci_data_binned
   subplot_imaging_ci_list
   subplot_imaging_ci_data_region_list

**Fit:**

.. autosummary::
   :toctree: _autosummary

   figure_fit_ci_region
   subplot_fit_ci
   subplot_fit_ci_region
   subplot_noise_scaling_map_dict
   subplot_fit_ci_list
   subplot_fit_ci_region_list
   fits_fit_ci

General Plot Functions [aplt]
-----------------------------

Lower-level functions the plots above are built from, for plotting any array or (y,x) line yourself.

.. autosummary::
   :toctree: _autosummary

   plot_array
   plot_yx
   plot_cti_1d
   subplot_save

Non-linear Search Plots [aplt]
------------------------------

Plots of a completed non-linear search, re-exported from **PyAutoFit**. Pass them the ``Samples`` of a fit.

.. autosummary::
   :toctree: _autosummary

   corner_cornerpy
   corner_anesthetic
   subplot_parameters
   log_likelihood_vs_iteration

Figure Output [aplt]
--------------------

The shared helper that shows a figure or writes it to ``path/filename.format``:

.. autosummary::
   :toctree: _autosummary

   output_figure

Visualization During a Fit [aplt]
---------------------------------

The classes a model-fit uses to write its on-the-fly visualization. You do not normally create these
yourself; the ``Analysis`` classes do.

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   :recursive:

   PlotterDataset1D
   PlotterImagingCI
