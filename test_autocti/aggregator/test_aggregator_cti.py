import pytest

import autocti as ac

from test_autocti.aggregator.conftest import clean, aggregator_from

database_file = "db_cti_gen"


def test__cti_randomly_drawn_via_pdf_gen_from(
    dataset_1d_7, clocker_1d, samples_1d, model_1d
):
    analysis = ac.AnalysisDataset1D(dataset=dataset_1d_7, clocker=clocker_1d)

    def save_results_combined(paths, result):
        pass

    analysis.save_results_combined = save_results_combined

    agg = aggregator_from(
        database_file=database_file,
        analysis=analysis,
        model=model_1d,
        samples=samples_1d,
    )

    cti_agg = ac.agg.CTIAgg(aggregator=agg)
    cti_pdf_gen = cti_agg.randomly_drawn_via_pdf_gen_from(total_samples=2)

    i = 0

    for cti_gen in cti_pdf_gen:
        for cti in cti_gen:
            i += 1

            assert cti.trap_list[0].density == pytest.approx(10.0, 1.0e-4)

    assert i == 2

    clean(database_file=database_file)


def test__cti_all_above_weight_gen(dataset_1d_7, clocker_1d, samples_1d, model_1d):
    analysis = ac.AnalysisDataset1D(dataset=dataset_1d_7, clocker=clocker_1d)

    agg = aggregator_from(
        database_file=database_file,
        analysis=analysis,
        model=model_1d,
        samples=samples_1d,
    )

    cti_agg = ac.agg.CTIAgg(aggregator=agg)
    cti_pdf_gen = cti_agg.all_above_weight_gen_from(minimum_weight=-1.0)

    i = 0

    for cti_gen in cti_pdf_gen:
        for cti in cti_gen:
            i += 1

            # Each above-weight sample's own instance (samples_1d: all 1.0, then
            # all 10.0), not the max likelihood instance repeated.
            if i == 1:
                assert cti.trap_list[0].density == pytest.approx(1.0, 1.0e-4)

            if i == 2:
                assert cti.trap_list[0].density == pytest.approx(10.0, 1.0e-4)

    assert i == 2

    clean(database_file=database_file)


def test__cti_max_log_likelihood_gen__factor_graph_returns_one_cti_per_dataset(
    dataset_1d_7, clocker_1d, samples_1d, model_1d
):
    # A multi-dataset fit is a FactorGraphModel: its instance has one child per
    # dataset rather than a top-level `cti` attribute.
    analysis = ac.AnalysisDataset1D(dataset=dataset_1d_7, clocker=clocker_1d)

    agg = aggregator_from(
        database_file=database_file,
        analysis=[analysis, analysis],
        model=model_1d,
        samples=samples_1d,
    )

    cti_agg = ac.agg.CTIAgg(aggregator=agg)

    i = 0

    for cti_list in cti_agg.max_log_likelihood_gen_from():
        i += 1

        assert len(cti_list) == 2

        for cti in cti_list:
            assert cti.trap_list[0].density == pytest.approx(10.0, 1.0e-4)

    assert i == 1

    clean(database_file=database_file)


def test__cti_object_via_gen_from__uses_input_instance(
    dataset_1d_7, clocker_1d, samples_1d, model_1d
):
    analysis = ac.AnalysisDataset1D(dataset=dataset_1d_7, clocker=clocker_1d)

    agg = aggregator_from(
        database_file=database_file,
        analysis=analysis,
        model=model_1d,
        samples=samples_1d,
    )

    instance = model_1d.instance_from_prior_medians()
    instance.cti.trap_list[0].density = 123.0

    cti_agg = ac.agg.CTIAgg(aggregator=agg)

    cti = cti_agg.object_via_gen_from(fit=list(agg)[0], instance=instance)

    assert cti.trap_list[0].density == pytest.approx(123.0, 1.0e-4)

    clean(database_file=database_file)
