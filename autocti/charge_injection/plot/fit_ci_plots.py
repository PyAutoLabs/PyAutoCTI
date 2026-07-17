from pathlib import Path
from typing import List, Optional

import numpy as np

from autoconf.fitsable import hdu_list_for_output_from
from autoarray.plot.array import plot_array
from autoarray.plot.utils import (
    subplots,
    subplot_save,
    conf_subplot_figsize,
    tight_layout,
)

from autocti.charge_injection.fit import FitImagingCI
from autocti.util import plot_utils

# The fit quantities plottable in 2D and (binned over a region) in 1D.
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


def _extract(fit: FitImagingCI, array, region: str):
    return fit.dataset.layout.extract_region_from(array=array, region=region)


def figure_fit_region(
    fit: FitImagingCI,
    quantity: str,
    region: str,
    logy: bool = False,
    ax=None,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Plot a quantity of a ``FitImagingCI`` extracted and binned over a region (e.g. the parallel FPR) as a
    1D figure.

    The ``data`` quantity is drawn as an errorbar figure with the binned model data overlaid in red; all
    other quantities are plain line figures.

    Parameters
    ----------
    fit
        The charge injection fit whose quantity is plotted.
    quantity
        One of {"data", "noise_map", "signal_to_noise_map", "pre_cti_data", "post_cti_data",
        "residual_map", "normalized_residual_map", "chi_squared_map"}.
    region
        The region extracted and binned {"parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper"}.
    logy
        Whether the y-axis is log10 scaled.
    """
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
            f"{_QUANTITY_TITLES[quantity]} {title_str}" + (" [log10 y]" if logy else "")
        ),
        ylabel="e-" if quantity != "signal_to_noise_map" else "",
        ax=ax,
        output_path=output_path,
        output_filename=f"{quantity}_logy_{region}" if logy else f"{quantity}_{region}",
        output_format=output_format,
    )


def subplot_fit(
    fit: FitImagingCI,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Eight-panel 2D subplot of a ``FitImagingCI``: the data, noise map, signal-to-noise map, pre-CTI data,
    post-CTI data, residual map, normalized residual map and chi-squared map.

    Parameters
    ----------
    fit
        The charge injection fit to visualize.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    title_str = plot_utils.title_str_2d_from(dataset=fit.dataset)
    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    fig, axes = subplots(2, 4, figsize=conf_subplot_figsize(2, 4))
    axes = axes.flatten()

    for i, (quantity, title) in enumerate(_QUANTITY_TITLES.items()):
        plot_array(
            getattr(fit, quantity),
            ax=axes[i],
            title=_pf(title if title_str is None else f"{title_str} {title}"),
        )

    tight_layout()
    subplot_save(fig, output_path, "subplot_fit", output_format)


def subplot_fit_region(
    fit: FitImagingCI,
    region: str,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Four-panel 1D subplot of a ``FitImagingCI`` extracted and binned over a region (e.g. the parallel
    FPR): the data (with model overlay), residual map, normalized residual map and chi-squared map.

    Parameters
    ----------
    fit
        The charge injection fit to visualize.
    region
        The region extracted and binned {"parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper"}.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    fig, axes = subplots(2, 2, figsize=conf_subplot_figsize(2, 2))
    axes = axes.flatten()

    for i, quantity in enumerate(
        ["data", "residual_map", "normalized_residual_map", "chi_squared_map"]
    ):
        figure_fit_region(
            fit=fit,
            quantity=quantity,
            region=region,
            ax=axes[i],
            title_prefix=title_prefix,
        )

    tight_layout()
    subplot_save(fig, output_path, f"subplot_1d_fit_ci_{region}", output_format)


def subplot_noise_scaling_map_dict(
    fit: FitImagingCI,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Subplot of every noise scaling map of a ``FitImagingCI``, which are used by hyper-functionality to
    scale the noise map between fits.

    Parameters
    ----------
    fit
        The charge injection fit whose noise scaling maps are visualized.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    n = len(fit.noise_scaling_map_dict)
    cols = min(n, 2)
    rows = (n + cols - 1) // cols

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, (key, noise_scaling_map) in enumerate(fit.noise_scaling_map_dict.items()):
        plot_array(noise_scaling_map, ax=axes[i], title=_pf(f"Noise Scaling Map {key}"))

    for ax in axes[n:]:
        ax.axis("off")

    tight_layout()
    subplot_save(fig, output_path, "subplot_noise_scaling_map_dict", output_format)


def subplot_fit_list(
    fit_list: List[FitImagingCI],
    quantity: str = "residual_map",
    output_path=None,
    output_filename: str = None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Combined 2D subplot of one quantity of a list of ``FitImagingCI`` objects (e.g. from a combined
    analysis), one panel per fit.

    Parameters
    ----------
    fit_list
        The list of charge injection fits to visualize.
    quantity
        The fit quantity plotted in every panel (see ``figure_fit_region``).
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    n = len(fit_list)
    cols = min(n, 3)
    rows = (n + cols - 1) // cols

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, fit in enumerate(fit_list):
        plot_array(
            getattr(fit, quantity),
            ax=axes[i],
            title=_pf(f"{_QUANTITY_TITLES[quantity]} {i}"),
        )

    for ax in axes[n:]:
        ax.axis("off")

    tight_layout()

    if output_filename is None:
        output_filename = f"subplot_{quantity}_list"

    subplot_save(fig, output_path, output_filename, output_format)


def subplot_fit_region_list(
    fit_list: List[FitImagingCI],
    region: str,
    quantity: str = "data",
    logy: bool = False,
    output_path=None,
    output_filename: str = None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Combined 1D subplot of one binned quantity of a list of ``FitImagingCI`` objects over a region (e.g.
    the parallel EPER), one panel per fit.

    Parameters
    ----------
    fit_list
        The list of charge injection fits to visualize.
    region
        The region extracted and binned {"parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper"}.
    quantity
        The fit quantity plotted in every panel (see ``figure_fit_region``).
    logy
        Whether the y-axes are log10 scaled.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    n = len(fit_list)
    cols = min(n, 3)
    rows = (n + cols - 1) // cols

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, fit in enumerate(fit_list):
        figure_fit_region(
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
        output_filename = f"subplot_{quantity}{'_logy' if logy else ''}_list_{region}"

    subplot_save(fig, output_path, output_filename, output_format)


def fits_fit(fit: FitImagingCI, output_path):
    """
    Output the quantities of a ``FitImagingCI`` to a single ``fit.fits`` file with one extension per
    quantity (post-CTI data, residual map, normalized residual map and chi-squared map).
    """
    hdu_list = hdu_list_for_output_from(
        values_list=[
            np.asarray(fit.post_cti_data.native),
            np.asarray(fit.residual_map.native),
            np.asarray(fit.normalized_residual_map.native),
            np.asarray(fit.chi_squared_map.native),
        ],
        ext_name_list=[
            "post_cti_data",
            "residual_map",
            "normalized_residual_map",
            "chi_squared_map",
        ],
        header_dict=fit.dataset.mask.header_dict,
    )
    hdu_list.writeto(Path(output_path) / "fit.fits", overwrite=True)
