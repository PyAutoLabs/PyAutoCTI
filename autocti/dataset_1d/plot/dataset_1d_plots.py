from typing import List, Optional

from autoarray.plot.utils import (
    subplots,
    subplot_save,
    conf_subplot_figsize,
    tight_layout,
)

from autocti.dataset_1d.dataset_1d.dataset_1d import Dataset1D
from autocti.util import plot_utils


def _extract(dataset: Dataset1D, array, region: Optional[str]):
    """Extract (and for a region, bin) a 1D quantity of the dataset via its layout."""
    return dataset.layout.extract_region_from(array=array, region=region)


def figure_data(
    dataset: Dataset1D,
    region: Optional[str] = None,
    logy: bool = False,
    ax=None,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Plot the data of a ``Dataset1D`` (optionally extracted and binned over a region, e.g. the FPR or EPER)
    as a 1D errorbar figure, with the noise map as error bars.

    Parameters
    ----------
    dataset
        The 1D dataset whose data is plotted.
    region
        The region extracted and binned {"fpr", "eper"}; ``None`` plots the full dataset.
    logy
        Whether the y-axis is log10 scaled.
    ax
        Existing matplotlib axes to draw onto (subplot panel); ``None`` creates a standalone figure.
    """
    suffix = f"_{region}" if region is not None else ""
    title_str = plot_utils.title_str_from(dataset=dataset, region=region)
    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.data, region),
        y_errors=_extract(dataset, dataset.noise_map, region),
        errorbar=True,
        logy=logy,
        should_plot_zero=plot_utils.should_plot_zero_from(region=region),
        text_manual_dict=plot_utils.text_manual_dict_from(
            dataset=dataset, region=region
        ),
        text_manual_dict_y=plot_utils.text_manual_dict_y_from(region=region),
        title=_pf(f"Data 1D {title_str}" + (" [log10]" if logy else "")),
        ax=ax,
        output_path=output_path,
        output_filename=f"data_logy{suffix}" if logy else f"data{suffix}",
        output_format=output_format,
    )


def subplot_dataset(
    dataset: Dataset1D,
    region: Optional[str] = None,
    output_path=None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Four-panel subplot of a ``Dataset1D``: the data (with noise error bars), noise map, signal-to-noise
    map and pre-CTI data, each optionally extracted and binned over a region (e.g. the FPR or EPER).

    Parameters
    ----------
    dataset
        The 1D dataset to visualize.
    region
        The region extracted and binned {"fpr", "eper"}; ``None`` plots the full dataset.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    suffix = f"_{region}" if region is not None else ""
    title_str = plot_utils.title_str_from(dataset=dataset, region=region)
    _pf = (lambda t: f"{title_prefix.rstrip()} {t}") if title_prefix else (lambda t: t)

    fig, axes = subplots(2, 2, figsize=conf_subplot_figsize(2, 2))
    axes = axes.flatten()

    figure_data(dataset=dataset, region=region, ax=axes[0], title_prefix=title_prefix)

    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.noise_map, region),
        title=_pf(f"Noise Map {title_str}"),
        ax=axes[1],
    )
    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.signal_to_noise_map, region),
        title=_pf(f"Signal To Noise Map {title_str}"),
        ylabel="",
        ax=axes[2],
    )
    plot_utils.plot_cti_1d(
        y=_extract(dataset, dataset.pre_cti_data, region),
        title=_pf(f"Pre CTI Data {title_str}"),
        ax=axes[3],
    )

    tight_layout()
    subplot_save(fig, output_path, f"subplot_dataset{suffix}", output_format)


def subplot_dataset_list(
    dataset_list: List[Dataset1D],
    region: Optional[str] = None,
    logy: bool = False,
    output_path=None,
    output_filename: str = None,
    output_format=None,
    title_prefix: str = None,
):
    """
    Combined subplot of the data of a list of ``Dataset1D`` objects (e.g. from a combined analysis of
    multiple datasets), one panel per dataset.

    Parameters
    ----------
    dataset_list
        The list of 1D datasets to visualize.
    region
        The region extracted and binned {"fpr", "eper"}; ``None`` plots the full datasets.
    logy
        Whether the y-axes are log10 scaled.
    """
    if isinstance(output_format, (list, tuple)):
        output_format = output_format[0]

    suffix = f"_{region}" if region is not None else ""

    n = len(dataset_list)
    cols = min(n, 3)
    rows = (n + cols - 1) // cols

    fig, axes = subplots(rows, cols, figsize=conf_subplot_figsize(rows, cols))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, dataset in enumerate(dataset_list):
        figure_data(
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
        output_filename = (
            f"subplot_data_logy_list{suffix}" if logy else f"subplot_data_list{suffix}"
        )

    subplot_save(fig, output_path, output_filename, output_format)
