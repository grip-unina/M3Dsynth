# M3Dsynth: A dataset of medical 3D images with AI-generated local manipulations 

[![Github](https://img.shields.io/badge/Github%20webpage-222222.svg?style=for-the-badge&logo=github)](https://grip-unina.github.io/M3Dsynth/)
[![arXiv](https://img.shields.io/badge/-arXiv-B31B1B.svg?style=for-the-badge)](https://arxiv.org/abs/2309.07973)
[![GRIP](https://img.shields.io/badge/-GRIP-0888ef.svg?style=for-the-badge)](https://www.grip.unina.it)

This is the official repository of the paper:
[M3Dsynth: A dataset of medical 3D images with AI-generated local manipulations](https://arxiv.org/abs/2309.07973)

Giada Zingarini, Davide Cozzolino, Riccardo Corvi, Giovanni Poggi, and Luisa Verdoliva

<p align="center">
 <img src="./docs/images.png" alt="preview" width="80%" />
</p>

## Overview

The ability to detect manipulated visual content is becoming increasingly important in many application fields, given the rapid advances in image synthesis methods. 
Of particular concern is the possibility of modifying the content of medical images, altering the resulting diagnoses. Despite its relevance, this issue has received limited attention from the research community. One reason is the lack of large and curated datasets to use for development and benchmarking purposes. Here, we investigate this issue and propose **M3Dsynth**, a large dataset of manipulated Computed Tomography (CT) lung images.
We create manipulated images by injecting or removing lung cancer nodules in real CT scans, 
using three different methods based on Generative Adversarial Networks (GAN) or Diffusion Models (DM), for a total of 8,577 manipulated samples. 
Experiments show that these images easily fool automated diagnostic tools. 
We also tested several state-of-the-art forensic detectors and demonstrated that, 
once trained on the proposed dataset, they are able to accurately detect and localize manipulated synthetic content,
including when training and test sets are not aligned, showing good generalization ability.

## Requirements

![tqdm](https://img.shields.io/badge/tqdm-grey.svg?style=plastic)
![pillow](https://img.shields.io/badge/pillow-grey.svg?style=plastic)
![numpy](https://img.shields.io/badge/numpy-grey.svg?style=plastic)
![pydicom](https://img.shields.io/badge/pydicom-grey.svg?style=plastic)
![matplotlib](https://img.shields.io/badge/matplotlib-grey.svg?style=plastic)

## Dataset

**M3Dsynth** dataset relies on the Computed Tomography (CT) lung scans of the LIDC-IDRI dataset [A].
To download real CT scans in dicom format, see the official web page of LIDC-IDRI dataset [here](https://www.cancerimagingarchive.net/collection/lidc-idri/).
While, the manipulated CT scans can be downloaded [here](https://www.grip.unina.it/download/prog/M3Dsynth/) or using the following script:

```
bash ./get_M3Dsynth.sh PATH_LIDC_IDRI OUTPUT_DIR_PATH
```

[A] Armato SG 3rd, et al. "The Lung Image Database Consortium (LIDC) and Image Database Resource Initiative (IDRI): A completed reference database of lung nodules on CT scans." Medical Physics, 2011. doi.org/10.1118/1.3528204

## License

The license of the datasat can be found in the LICENSE.md file.

## Bibtex 
```
@article{zingarini2023m3dsynth,
  title={{M3Dsynth}: A dataset of medical 3D images with AI-generated local manipulations}, 
  author={Giada Zingarini and Davide Cozzolino and Riccardo Corvi and Giovanni Poggi and Luisa Verdoliva},
  journal={arXiv preprint arXiv:2309.07973},
  year={2023}
}
```
