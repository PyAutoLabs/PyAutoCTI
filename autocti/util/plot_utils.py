import logging
from typing import Dict, Optional

import numpy as np

from autoarray.plot.utils import subplot_save

from autocti.extract.settings import SettingsExtract
from autocti.mask.mask_2d import Mask2D

from autocti import exc

logger = logging.getLogger(__name__)


def title_str_from(dataset, region: Optional[str]) -> str:
    """
    The title of a 1D CTI figure, which describes the region of the dataset that is extracted and binned
    (e.g. the FPR or EPER) and, when available, the CCD identifier from the dataset's settings dictionary.

    Parameters
    ----------
    dataset
        The dataset (e.g. `Dataset1D`, `ImagingCI`) whose `settings_dict` may contain a CCD identifier.
    region
        The region string {"fpr", "eper", "parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper"} or None.
    """
    if dataset.settings_dict is not None:
        ccd_str = dataset.settings_dict.get("CCD")
    else:
        ccd_str = None

    title_str = {
        None: "",
        "fpr": "FPR",
        "eper": "EPER",
        "parallel_fpr": "Parallel FPR",
        "parallel_eper": "Parallel EPER",
        "serial_fpr": "Serial FPR",
        "serial_eper": "Serial EPER",
        "fpr_non_uniformity": "FPR Non Uniformity",
    }.get(region, region or "")

    if ccd_str is None:
        return title_str
    return f"{ccd_str} {title_str}"


def title_str_2d_from(dataset) -> Optional[str]:
    """
    The title of a 2D CTI figure, built from the charge injection electronics settings in the dataset's
    settings dictionary (CCD id, injection gate voltages, id delay) when available.
    """
    if dataset.settings_dict is not None:
        ccd_str = dataset.settings_dict.get("CCD")
        ig1_str = dataset.settings_dict.get("CI_IG1")
        ig2_str = dataset.settings_dict.get("CI_IG2")
        id_delay_str = dataset.settings_dict.get("CI_IDDLY")

        return f"{ccd_str} IG1={ig1_str} IG2={ig2_str} IDD={id_delay_str}"


def text_manual_dict_from(dataset, region: Optional[str] = None) -> Dict:
    """
    A dictionary of text annotations added to 1D CTI figures — the dataset's FPR value (on EPER figures,
    where the trailed charge is interpreted relative to the injection level) and its settings dictionary.
    """
    try:
        fpr_value = dataset.fpr_value
    except AttributeError:
        fpr_value = None

    text_manual_dict = {}

    if region is not None:
        if fpr_value is not None and "eper" in region:
            text_manual_dict = {**text_manual_dict, "FPR (e-)": dataset.fpr_value}

    if dataset.settings_dict is not None:
        text_manual_dict = {**text_manual_dict, **dataset.settings_dict}

    return text_manual_dict


def text_manual_dict_y_from(region: Optional[str] = None) -> float:
    """
    The figure-fraction y coordinate where the text annotations of a 1D CTI figure begin.
    """
    if region is None or "eper" in region:
        return 0.94
    return 0.34


def should_plot_zero_from(region: Optional[str]) -> bool:
    """
    Whether a 1D CTI figure includes a horizontal line at y=0 — EPER trails decay towards zero, so the
    zero line aids interpretation.
    """
    if region is None:
        return False

    return "eper" in region


def fpr_mask_from(dataset) -> Mask2D:
    """
    Returns a mask of a charge injection dataset's FPRs, where the serial prescan and overscan regions are
    also masked.

    This is used for plotting images binned across rows and columns (e.g. the parallel and serial directions)
    with the FPR excluded.
    """
    fpr_size = dataset.layout.parallel_rows_within_regions[0]

    if any(
        [
            fpr_size != fpr_size_of_row
            for fpr_size_of_row in dataset.layout.parallel_rows_within_regions
        ]
    ):
        raise exc.PlottingException(
            "The FPR in this dataset have a variable number of rows. This means that masking the FPR in "
            "data-binned figures is not supported."
        )

    fpr_mask = dataset.layout.extract.parallel_fpr.mask_from(
        settings=SettingsExtract(pixels=(0, fpr_size)),
        pixel_scales=dataset.pixel_scales,
    )

    # A layout may legitimately lack prescan / overscan regions (e.g. after the
    # dataset is trimmed via `apply_settings`), in which case there is nothing
    # to mask for that region.
    serial_prescan = dataset.layout.extract.serial_prescan.serial_prescan

    if serial_prescan is not None:
        fpr_mask[
            serial_prescan.y0 : serial_prescan.y1, serial_prescan.x0 : serial_prescan.x1
        ] = True

    serial_overscan = dataset.layout.extract.serial_overscan.serial_overscan

    if serial_overscan is not None:
        fpr_mask[
            serial_overscan.y0 : serial_overscan.y1,
            serial_overscan.x0 : serial_overscan.x1,
        ] = True

    return fpr_mask


def plot_cti_1d(
    y,
    y_errors=None,
    y_extra=None,
    y_extra_color: str = "r",
    logy: bool = False,
    errorbar: bool = False,
    ls_errorbar: str = "",
    title: str = "",
    ylabel: str = "e-",
    xlabel: str = "Pixel No.",
    text_manual_dict: Optional[Dict] = None,
    text_manual_dict_y: float = 0.94,
    should_plot_zero: bool = False,
    ax=None,
    output_path=None,
    output_filename: str = "cti_1d",
    output_format=None,
):
    """
    Plot a 1D quantity of a CTI dataset or fit (e.g. the data binned over an FPR or EPER region) using
    direct matplotlib calls.

    This is the 1D plotting primitive of PyAutoCTI, which every ``*_plots.py`` figure and subplot panel
    goes through. When ``ax`` is input the line is drawn on the existing axes (subplot panel); otherwise a
    new figure is created and output via ``autoarray.plot.utils.subplot_save``.

    Parameters
    ----------
    y
        The 1D array of values plotted on the y-axis.
    y_errors
        The noise values of every y value, plotted via ``errorbar`` when ``errorbar=True``.
    y_extra
        An optional second y series overlaid as a line (e.g. the model data of a fit).
    logy
        Whether the y-axis is log10 scaled (used for EPER trails which span decades).
    errorbar
        Whether the primary series is drawn via ``plt.errorbar`` with ``y_errors``.
    ls_errorbar
        The linestyle of the errorbar plot (e.g. "-" to connect points, "" for markers only).
    text_manual_dict
        A dict of ``label: value`` annotations written down the side of the figure (e.g. electronics
        settings, the FPR value on EPER figures).
    text_manual_dict_y
        The axes-fraction y coordinate where annotations start.
    should_plot_zero
        Whether a horizontal line at y=0 is drawn (EPER figures).
    ax
        Existing matplotlib axes to draw onto; ``None`` creates and saves/shows a new figure.
    """
    import matplotlib.pyplot as plt

    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    standalone = ax is None

    if standalone:
        from autoarray.plot.utils import conf_figsize

        fig, ax = plt.subplots(figsize=conf_figsize())
    else:
        fig = ax.figure

    y = np.asarray(y)
    x = np.arange(len(y))

    if errorbar:
        ax.errorbar(
            x,
            y,
            yerr=np.asarray(y_errors) if y_errors is not None else None,
            color="k",
            ecolor="k",
            elinewidth=1,
            capsize=2,
            linestyle=ls_errorbar,
            marker=".",
        )
    else:
        ax.plot(x, y, color="k")

    if y_extra is not None:
        ax.plot(x, np.asarray(y_extra), color=y_extra_color)

    if logy:
        ax.set_yscale("log")

    if should_plot_zero and not logy:
        ax.axhline(y=0.0, color="b", linestyle="--", linewidth=1)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if text_manual_dict:
        text_y = text_manual_dict_y
        for key, value in text_manual_dict.items():
            ax.text(
                0.7,
                text_y,
                f"{key} = {value}",
                transform=ax.transAxes,
                fontsize=8,
            )
            text_y -= 0.05

    if standalone:
        subplot_save(fig, output_path, output_filename, output_format)
