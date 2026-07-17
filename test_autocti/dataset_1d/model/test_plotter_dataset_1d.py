import shutil
from pathlib import Path

import pytest

from autocti.dataset_1d.model.plotter import PlotterDataset1D

directory = Path(__file__).resolve().parent


@pytest.fixture(name="plot_path")
def make_plot_path():
    return directory / "files"


def test__dataset(dataset_1d_7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterDataset1D(image_path=plot_path)

    plotter.dataset(dataset=dataset_1d_7)
    plotter.dataset_regions(dataset=dataset_1d_7, region_list=["fpr", "eper"])

    assert str(Path(plot_path) / "dataset" / "subplot_dataset.png") in plot_patch.paths
    assert (
        str(Path(plot_path) / "dataset" / "subplot_dataset_fpr.png") in plot_patch.paths
    )
    assert str(Path(plot_path) / "dataset" / "data_eper.png") in plot_patch.paths


def test__dataset_combined(dataset_1d_7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterDataset1D(image_path=plot_path)

    plotter.dataset_combined(dataset_list=[dataset_1d_7, dataset_1d_7])
    plotter.dataset_regions_combined(
        dataset_list=[dataset_1d_7, dataset_1d_7], region_list=["fpr"]
    )

    assert (
        str(Path(plot_path) / "dataset" / "subplot_data_list.png") in plot_patch.paths
    )
    assert (
        str(Path(plot_path) / "dataset" / "subplot_data_list_fpr.png")
        in plot_patch.paths
    )


def test__fit(fit_1d_7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterDataset1D(image_path=plot_path)

    plotter.fit(fit=fit_1d_7, during_analysis=True)
    plotter.fit_regions(fit=fit_1d_7, region_list=["fpr", "eper"], during_analysis=True)

    assert str(Path(plot_path) / "fit_dataset" / "subplot_fit.png") in plot_patch.paths
    assert (
        str(Path(plot_path) / "fit_dataset" / "subplot_fit_eper.png")
        in plot_patch.paths
    )


def test__fit__not_during_analysis_outputs_fits(fit_1d_7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterDataset1D(image_path=plot_path)

    plotter.fit(fit=fit_1d_7, during_analysis=False)

    assert (Path(plot_path) / "fit_dataset" / "fit.fits").exists()


def test__fit_combined(fit_1d_7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterDataset1D(image_path=plot_path)

    plotter.fit_combined(fit_list=[fit_1d_7, fit_1d_7], during_analysis=True)
    plotter.fit_region_combined(
        fit_list=[fit_1d_7, fit_1d_7], region_list=["eper"], during_analysis=True
    )

    assert (
        str(Path(plot_path) / "fit_dataset_combined" / "subplot_data_list.png")
        in plot_patch.paths
    )
    assert (
        str(Path(plot_path) / "fit_dataset_combined" / "subplot_data_list_eper.png")
        in plot_patch.paths
    )
