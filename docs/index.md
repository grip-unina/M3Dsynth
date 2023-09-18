---
layout: paper
paper: M3Dsynth&colon; A dataset of medical 3D images with AI-generated local manipulations 
github_url: https://github.com/grip-unina/M3Dsynth
authors:  
  - name: Giada Zingarini
    link: https://www.grip.unina.it/members/zingarini
    index: 1
  - name: Davide Cozzolino
    link: https://www.grip.unina.it/members/cozzolino
    index: 1
  - name: Riccardo Corvi
    link: https://www.grip.unina.it/members/corvi
    index: 1
  - name: Giovanni Poggi
    link: https://www.grip.unina.it/members/poggi
    index: 1
  - name: Luisa Verdoliva
    link: https://www.grip.unina.it/members/verdoliva
    index: 1
affiliations: 
  - name: University Federico II of Naples, Italy
    index: 1
---

[![Github](https://img.shields.io/badge/Github%20page-222222.svg?style=for-the-badge&logo=github)](https://github.com/grip-unina/M3Dsynth/)
[![GRIP](https://img.shields.io/badge/-GRIP-0888ef.svg?style=for-the-badge)](https://www.grip.unina.it)

<center><img src="./images.png" alt="images" width="500pt" /></center>

The ability to detect manipulated visual content is becoming increasingly important in many application fields, given the rapid advances in image synthesis methods. 
Of particular concern is the possibility of modifying the content of medical images, altering the resulting diagnoses. Despite its relevance, this issue has received limited attention from the research community. One reason is the lack of large and curated datasets to use for development and benchmarking purposes. Here, we investigate this issue and propose **M3Dsynth**, a large dataset of manipulated Computed Tomography (CT) lung images.
We create manipulated images by injecting or removing lung cancer nodules in real CT scans, 
using three different methods based on Generative Adversarial Networks (GAN) or Diffusion Models (DM), for a total of 8,577 manipulated samples. 
Experiments show that these images easily fool automated diagnostic tools. 
We also tested several state-of-the-art forensic detectors and demonstrated that, 
once trained on the proposed dataset, they are able to accurately detect and localize manipulated synthetic content,
including when training and test sets are not aligned, showing good generalization ability.

## Bibtex 

```
@article{zingarini2023m3dsynth,
  author={Giada Zingarini and Davide Cozzolino and Riccardo Corvi and Giovanni Poggi and Luisa Verdoliva},
  title={M3Dsynth: A dataset of medical 3D images with AI-generated local manipulations},   
  journal={arXiv preprint arXiv:2309.07973},
  year={2023}
}
```
  
## Acknowledgments
 
We gratefully acknowledge the support of this research by the Defense Advanced Research Projects Agency (DARPA) under agreement number FA8750-20-2-1004.
The U.S. Government is authorized to reproduce and distribute reprints for Governmental purposes notwithstanding any copyright notation thereon.
The views and conclusions contained herein are those of the authors and should not be interpreted as necessarily representing the official policies or endorsements, either expressed or implied, of DARPA or the U.S. Government.

This work has also received funding by the European Union under the Horizon Europe vera.ai project, Grant Agreement number 101070093, and is supported by a TUM-IAS Hans Fischer Senior Fellowship and by PREMIER funded by the Italian Ministry of Education, University, and Research within the PRIN 2017 program.
