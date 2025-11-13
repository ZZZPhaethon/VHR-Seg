# Install

## Prerequisites

In this section we demonstrate how to prepare an environment with PyTorch.

VHR-Seg works on Linux. It requires Python 3.10+, CUDA 10.2+ and PyTorch 1.8+, GDAL3.7+.

**Note:**
If you are experienced with PyTorch and have already installed it, just skip this part and jump to the [next section](##installation). Otherwise, you can follow these steps for the preparation.

**Step 0.** Download and install Miniconda from the [official website](https://docs.conda.io/en/latest/miniconda.html).

```shell
conda --version
# Should print: conda <some version>
```
If an error is reported, install `miniconda`
from https://docs.conda.io/en/latest/miniconda.html or use `miniforge`, which provides `mamba` as a
faster alternative:
https://github.com/conda-forge/miniforge

Next, update conda:

```shell
conda update -n base -c conda-forge conda -y
```
**Step 1.** 
Create an environment and activate it. Be sure to use Python __3.10__ as shown.

```shell
conda create -n vhrseg python=3.10 -y
conda activate vhrseg
```

**Step 2.** Update pip and install the project dependencies:

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 3.** Install PyTorch following [official instructions](https://pytorch.org/get-started/locally/), e.g.

On GPU platforms:

```shell
conda install pytorch torchvision -c pytorch
```

On CPU platforms:

```shell
conda install pytorch torchvision cpuonly -c pytorch
```

**Step 4.** Install [MMCV](https://github.com/open-mmlab/mmcv) using [MIM](https://github.com/open-mmlab/mim).

```shell
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0"
```

**Step 5.** Install MMSegmentation and MMDetection.

Case a: If you develop and run mmseg directly, install it from source:

```shell
git clone -b main https://github.com/open-mmlab/mmsegmentation.git
cd mmsegmentation
pip install -v -e .
# '-v' means verbose, or more output
# '-e' means installing a project in editable mode,
# thus any local modifications made to the code will take effect without reinstallation.
```

Case b: If you use mmsegmentation as a dependency or third-party package, install it with pip:

```shell
pip install "mmsegmentation>=1.0.0"
```

Install MMDetection:

```shell
pip install git+https://github.com/open-mmlab/mmdetection@ecac3a77becc63f23d9f6980b2a36f86acd00a8a
```

**Step 6.** Install GDAL. [GDAL](https://gdal.org/) is a translator library for raster and vector geospatial data formats. Install GDAL to read complex formats and extremely large remote sensing images.

```shell
conda install GDAL=3.7.2
```

