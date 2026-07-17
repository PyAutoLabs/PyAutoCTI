from autofit.non_linear import result


class Result(result.Result):
    def __init__(
        self,
        samples_summary,
        paths=None,
        samples=None,
        analysis=None,
        search_internal=None,
    ):
        """
        The result of a phase
        """
        super().__init__(
            samples_summary=samples_summary,
            paths=paths,
            samples=samples,
            search_internal=search_internal,
            analysis=analysis,
        )

    @property
    def analysis_unwrapped(self):
        """
        The CTI analysis this result was inferred from.

        A multi-dataset fit via a factor graph gives each child result an
        `AnalysisFactor` wrapper as its analysis, which does not delegate
        attribute access to the analysis it wraps — so it is unwrapped here
        (the same unwrap PyAutoFit performs when dispatching combined
        visualization).
        """
        return getattr(self.analysis, "analysis", self.analysis)

    @property
    def clocker(self):
        return self.analysis_unwrapped.clocker


class ResultDataset(Result):
    @property
    def max_log_likelihood_fit(self):
        return self.analysis_unwrapped.fit_via_instance_from(instance=self.instance)

    @property
    def mask(self):
        return self.max_log_likelihood_fit.mask
