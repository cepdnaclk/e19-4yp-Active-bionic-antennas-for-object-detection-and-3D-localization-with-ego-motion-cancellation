# Active Bionic Antennas for Object Detection and 3D Localization

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

This project presents a bio-inspired tactile sensing system for robotic navigation in low-visibility environments. Inspired by insect antennae and mammalian whiskers, our system integrates:

- Echo State Networks (ESNs) for ego-motion cancellation  
- Multi-contact bionic antennas for tactile object detection  

The result is a robust 3D localization framework suitable for unstructured, cluttered, or visually degraded environments such as disaster zones, underwater habitats, or extraterrestrial exploration.

---

## 🚀 Key Features

- 🧠 Self-sensing cancellation using ESNs   
- 🤖 Real-time contact detection with motion filtering  
- 🧩 Modular offline and online processing models  

---

## 🛠️ Hardware Components

- 4WD robot platform  
- Jetson Nano (Main Processing Unit)  
- MPU6050 Accelerometers (x2)  
- MG90 Servo Motors (x2)  
- Poly-acrylic tubes (antenna support)  
- 12V Ni-MH Battery Pack
- Arduino Uno with Motor controller  
  

---

## ⚙️ System Architecture

```
+---------------------------+
|       Jetson Nano        |
| +---------------------+  |
| | Echo State Network  |  |
| |  - Predict motion    | |
| |  - Filter contact    | |
| +---------------------+  |
+---------------------------+
        ↑         ↑
  Antenna IMU   Servo Cmds
```

---

## 🧪 Methodology

1. **Data Collection**: Acceleration & servo data at 130 Hz  
2. **Offline ESN Training**: Model self-induced antenna motion  
3. **Online Filtering**: Real-time ego-motion cancellation  
 

---

## 🔬 Data Processing

- FFT: Analyze vibration signatures  
- Band-pass Filtering: Eliminate high-frequency noise  

---



## 📚 References

1. [Insect-Inspired Tactile Sampling - Hoinville et al. (2014)](https://doi.org/10.1007/978-3-319-09435-9_11)  
2. [CPG-Driven Antenna Motion - Harischandra et al. (2015)](https://doi.org/10.3389/fncom.2015.00107)  
3. [Forward Models with ESNs - Harischandra & Dürr (2012)](https://doi.org/10.1109/rose.2012.6402605)  

---

## 🧠 Outcomes & Impact

- ✅ Significantly reduces false positives from ego-motion  
- 🧭 Enables navigation in dark, dusty, or occluded areas  
- 🔁 Real-time external contact detection  
- 🌍 Potential for application in rescue robotics, planetary rovers, underwater drones  

---

## 📁 Repository Structure

```
📦 tactile-bionic-antennas/
├── data/               # Raw sensor data
├── models/             # ESN training scripts and configs
├── slam/               # Google Cartographer configs
├── hardware/           # Antenna CAD, schematics
├── README.md           # Project overview
└── requirements.txt    # Python/ROS dependencies
```

---

## 🔮 Future Work

- Integrate reinforcement learning for adaptive path planning  
- Expand beyond vibration to include auditory/visual cancellation  
- Outdoor trials with GPS-denied navigation  

---

## 🙏 Acknowledgments

Special thanks to the Department of Computer Engineering, University of Peradeniya, and our supervisors for their support and guidance.

---

## 📬 Contact

For queries, collaborations, or project discussions, feel free to open an issue or reach out via email.
