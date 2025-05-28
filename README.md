# Active Bionic Antennas for Object Detection and 3D Localization

![University of Peradeniya Logo](https://upload.wikimedia.org/wikipedia/en/3/32/University_of_Peradeniya_crest.png)

**Final Year Project – Department of Computer Engineering, University of Peradeniya**  
**Team Members:**  
- K. H. J. D. Premachandra (E/19/295)  
- L. M. A. H. Premawansha (E/19/300)  
- A. G. D. C. Thilkarathne (E/19/495)  

**Supervisors:**  
- Dr. Nalin Harischandra  
- Dr. Isuru Navinne  

---

## 📌 Project Overview

This project presents a **bio-inspired tactile sensing system** for robotic navigation in low-visibility environments. Inspired by insect antennae and mammalian whiskers, our system integrates:

- **Echo State Networks (ESNs)** for ego-motion cancellation.  
- **Multi-contact bionic antennas** for tactile object detection.  
- **Google Cartographer SLAM** adapted for tactile input.

The result is a robust 3D localization framework suitable for unstructured, cluttered, or visually degraded environments like disaster zones or underwater missions.

---

## 🚀 Key Features

- **Self-Sensing Cancellation**: Filters out motion-induced noise using ESNs and proprioceptive data.  
- **Tactile-Based SLAM**: Google Cartographer adapted to operate using tactile and IMU data instead of LiDAR.  
- **Real-Time Feedback**: Predicts and isolates external contacts from self-generated vibrations.  
- **Modular Design**: Separate models for offline training and online real-time inference.

---

## 🛠️ Hardware Platform

- 4WD Omni Wheel Robot Base  
- Jetson Nano (Main Processing Unit)  
- MPU6050 Accelerometers (x2)  
- MG90 Servo Motors (x4)  
- Poly-acrylic tubes (antenna support structure)  
- 12V Ni-MH Battery Pack  

---

## 📦 System Architecture

