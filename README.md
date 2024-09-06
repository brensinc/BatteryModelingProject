# Battery State of Charge Model

## Overview
This project, started during the fall of my sophomore year, aims to simulate a battery’s State of Charge (SOC) and State of Health (SOH) over time. The model leverages electric current and ambient temperature to estimate these parameters, allowing for robust analysis and optimization of battery performance.

The project is still under development, with core features in place but further refinements needed. Current functionalities include creating a battery object, interpolating voltage data, and simulating the impact of environmental factors on battery health.

## Features
- **Voltage Interpolation**: Developed a robust voltage interpolation model using cubic spline fitting to estimate open circuit voltage for batteries of varying capacities and SOC.
- **SOC & SOH Simulation**: Implemented logic to simulate how a battery’s state of charge and health evolve over time based on external conditions such as temperature and current.
- **Data Pipeline**: Built a pipeline for data preprocessing, reducing dimensionality and incorporating battery state of charge into the analysis.
- **Incomplete Implementation**: The current version of the program is incomplete, with ongoing work to refine the SOC and SOH relationship models.

## References
The following articles were referenced during the development of this model:

- Lin, X., Perez, H. E., Mohan, S., Siegel, J. B., Stefanopoulou, A. G., Ding, Y., & Castanier, M. P. (2014). *A lumped-parameter electro-thermal model for cylindrical batteries*. Journal of Power Sources, 257, 1-11.
  
- Perez, H. E., Hu, X., Dey, S., & Moura, S. J. (2017). *Optimal charging of Li-Ion batteries with coupled electro-thermal-aging dynamics*. IEEE Transactions on Vehicular Technology, 66(9), 7761-7770.
  
- Perez, H. E., Siegel, J. B., Lin, X., Stefanopoulou, A. G., Ding, Y., & Castanier, M. P. (2012). *Parameterization and validation of an integrated electro-thermal cylindrical LFP battery model*. In ASME 2012 5th Annual Dynamic Systems and Control Conference, Fort Lauderdale, Florida.
