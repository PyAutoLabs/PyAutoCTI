from pathlib import Path

import pytest

import autocti.plot as aplt

directory = Path(__file__).resolve().parent


@pytest.fixture(name="plot_path")
def make_plot_path():
    return directory / "files" / "plots"


def test__figure_data_region(imaging_ci_7x7, plot_path, plot_patch):
    aplt.figure_imaging_ci_data_region(
        dataset=imaging_ci_7x7,
        region="parallel_fpr",
        output_path=plot_path,
        output_format="png",
    )
    aplt.figure_imaging_ci_data_region(
        dataset=imaging_ci_7x7,
        region="parallel_eper",
        logy=True,
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "data_parallel_fpr.png") in plot_patch.paths
    assert str(Path(plot_path) / "data_logy_parallel_eper.png") in plot_patch.paths


def test__subplot_dataset(imaging_ci_7x7, plot_path, plot_patch):
    aplt.subplot_imaging_ci(
        dataset=imaging_ci_7x7, output_path=plot_path, output_format="png"
    )

    assert str(Path(plot_path) / "subplot_dataset.png") in plot_patch.paths


def test__subplot_dataset_region(imaging_ci_7x7, plot_path, plot_patch):
    aplt.subplot_imaging_ci_region(
        dataset=imaging_ci_7x7,
        region="serial_eper",
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "subplot_1d_ci_serial_eper.png") in plot_patch.paths


def test__subplot_dataset_list(imaging_ci_7x7, plot_path, plot_patch):
    aplt.subplot_imaging_ci_list(
        dataset_list=[imaging_ci_7x7, imaging_ci_7x7],
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "subplot_dataset_list.png") in plot_patch.paths


def test__subplot_data_region_list(imaging_ci_7x7, plot_path, plot_patch):
    aplt.subplot_imaging_ci_data_region_list(
        dataset_list=[imaging_ci_7x7, imaging_ci_7x7],
        region="parallel_fpr",
        output_path=plot_path,
        output_format="png",
    )

    assert (
        str(Path(plot_path) / "subplot_data_list_parallel_fpr.png") in plot_patch.paths
    )
