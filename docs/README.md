---
layout: home
permalink: index.html

# Please update this with your repository name and title
repository-name: e19-4yp-Active-bionic-antennas-for-object-detection-and-3D-localization-with-ego-motion-cancellation
title: Active-bionic-antennas-for-object-detection-and-3D-localization-with-ego-motion-cancellation
---

[comment]: # "This is the standard layout for the project, but you can clean this and use your own template"

# Active Bionic Antennas for Object Detection and 3D Localization with Ego-Motion Cancellation

#### Team

- E/19/295, Janitha Dilshan, [email](mailto:e19295@eng.pdn.ac.lk)
- E/19/300, Asela Hemantha, [email](mailto:e19300@eng.pdn.ac.lk)
- E/19/495, Dulshan Chamuditha, [email](mailto:e19495@eng.pdn.ac.lk)

#### Supervisors

- Dr. Nalin Harischandra, [email](mailto:nalin@eng.pdn.ac.lk)
- Dr. Isuru Nawinne, [email](mailto:isurunawinne@eng.pdn.ac.lk)

#### Table of content

1. [Abstract](#abstract)
2. [Related works](#related-works)
3. [Methodology](#methodology)
4. [Experiment Setup and Implementation](#experiment-setup-and-implementation)
5. [Results and Analysis](#results-and-analysis)
6. [Conclusion](#conclusion)
7. [Publications](#publications)
8. [Links](#links)

---

## Abstract

Inspired by biological systems such as insect antennae and mammalian whiskers, this project focuses on developing bionic tactile sensors for robotic platforms. These sensors enable object detection and 3D localization in unstructured environments. A major innovation is the cancellation of self-induced sensory interference (ego-motion) using Echo State Networks (ESNs). The system improves spatial awareness and mapping by integrating tactile sensing with proprioceptive feedback and adaptive learning.

---

## Related works

The literature survey explores bio-inspired tactile sensors, particularly in insects and mammals, highlighting key features such as mechanoreception, active exploration, and adaptation. Early research in robotic whiskers and antennae showed promise but struggled with motion noise. Recent studies introduced ESNs, deep learning, and reinforcement learning for filtering self-sensing artifacts and improving localization in robotics.

---

## Methodology

- Design of bionic tactile antennae using servo-actuated flexible probes  
- Sensor integration with MPU6050 IMUs and vibration monitoring  
- Data acquisition at 100Hz and preprocessing using Kalman and low-pass filters  
- Training ESNs offline to model and subtract ego-motion signals  
- Adapting Google Cartographer SLAM to use tactile input for mapping  
- Multi-contact strategies for enhanced spatial resolution  

---

## Experiment Setup and Implementation

- 4WD Omni-directional mobile platform  
- Jetson Nano for processing and inference  
- Dual bionic antennae each with IMU sensors and servo control  
- Real-time filtering of vibration data via trained ESNs  
- Mapping performed using modified Cartographer SLAM stack in ROS  
- Evaluation in structured and unstructured test environments  

---

## Results and Analysis

- ESNs achieved over 90% accuracy in predicting self-induced vibrations  
- Significant reduction in false positive detections  
- Improved localization accuracy under low-light and visually degraded conditions  
- Demonstrated robust tactile mapping in environments where vision/LiDAR fail  

---

## Conclusion

This project successfully demonstrates the potential of biologically-inspired tactile sensing combined with machine learning for robust robotic navigation. The integration of self-sensing cancellation and tactile-based SLAM opens new possibilities for exploration, disaster response, and industrial applications.

---

## Publications

<!-- 1. [Semester 7 report](./) -->
<!-- 2. [Semester 7 slides](./) -->
<!-- 3. [Semester 8 report](./) -->
<!-- 4. [Semester 8 slides](./) -->
<!-- 5. Janitha D., Asela H., Dulshan C., “Active Bionic Antennas for Object Detection and 3D Localization with Ego-Motion Cancellation”, (2025). [PDF](./) -->

---

## Links

- [Project Repository](https://github.com/cepdnaclk/e19-4yp-Active-bionic-antennas-for-object-detection-and-3D-localization-with-ego-motion-cancellation)
- [Project Page](https://cepdnaclk.github.io/e19-4yp-Active-bionic-antennas-for-object-detection-and-3D-localization-with-ego-motion-cancellation)
- [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- [University of Peradeniya](https://eng.pdn.ac.lk/)
