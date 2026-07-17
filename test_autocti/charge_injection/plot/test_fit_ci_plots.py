from pathlib import Path

import pytest

import autocti.plot as aplt

directory = Path(__file__).resolve().parent


@pytest.fixture(name="plot_path")
def make_plot_path():
    return directory / "files" / "plots"


def test__figure_fit_region(fit_ci_7x7, plot_path, plot_patch):
    aplt.figure_fit_ci_region(
        fit=fit_ci_7x7,
        quantity="data",
        region="parallel_fpr",
        output_path=plot_path,
        output_format="png",
    )
    aplt.figure_fit_ci_region(
        fit=fit_ci_7x7,
        quantity="residual_map",
        region="parallel_eper",
        logy=True,
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "data_parallel_fpr.png") in plot_patch.paths
    assert (
        str(Path(plot_path) / "residual_map_logy_parallel_eper.png") in plot_patch.paths
    )


def test__subplot_fit(fit_ci_7x7, plot_path, plot_patch):
    aplt.subplot_fit_ci(fit=fit_ci_7x7, output_path=plot_path, output_format="png")

    assert str(Path(plot_path) / "subplot_fit.png") in plot_patch.paths


def test__subplot_fit_region(fit_ci_7x7, plot_path, plot_patch):
    aplt.subplot_fit_ci_region(
        fit=fit_ci_7x7,
        region="serial_fpr",
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "subplot_1d_fit_ci_serial_fpr.png") in plot_patch.paths


def test__subplot_noise_scaling_map_dict(fit_ci_7x7, plot_path, plot_patch):
    aplt.subplot_noise_scaling_map_dict(
        fit=fit_ci_7x7, output_path=plot_path, output_format="png"
    )

    assert (
        str(Path(plot_path) / "subplot_noise_scaling_map_dict.png") in plot_patch.paths
    )


def test__subplot_fit_list(fit_ci_7x7, plot_path, plot_patch):
    aplt.subplot_fit_ci_list(
        fit_list=[fit_ci_7x7, fit_ci_7x7],
        quantity="chi_squared_map",
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "subplot_chi_squared_map_list.png") in plot_patch.paths


def test__subplot_fit_region_list(fit_ci_7x7, plot_path, plot_patch):
    aplt.subplot_fit_ci_region_list(
        fit_list=[fit_ci_7x7, fit_ci_7x7],
        region="parallel_eper",
        output_path=plot_path,
        output_format="png",
    )

    assert (
        str(Path(plot_path) / "subplot_data_list_parallel_eper.png") in plot_patch.paths
    )


def test__fits_fit(fit_ci_7x7, tmp_path):
    aplt.fits_fit_ci(fit=fit_ci_7x7, output_path=tmp_path)

    assert (Path(tmp_path) / "fit.fits").exists()
