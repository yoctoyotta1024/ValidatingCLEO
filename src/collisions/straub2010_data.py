"""
Copyright (c) 2026 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: straub2010_data.py
Project: collisions
Created Date: Thursday 1st January 1970
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Friday 13th March 2026
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
"""


def get_straub_fig10_data():
    """function copied and adapted from PySDM v3.0.0-pre.15 examples folder:
    examples/PySDM_examples/deJong_Mackay_et_al_2023/simulation_ss.py"""
    import numpy as np

    graph_x = np.array(
        [
            0.08988764,
            0.086142322,
            0.097378277,
            0.108614232,
            0.119850187,
            0.142322097,
            0.164794007,
            0.194756554,
            0.224719101,
            0.262172285,
            0.314606742,
            0.36329588,
            0.419475655,
            0.479400749,
            0.558052434,
            0.68164794,
            0.816479401,
            0.943820225,
            1.071161049,
            1.213483146,
            1.370786517,
            1.617977528,
            1.865168539,
            2.074906367,
            2.322097378,
            2.546816479,
            2.801498127,
            3.018726592,
            3.220973783,
            3.378277154,
            3.543071161,
            3.651685393,
        ]
    )  # [mm]

    graph_log_y = np.array(
        [
            1.055803251,
            1.003199334,
            1.14357294,
            1.316140369,
            1.509917836,
            1.811447329,
            2.159352957,
            2.607176908,
            3.048912888,
            3.453402358,
            3.849578422,
            3.955529874,
            3.849578422,
            3.634485506,
            3.328848104,
            2.897005075,
            2.525213782,
            2.294463222,
            2.125139584,
            2.045222871,
            2.02571776,
            2.032198707,
            2,
            1.930947254,
            1.811447329,
            1.685826681,
            1.531778159,
            1.389585281,
            1.262606891,
            1.169430766,
            1.069379699,
            1.0064089029687935,
        ]
    )

    return graph_x, np.power(10, graph_log_y)
