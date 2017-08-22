# pyhardrat
![alt text](https://github.com/grburgess/pyhardrat/blob/master/Cyborg-Rats.png)

pyhardrat calculates photon/energy model hardness ratios from fitted GBM catalog models for a user specified energy range

## Install

pip install  git+https://github.com/grburgess/pyhardrat.git

## Usage

```python
from pyhardrat import *

hrb = HardnessDurationBuilder()

hrb.catalog.query('.01<t90<5')

hrb.build_sample()

hrb.compute_hardness_ratios(10,50,50,300)


```
