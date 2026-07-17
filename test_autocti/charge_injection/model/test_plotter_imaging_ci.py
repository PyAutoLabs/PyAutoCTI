import shutil
from pathlib import Path

import pytest

from autocti.charge_injection.model.plotter import PlotterImagingCI

directory = Path(__file__).resolve().parent


@pytest.fixture(name="plot_path")
def make_plot_path():
    return directory / "files"


def test__dataset(imaging_ci_7x7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterImagingCI(image_path=plot_path)

    plotter.dataset(dataset=imaging_ci_7x7)
    plotter.dataset_regions(
        dataset=imaging_ci_7x7, region_list=["parallel_fpr", "serial_eper"]
    )

    assert str(Path(plot_path) / "dataset" / "subplot_dataset.png") in plot_patch.paths
    assert (
        str(Path(plot_path) / "dataset" / "subplot_1d_ci_parallel_fpr.png")
        in plot_patch.paths
    )
    assert str(Path(plot_path) / "dataset" / "data_serial_eper.png") in plot_patch.paths


def test__dataset_combined(imaging_ci_7x7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterImagingCI(image_path=plot_path)

    plotter.dataset_combined(dataset_list=[imaging_ci_7x7, imaging_ci_7x7])
    plotter.dataset_regions_combined(
        dataset_list=[imaging_ci_7x7, imaging_ci_7x7], region_list=["parallel_fpr"]
    )

    assert (
        str(Path(plot_path) / "dataset_combined" / "subplot_dataset_list.png")
        in plot_patch.paths
    )
    assert (
        str(Path(plot_path) / "dataset_combined" / "subplot_data_list_parallel_fpr.png")
        in plot_patch.paths
    )


def test__fit(fit_ci_7x7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterImagingCI(image_path=plot_path)

    plotter.fit(fit=fit_ci_7x7, during_analysis=True)
    plotter.fit_1d_regions(
        fit=fit_ci_7x7, region_list=["parallel_fpr"], during_analysis=True
    )

    assert str(Path(plot_path) / "fit_dataset" / "subplot_fit.png") in plot_patch.paths
    assert (
        str(Path(plot_path) / "fit_dataset" / "subplot_1d_fit_ci_parallel_fpr.png")
        in plot_patch.paths
    )


def test__fit__not_during_analysis_outputs_fits(fit_ci_7x7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterImagingCI(image_path=plot_path)

    plotter.fit(fit=fit_ci_7x7, during_analysis=False)

    assert (Path(plot_path) / "fit_dataset" / "fit.fits").exists()


def test__fit_combined(fit_ci_7x7, plot_path, plot_patch):
    if Path(plot_path).exists():
        shutil.rmtree(plot_path)

    plotter = PlotterImagingCI(image_path=plot_path)

    plotter.fit_combined(fit_list=[fit_ci_7x7, fit_ci_7x7], during_analysis=True)
    plotter.fit_1d_regions_combined(
        fit_list=[fit_ci_7x7, fit_ci_7x7],
        region_list=["parallel_eper"],
        during_analysis=True,
    )

    assert (
        str(Path(plot_path) / "fit_dataset_combined" / "subplot_residual_map_list.png")
        in plot_patch.paths
    )
    assert (
        str(
            Path(plot_path)
            / "fit_dataset_combined"
            / "subplot_data_list_parallel_eper.png"
        )
        in plot_patch.paths
    )
