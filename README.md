# asp-tutorials

Launch a preconfigured computing environment with interactive example notebooks for [Ames Stereo Pipeline](ASP) processing on [BinderHub](https://mybinder.org) or [GitHub Codespaces](https://github.com/features/codespaces)

### Launch on GitHub Codespaces (preferred way)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/uw-cryo/asp_tutorials?quickstart=1)

☝️ this button will launch an Cloud-hosted computer on Microsoft Azure with a VSCode interface. GitHub currently gives every user [120 vCPU hours per month for free](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#monthly-included-storage-and-core-hours-for-personal-accounts), beyond that you must pay. **So be sure to explicitly stop or shut down your codespace when you are done by going to this page (https://github.com/codespaces/).**

* More details on codespace lifecycle is explained [here](https://docs.github.com/en/codespaces/getting-started/the-codespace-lifecycle#). 

### Launch on Mybinder.org
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/uw-cryo/asp_tutorials/master?labpath=tutorials%2Fexample-aster_stereo_reconstruction.ipynb)
☝️ this button will launch an *ephemeral* Cloud-hosted computer with a JupyterLab interface that is convenient for demos. The computing cost is graciously supported by the scientific community (https://binderhub.readthedocs.io/en/stable/federation/federation.html) but you do not have control over computing resources (which are typically limited to 2vCPU and 4GB RAM), and files are not saved between sessions.

### Usage
Once launched, open the example-aster\_on\_pangeo\_binder\_demo.ipynb from the left directory panel and run the cells to execute the interactive tutorial.

### Sample L1A ASTER stereo images 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7972223.svg)](https://doi.org/10.5281/zenodo.7972223)
* The tutorial uses sample L1A stereo images acquired by the ASTER instrument over Mt. Rainier, WA on July 31, 2017 (AST_L1A_00307312017190728_20200218153629_19952.zip)
* More details can be found on the data product page: https://lpdaac.usgs.gov/products/ast_l1av003/
* The sample data were downloaded from the [NASA EarthData website](https://www.earthdata.nasa.gov/). We are rehosting on Zenodo to enable on-demand access to the sample images when running the tutorial.

### Example output
![Example DEM produced from the ASTEER tutorial](./assets/images/asp_aster_output_plot.jpg)
Figure: Example output DEM produced from ASTER imagery acquired over Mt. Rainier. Top Row: Orthorectified A) left  and B) right stereo images. Middle Row: Disparity in C) x (E-W) and D) y (N-S) direction. Bottom Row: E) Intersection error and F) Digital Elevation Model.
