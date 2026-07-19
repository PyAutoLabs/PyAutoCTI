from __future__ import annotations
import os
from pathlib import Path
from typing import List, Union

from autonerves import conf


def setting(section: Union[List[str], str], name: str):
    if isinstance(section, str):
        return conf.instance["visualize"]["plots"][section][name]

    for sect in reversed(section):
        try:
            return conf.instance["visualize"]["plots"][sect][name]
        except KeyError:
            continue

    return conf.instance["visualize"]["plots"][section[0]][name]


def plot_setting(section: Union[List[str], str], name: str) -> bool:
    return setting(section, name)


class Plotter:
    def __init__(self, image_path: Union[Path, str], title_prefix: str = None):
        """
        Base class for the plotters which output visualization during a model fit.

        The methods of a `Plotter` are called throughout a non-linear search via the `Analysis` and
        `Visualizer` classes.

        The images output by a `Plotter` are customized using the file `config/visualize.yaml`.

        Parameters
        ----------
        image_path
            The path on the hard-disk to the `image` folder of the non-linear search results, where all
            visualization is saved.
        title_prefix
            An optional string prefixed to every plot title.
        """
        self.image_path = Path(image_path)
        self.title_prefix = title_prefix

        os.makedirs(image_path, exist_ok=True)

    @property
    def fmt(self) -> List[str]:
        """The output file format(s) read from the `subplot_format` visualize config entry."""
        try:
            return conf.instance["visualize"]["plots"]["subplot_format"]
        except KeyError:
            return "png"
