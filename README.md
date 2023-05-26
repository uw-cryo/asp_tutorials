# asp-binder demo

Launch a preconfigured computing environment with example notebooks for [Ames Stereo Pipeline](ASP) on [BinderHub](https://mybinder.org) or [GitHub Codespaces](https://github.com/features/codespaces)

### Launch on GitHub Codespaces
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/uw-cryo/asp-binder-demo?quickstart=1)

☝️ this button will launch an Cloud-hosted computer on Microsoft Azure with a VSCode interface. GitHub currently gives every user [120 vCPU hours per month for free](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#monthly-included-storage-and-core-hours-for-personal-accounts), beyond that you must pay. **So be sure to explicitly stop or shut down your codespace when you are done by going to this page (https://github.com/codespaces/).**

* More details on codespace lifecycle is explained [here](https://docs.github.com/en/codespaces/getting-started/the-codespace-lifecycle#). 

### Launch on Mybinder.org
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/uw-cryo/asp-binder-demo/binder?urlpath=git-pull?repo=https://github.com/uw-cryo/asp-binder-demo%26amp%3Bbranch=master%26amp%3Burlpath=lab/tree/asp-binder-demo/example.ipynb/%3Fautodecode)

☝️ this button will launch an *ephemeral* Cloud-hosted computer with a JupyterLab interface that is convenient for demos. The computing cost is graciously supported by the scientific community (https://binderhub.readthedocs.io/en/stable/federation/federation.html) but you do not have control over computing resources (which are typically limited to 2vCPU and 4GB RAM), and files are not saved between sessions.

### Usage
Once launched, open the example-aster\_on\_pangeo\_binder\_demo.ipynb from the left directory panel and run the cells to execute the interactive tutorial.

### Sample L1A stereo 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7972223.svg)](https://doi.org/10.5281/zenodo.7972223)
* The tutorial uses an Aster Stereo collected over Mt. Rainier, WA on July 31st 2017. 
* The sample data was downloaded from the [NASA EarthData website](https://www.earthdata.nasa.gov/).
* We have hosted the data on zenodo, which is downloaded on the fly during the tutorial.
