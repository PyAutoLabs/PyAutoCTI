from pathlib import Path
from typing import List, Optional

import numpy as np

from autoconf.fitsable import hdu_list_for_output_from
from autoarray.plot.utils import (
    subplots,
    subplot_save,
    conf_subplot_figsize,
    tight_layout,
)

from autocti.dataset_1d.fit import FitDataset1D
from autocti.util import plot_utils

# The 1D fit quantities plottable via figure_fit: name -> (title, has data errorbars, model overlay)
_QUANTITY_TITLES = {
    "data": "Data",
    "noise_map": "Noise Map",
    "signal_to_noise_map": "Signal To Noise Map",
    "pre_cti_data": "Pre CTI Data",
    "post_cti_data": "Post CTI Data",
    "residual_map": "Residual Map",
    "normalized_residual_map": "Normalized Residual Map",
    "chi_squared_map": "Chi-Squared Map",
}


def _extract(fit: FitDataset1D, array, region: Optional[str]):
    return fit.dataset.layout.extract_region_from(array=array, region=region)


def figure_fit(
    fit: FitDataset1D,
    quantity: str,
    region: Optional[str] = None,
    logy: bool = False,
    ax=None,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Plot a 1D quantity of a ``FitDataset1D`` (optionally extracted and binned over a region, e.g. the FPR
    or EPER).

    The ``data`` quantity is drawn as an errorbar figure with the model data overlaid in red; all other
    quantities are plain line figures.

    Parameters
    ----------
    fit
        The 1D fit whose quantity is plotted.
    quantity
        One of {"data", "noise_map", "signal_to_noise_map", "pre_cti_data", "post_cti_data",
        "residual_map", "normalized_residual_map", "chi_squared_map"}.
    region
        The region extracted and binned {"fpr", "eper"}; ``None`` plots the full fit.
    logy
        Whether the y-axis is log10 scaled.
    """
    suffix = f"_{region}" if region is not None else ""
    title_str = plot_utils.title_str_from(dataset=fit.dataset, region=region)
    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    is_data = quantity == "data"

    plot_utils.plot_cti_1d(
        y=_extract(fit, getattr(fit, quantity), region),
        y_errors=_extract(fit, fit.noise_map, region) if is_data else None,
        y_extra=_extract(fit, fit.model_data, region) if is_data else None,
        errorbar=is_data,
        logy=logy,
        should_plot_zero=plot_utils.should_plot_zero_from(region=region),
        text_manual_dict=(
            plot_utils.text_manual_dict_from(dataset=fit.dataset, region=region)
            if is_data
            else None
        ),
        text_manual_dict_y=plot_utils.text_manual_dict_y_from(region=region),
        title=_pf(
            f"{_QUANTITY_TITLES[quantity]} {title_str}" + (" [log10]" if logy else "")
        ),
        ylabel="e-" if quantity != "signal_to_noise_map" else "",
        ax=ax,
        output_path=output_path,
        output_filename=f"{quantity}_logy{suffix}" if logy else f"{quantity}{suffix}",
        output_format=output_format,
    )


def subplot_fit(
    fit: FitDataset1D,
    region: Optional[str] = None,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Eight-panel subplot of a ``FitDataset1D``: the data (with model overlay), noise map, signal-to-noise
    map, pre-CTI data, post-CTI data, residual map, normalized residual map and chi-squared map, each
    optionally extracted and binned over a region (e.g. the FPR or EPER).

    Parameters
    ----------
    fit
        The 1D fit to visualize.
    region
        The region extracted and binned {"fpr", "eper"}; ``None`` plots the full fit.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    suffix = f"_{region}" if region is not None else ""

    quantities = list(_QUANTITY_TITLES)

    fig, axes = subplots(2, 4, figsize=conf_subplot_figsize(2, 4))
    axes = axes.flatten()

    for i, quantity in enumerate(quantities):
        figure_fit(
            fit=fit,
            quantity=quantity,
            region=region,
            ax=axes[i],
            title_prefix=title_prefix,
        )

    tight_layout()
    subplot_save(fig, output_path, f"subplot_fit{suffix}", output_format)


def subplot_fit_list(
    fit_list: List[FitDataset1D],
    quantity: str = "data",
    region: Optional[str] = None,
    logy: bool = False,
    output_path=None,
    output_filename: str = None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Combined subplot of one quantity of a list of ``FitDataset1D`` objects (e.g. from a combined
    analysis), one panel per fit.

    Parameters
    ----------
    fit_list
        The list of 1D fits to visualize.
    quantity
        The fit quantity plotted in every panel (see ``figure_fit``).
    region
        The region extracted and binned {"fpr", "eper"}; ``None`` plots the full fits.
    logy
        Whether the y-axes are log10 scaled.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    suffix = f"_{region}" if region is not None else ""

    n = len(fit_list)
    if n == 0:
        raise ValueError("An empty list was passed to a *_list plot function.")

    cols = min(n, 3)
    rows = (n + cols - 1) // cols

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, fit in enumerate(fit_list):
        figure_fit(
            fit=fit,
            quantity=quantity,
            region=region,
            logy=logy,
            ax=axes[i],
            title_prefix=title_prefix,
        )

    for ax in axes[n:]:
        ax.axis("off")

    tight_layout()

    if output_filename is None:
        output_filename = f"subplot_{quantity}{'_logy' if logy else ''}_list{suffix}"

    subplot_save(fig, output_path, output_filename, output_format)


def fits_fit(fit: FitDataset1D, output_path):
    """
    Output the quantities of a ``FitDataset1D`` to a single ``fit.fits`` file with one extension per
    quantity (model data, residual map, normalized residual map and chi-squared map).
    """
    hdu_list = hdu_list_for_output_from(
        values_list=[
            np.asarray(fit.model_data.native),
            np.asarray(fit.residual_map.native),
            np.asarray(fit.normalized_residual_map.native),
            np.asarray(fit.chi_squared_map.native),
        ],
        ext_name_list=[
            "model_data",
            "residual_map",
            "normalized_residual_map",
            "chi_squared_map",
        ],
        header_dict=fit.dataset.mask.header_dict,
    )
    hdu_list.writeto(Path(output_path) / "fit.fits", overwrite=True)
