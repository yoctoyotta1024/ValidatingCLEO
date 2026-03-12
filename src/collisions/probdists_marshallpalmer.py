"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: probdists_marshallpalmer.py
Project: collisions
Created Date: Thursday 12th March 2026
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 12th March 2026
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
probdist for marshall palmer as in de Jong et al. 2023.
"""


import numpy as np


class SampleRadiiMarshallPalmer:
    def __init__(self, rspan):
        self.rspan = rspan  # [min, max] radii to sample between [m]

    def __call__(self, nsupers):
        """evenly in log-space superdroplet radii between rspan[0] and rspan[1]"""
        redges = np.logspace(
            np.log10(self.rspan[0]), np.log10(self.rspan[1]), nsupers + 1
        )
        r_cens = (redges[1:] + redges[:-1]) / 2

        return r_cens  # units [m]


class SampleXiMarshallPalmer:
    def __init__(self, rspan, volume):
        self.rspan = rspan  # [min, max] radii to sample between [m]
        self.volume = volume

        rain_rate = 54  # mm/hr
        self.lamda = 4.1e3 * (rain_rate ** (-0.21))  # m^-1
        self.norm0 = 8e6  # m^-3 m^-1

    def __call__(self, radii, totxi):
        xi = self.calc_xi(radii)
        normalised = xi / np.sum(xi)
        return normalised

    def calc_numconc(self):
        exp_diff = self._calc_exp(self.rspan[1]) - self._calc_exp(self.rspan[0])
        numconc_in_rspan = self.norm0 / (-2.0 * self.lamda) * exp_diff
        return numconc_in_rspan

    def calc_xi(self, radii):
        nsupers = len(radii)
        redges = np.logspace(
            np.log10(self.rspan[0]), np.log10(self.rspan[1]), nsupers + 1
        )
        r_cens = (redges[1:] + redges[:-1]) / 2
        r_widths = redges[1:] - redges[:-1]
        assert np.all(r_cens - radii < 1e-20)

        xi = self._probdistrib(r_cens) * r_widths * self.volume

        return xi

    def _calc_exp(self, radius):
        return np.exp(-1.0 * self.lamda * (radius * 2))

    def _probdistrib(self, radii):
        """Returns probability of each radius in radii according to
        Marshall Palmer distribution as in de Jong et al. 2023
        (and same as Straub et al. 2010)."""
        prob_dist = self.norm0 * self._calc_exp(radii)  # m^-3 m^-1
        return prob_dist


def get_marshall_palmer_generators(rspan, volume):
    radiigen = SampleRadiiMarshallPalmer(rspan)
    xiprobdist = SampleXiMarshallPalmer(rspan, volume)

    return radiigen, xiprobdist
