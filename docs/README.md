---
layout: home
permalink: index.html

repository-name: e19-4yp-Active-bionic-antennas-for-object-detection-and-3D-localization-with-ego-motion-cancellation
title: Active Bionic Antennas for Object Detection and 3D Localization with Ego-Motion Cancellation
---

# Active Bionic Antennas for Object Detection and 3D Localization with Ego-Motion Cancellation

---

###  Team

- **E/19/295** Janitha Dilshan — [e19295@eng.pdn.ac.lk](mailto:e19295@eng.pdn.ac.lk)
- **E/19/300** Asela Hemantha — [e19300@eng.pdn.ac.lk](mailto:e19300@eng.pdn.ac.lk)
- **E/19/495** Dulshan Chamuditha — [e19495@eng.pdn.ac.lk](mailto:e19495@eng.pdn.ac.lk)

###  Supervisors

- **Dr. Nalin Harischandra** — [nalin@eng.pdn.ac.lk](mailto:nalin@eng.pdn.ac.lk)  
- **Dr. Isuru Nawinne** — [isurunawinne@eng.pdn.ac.lk](mailto:isurunawinne@eng.pdn.ac.lk)

---

##  Table of Contents

1. [Abstract](#abstract)
2. [Related Works](#related-works)
3. [Methodology](#methodology)
4. [System Architecture and Implementation](#system-architecture-and-implementation)
5. [Results and Analysis](#results-and-analysis)
6. [Conclusion](#conclusion)
7. [Publications](#publications)
8. [Links](#links)

---

##  Abstract

Inspired by the tactile sensing mechanisms of insects and mammals, this project presents a biologically-inspired bionic antenna system capable of **3D object detection and localization**. The system cancels **ego-motion artifacts** using **Echo State Networks (ESNs)**, enabling robust performance in vision-impaired environments. Key applications include **autonomous robotics**, **search and rescue**, and **industrial inspection**.

---

##  Related Works

- Previous tactile sensors like **robotic whiskers** and **flexible antennae** showed promise but struggled with motion-induced noise.
- Modern research applies **reservoir computing** and **deep learning** for proprioceptive signal processing and localization.
- Our system extends this by incorporating **real-time motion cancellation** using ESNs.

---

##  Methodology

- Design of flexible, servo-actuated antennae mimicking insect behavior.
- Integration of IMU sensors (MPU6050) and vibration data acquisition at ~130Hz.
- Application of Butterworth and band-pass filters to preprocess raw vibration signals.
- Offline training of Echo State Networks (ESNs) to model and cancel self-induced motion noise.


---

##  System Architecture and Implementation

- **Mobile Platform**: 4WD robot car.
- **Processing Unit**: NVIDIA Jetson Nano for ESN inference.
- **Sensor Module**:
  - flexible bionic antennae with servo motion.
  - MPU6050 IMUs to capture vibration and acceleration.
- **Software Stack**:
  - Real-time ESN-based ego-motion cancellation.


---

##  Results and Analysis

- **Reduced False Positives**: Ego-motion noise cancellation improved detection accuracy.
- **Improved Localization**: Antenna-based mapping functioned well in degraded environments (e.g., low light, dust).
- **High Tactile Sensitivity**: System responded reliably to light object contact, suitable for fragile environment exploration.
- **Limitations**:
  - Antenna accuracy depends on servo resolution and noise.
  - Slight inconsistency due to mechanical vibration in low-quality servo motors.

---

##  Conclusion

This project demonstrates the **first integration of bionic antennae with ESN-based ego-motion cancellation** into a mobile robotic system . The platform can effectively navigate environments unsuitable for visual or LiDAR sensing, opening up new domains for **tactile-based autonomy** in robotics.

---

##  Publications

<!-- Uncomment and link the actual files if available -->
<!--
1. [Semester 7 Report](./)
2. [Semester 7 Slides](./)
3. [Semester 8 Report](./)
4. [Final Presentation Slides](./)
5. Janitha D., Asela H., Dulshan C., “Active Bionic Antennas for Object Detection and 3D Localization with Ego-Motion Cancellation”, (2025). [PDF](./)
-->

---

##  Links

- 🔬 [Project Repository](https://github.com/cepdnaclk/e19-4yp-Active-bionic-antennas-for-object-detection-and-3D-localization-with-ego-motion-cancellation)
- 🌐 [Project Web Page](https://cepdnaclk.github.io/e19-4yp-Active-bionic-antennas-for-object-detection-and-3D-localization-with-ego-motion-cancellation)
- 🏫 [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- 🎓 [University of Peradeniya](https://eng.pdn.ac.lk/)

---

##  Screenshots / Demo (Optional)

<!-- You can add here later:
![Antenna System](./images/antenna-setup.jpg)
![SLAM Map](./images/slam-map.png)
-->

---

