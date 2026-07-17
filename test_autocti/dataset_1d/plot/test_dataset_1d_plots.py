from pathlib import Path

import pytest

import autocti.plot as aplt

directory = Path(__file__).resolve().parent


@pytest.fixture(name="plot_path")
def make_plot_path():
    return directory / "files" / "plots"


def test__figure_data(dataset_1d_7, plot_path, plot_patch):
    aplt.figure_dataset_1d_data(
        dataset=dataset_1d_7, output_path=plot_path, output_format="png"
    )

    assert str(Path(plot_path) / "data.png") in plot_patch.paths


def test__figure_data__region_and_logy(dataset_1d_7, plot_path, plot_patch):
    aplt.figure_dataset_1d_data(
        dataset=dataset_1d_7,
        region="fpr",
        output_path=plot_path,
        output_format="png",
    )
    aplt.figure_dataset_1d_data(
        dataset=dataset_1d_7,
        region="eper",
        logy=True,
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "data_fpr.png") in plot_patch.paths
    assert str(Path(plot_path) / "data_logy_eper.png") in plot_patch.paths


def test__subplot_dataset(dataset_1d_7, plot_path, plot_patch):
    aplt.subplot_dataset_1d(
        dataset=dataset_1d_7, output_path=plot_path, output_format="png"
    )
    aplt.subplot_dataset_1d(
        dataset=dataset_1d_7, region="fpr", output_path=plot_path, output_format="png"
    )

    assert str(Path(plot_path) / "subplot_dataset.png") in plot_patch.paths
    assert str(Path(plot_path) / "subplot_dataset_fpr.png") in plot_patch.paths


def test__subplot_dataset_list(dataset_1d_7, plot_path, plot_patch):
    aplt.subplot_dataset_1d_list(
        dataset_list=[dataset_1d_7, dataset_1d_7],
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "subplot_data_list.png") in plot_patch.paths
