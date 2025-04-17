/*
 * Copyright (c) 2025 MPI-M, Clara Bayley
 *
 *
 * ----- ValidatingCLEO -----
 * File: main_testikstraub.cpp
 * Project: collisions
 * Created Date: Friday 11th April 2025
 * Author: Clara Bayley (CB)
 * Additional Contributors:
 * -----
 * Last Modified: Wednesday 16th April 2025
 * Modified By: CB
 * -----
 * License: BSD 3-Clause "New" or "Revised" License
 * https://opensource.org/licenses/BSD-3-Clause
 * -----
 * File Description:
 * Program for CLEO 0-D box model of collisions as in Shima et al. 2009
 * with coalescence, rebound and breakup with glag decided based on section 4 of
 * Testik et al. 2011 (figure 12) as well as coalescence efficiency from
 * Straub et al. 2010.
 */

#include "./main_supplement.hpp"

inline MicrophysicalProcess auto create_microphysics(const Config &config,
  const Timesteps &tsteps) {
const PairProbability auto collprob = LongHydroProb();
const NFragments auto nfrags = CollisionKineticEnergyNFrags{};
const CoalBuReFlag auto coalbure_flag = TSCoalBuReFlag{};
const MicrophysicalProcess auto colls =
CoalBuRe(tsteps.get_collstep(), &step2realtime, collprob, nfrags, coalbure_flag);
return colls;
}

template <typename Store>
inline auto create_sdm(const Config &config, const Timesteps &tsteps, Dataset<Store> &dataset) {
  const auto couplstep = (unsigned int)tsteps.get_couplstep();
  const GridboxMaps auto gbxmaps(create_gbxmaps(config));
  const MicrophysicalProcess auto microphys(create_microphysics(config, tsteps));
  const MoveSupersInDomain movesupers(create_movement(gbxmaps));
  const Observer auto obs(create_observer(config, tsteps, dataset));

  return SDMMethods(couplstep, gbxmaps, microphys, movesupers, obs);
}

int main(int argc, char *argv[]) {
  if (argc < 2) {
    throw std::invalid_argument("configuration file(s) not specified");
  }

  MPI_Init(&argc, &argv);

  int comm_size;
  MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
  if (comm_size > 1) {
    std::cout << "ERROR: The current example is not prepared"
              << " to be run with more than one MPI process" << std::endl;
    MPI_Abort(MPI_COMM_WORLD, 1);
  }

  Kokkos::Timer kokkostimer;

  /* Read input parameters from configuration file(s) */
  const std::filesystem::path config_filename(argv[1]);  // path to configuration file
  const Config config(config_filename);

  /* Initialise Kokkos parallel environment */
  Kokkos::initialize(config.get_kokkos_initialization_settings());
  {
    Kokkos::print_configuration(std::cout);

    /* Create timestepping parameters from configuration */
    const Timesteps tsteps(config.get_timesteps());

    /* Create Xarray dataset wit Zarr backend for writing output data to a store */
    auto store = FSStore(config.get_zarrbasedir());
    auto dataset = Dataset(store);

    /* CLEO Super-Droplet Model (excluding coupled dynamics solver) */
    const SDMMethods sdm(create_sdm(config, tsteps, dataset));

    /* Create coupldyn solver and coupling between coupldyn and SDM */
    const CoupledDynamics auto coupldyn = NullDynamics(tsteps.get_couplstep());
    const CouplingComms<CartesianMaps, NullDynamics> auto comms = NullDynComms{};

    /* Initial conditions for CLEO run */
    const InitialConditions auto initconds = create_initconds(config, sdm.gbxmaps);

    /* Run CLEO (SDM coupled to dynamics solver) */
    const RunCLEO runcleo(sdm, coupldyn, comms);
    runcleo(initconds, tsteps.get_t_end());
  }
  Kokkos::finalize();

  const auto ttot = double{kokkostimer.seconds()};
  std::cout << "-----\n Total Program Duration: " << ttot << "s \n-----\n";

  MPI_Finalize();

  return 0;
}
