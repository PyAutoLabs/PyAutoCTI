import copy
from typing import List, Optional

from autoconf import conf

from autoarray.plot.array import plot_array
from autoarray.plot.utils import (
    subplots,
    subplot_save,
    conf_subplot_figsize,
    tight_layout,
)

from autocti.charge_injection.imaging.imaging import ImagingCI
from autocti.util import plot_utils


def _extract(dataset: ImagingCI, array, region: str):
    """Extract and bin a 1D quantity of the charge injection dataset via its layout."""
    return dataset.layout.extract_region_from(array=array, region=region)


def _extract_noise(dataset: ImagingCI, array, region: str):
    return dataset.layout.extract_region_noise_map_from(array=array, region=region)


def figure_data_region(
    dataset: ImagingCI,
    region: str,
    logy: bool = False,
    ax=None,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Plot the data of an ``ImagingCI`` dataset extracted and binned over a region (e.g. the parallel FPR)
    as a 1D errorbar figure, with the binned noise map as error bars.

    Parameters
    ----------
    dataset
        The charge injection dataset whose data is plotted.
    region
        The region extracted and binned {"parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper",
        "fpr_non_uniformity"}.
    logy
        Whether the y-axis is log10 scaled.
    ax
        Existing matplotlib axes to draw onto (subplot panel); ``None`` creates a standalone figure.
    """
    title_str = plot_utils.title_str_from(dataset=dataset, region=region)
    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.data, region),
        y_errors=_extract_noise(dataset, dataset.noise_map, region),
        errorbar=True,
        ls_errorbar="-" if region == "fpr_non_uniformity" else "",
        logy=logy,
        should_plot_zero=plot_utils.should_plot_zero_from(region=region),
        text_manual_dict=plot_utils.text_manual_dict_from(
            dataset=dataset, region=region
        ),
        text_manual_dict_y=plot_utils.text_manual_dict_y_from(region=region),
        title=_pf(f"Data {title_str}" + (" [log10 y]" if logy else "")),
        ax=ax,
        output_path=output_path,
        output_filename=f"data_logy_{region}" if logy else f"data_{region}",
        output_format=output_format,
    )


def subplot_dataset(
    dataset: ImagingCI,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Subplot of the 2D attributes of an ``ImagingCI`` dataset: the data, noise map, signal-to-noise map,
    pre-CTI data and (when present) the cosmic ray map.

    Parameters
    ----------
    dataset
        The charge injection dataset to visualize.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    title_str = plot_utils.title_str_2d_from(dataset=dataset)
    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    panels = [
        (dataset.data, "Data"),
        (dataset.noise_map, "Noise Map"),
        (dataset.signal_to_noise_map, "Signal To Noise Map"),
        (dataset.pre_cti_data, "Pre CTI Data"),
    ]

    if dataset.cosmic_ray_map is not None:
        panels.append((dataset.cosmic_ray_map, "Cosmic Ray Map"))

    n = len(panels)
    cols = 3
    rows = (n + cols - 1) // cols

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.flatten()

    for i, (array, title) in enumerate(panels):
        plot_array(array, ax=axes[i], title=_pf(title_str or title))

    for ax in axes[n:]:
        ax.axis("off")

    tight_layout()
    subplot_save(fig, output_path, "subplot_dataset", output_format)


def subplot_dataset_region(
    dataset: ImagingCI,
    region: str,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Four-panel 1D subplot of an ``ImagingCI`` dataset extracted and binned over a region (e.g. the
    parallel FPR): the data (with noise error bars), noise map, pre-CTI data and signal-to-noise map.

    Parameters
    ----------
    dataset
        The charge injection dataset to visualize.
    region
        The region extracted and binned {"parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper"}.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    title_str = plot_utils.title_str_from(dataset=dataset, region=region)
    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    fig, axes = subplots(2, 2, figsize=conf_subplot_figsize(2, 2))
    axes = axes.flatten()

    figure_data_region(
        dataset=dataset, region=region, ax=axes[0], title_prefix=title_prefix
    )

    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.noise_map, region),
        title=_pf(f"Noise Map {title_str}"),
        ylabel="Noise (e-)",
        ax=axes[1],
    )
    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.pre_cti_data, region),
        title=_pf(f"Pre CTI Data {title_str}"),
        ax=axes[2],
    )
    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.signal_to_noise_map, region),
        title=_pf(f"Signal To Noise Map {title_str}"),
        ylabel="Signal To Noise",
        ax=axes[3],
    )

    tight_layout()
    subplot_save(fig, output_path, f"subplot_1d_ci_{region}", output_format)


def subplot_data_binned(
    dataset: ImagingCI,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Four-panel subplot of the charge injection data binned over the parallel and serial directions, with
    and without the FPR regions included.

    Panels binned over rows show the FPR of each injection; with the FPR masked they show the parallel
    EPER of each injection. Panels binned over columns show the charge injection non-uniformity, where
    inaccurate bias / stray-light subtraction produces visible gradients.

    Parameters
    ----------
    dataset
        The charge injection dataset to visualize.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    fpr_mask = plot_utils.fpr_mask_from(dataset=dataset)

    panels = [
        (fpr_mask.invert(), "binned_across_rows", "Data With FPR Binned Over Rows"),
        (fpr_mask, "binned_across_rows", "Data No FPR Binned Over Rows"),
        (
            fpr_mask.invert(),
            "binned_across_columns",
            "Data With FPR Binned Over Columns",
        ),
        (fpr_mask, "binned_across_columns", "Data No FPR Binned Over Columns"),
    ]

    fig, axes = subplots(2, 2, figsize=conf_subplot_figsize(2, 2))
    axes = axes.flatten()

    text_manual_dict = plot_utils.text_manual_dict_from(dataset=dataset)
    text_manual_dict_y = plot_utils.text_manual_dict_y_from()

    for i, (mask, binned_attr, title) in enumerate(panels):
        data = copy.copy(dataset.data)
        y = getattr(data.apply_mask(mask=mask), binned_attr)

        plot_utils.plot_cti_1d(
            y=y,
            title=_pf(title),
            text_manual_dict=text_manual_dict,
            text_manual_dict_y=text_manual_dict_y,
            ax=axes[i],
        )

    tight_layout()
    subplot_save(fig, output_path, "subplot_data_binned", output_format)


def figure_pre_cti_data_residual_map(
    dataset: ImagingCI,
    ax=None,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Plot the 2D pre-CTI data residual map of an ``ImagingCI`` dataset with a symmetric color map, whose
    limits are set via the ``symmetric_cmap_value`` visualize config entry.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    symmetric_value = conf.instance["visualize"]["general"]["general"][
        "symmetric_cmap_value"
    ]

    plot_array(
        dataset.pre_cti_data_residual_map,
        ax=ax,
        title=_pf(
            plot_utils.title_str_2d_from(dataset=dataset) or "Pre CTI Data Residual Map"
        ),
        vmin=-symmetric_value,
        vmax=symmetric_value,
        output_path=output_path,
        output_filename="pre_cti_data_residual_map",
        output_format=output_format,
    )


def subplot_dataset_list(
    dataset_list: List[ImagingCI],
    output_path=None,
    output_filename: str = "subplot_dataset_list",
    output_format=None,
    title_prefix: str = None,
):
    """
    Combined subplot of a list of ``ImagingCI`` datasets (e.g. from a combined analysis), one row per
    dataset showing its data, noise map and pre-CTI data.

    Parameters
    ----------
    dataset_list
        The list of charge injection datasets to visualize.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    rows = len(dataset_list)
    cols = 3

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.reshape(rows, cols) if hasattr(axes, "reshape") else [[axes]]

    for i, dataset in enumerate(dataset_list):
        title_str = plot_utils.title_str_2d_from(dataset=dataset)
        plot_array(dataset.data, ax=axes[i][0], title=_pf(title_str or f"Data {i}"))
        plot_array(dataset.noise_map, ax=axes[i][1], title=_pf(f"Noise Map {i}"))
        plot_array(dataset.pre_cti_data, ax=axes[i][2], title=_pf(f"Pre CTI Data {i}"))

    tight_layout()
    subplot_save(fig, output_path, output_filename, output_format)


def subplot_data_region_list(
    dataset_list: List[ImagingCI],
    region: str,
    logy: bool = False,
    output_path=None,
    output_filename: str = None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Combined subplot of the binned 1D data of a list of ``ImagingCI`` datasets over a region (e.g. the
    parallel FPR), one panel per dataset.

    Parameters
    ----------
    dataset_list
        The list of charge injection datasets to visualize.
    region
        The region extracted and binned {"parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper"}.
    logy
        Whether the y-axes are log10 scaled.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    n = len(dataset_list)
    cols = min(n, 3)
    rows = (n + cols - 1) // cols

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, dataset in enumerate(dataset_list):
        figure_data_region(
            dataset=dataset,
            region=region,
            logy=logy,
            ax=axes[i],
            title_prefix=title_prefix,
        )

    for ax in axes[n:]:
        ax.axis("off")

    tight_layout()

    if output_filename is None:
        output_filename = f"subplot_data{'_logy' if logy else ''}_list_{region}"

    subplot_save(fig, output_path, output_filename, output_format)
