---
source: pora
tags: [pora, robot-autonomy, course]
---

# Principles of Robot Autonomy

Free textbook by Daniele Gammelli, Joseph Lorenzetti, Katie Luo, Gioele Zardini, and Marco Pavone (Cambridge University Press, 2026). Read it at https://porabook.com/book/; exercises at https://github.com/StanfordASL/pora-exercises.

Unofficial companion map. Concept summaries and prerequisite links are written independently and are not part of the book. The book is the authoritative reference.

## Course resources

- [Textbook](https://porabook.com/book/): Read free online, chapter by chapter
- [Video lectures](https://porabook.com/lectures/): AA174A and AA203 recordings
- [Interactive exercises](https://porabook.com/exercises/): Python and Jupyter notebooks
- [Teaching materials](https://porabook.com/instructors/): Slides and resources for instructors
- [Ask the Book](https://porabook.com/): AI study assistant inside the textbook

## Getting started
- [Robot Autonomy Software](https://porabook.com/book/software/): [[Autonomy_software_stack]]

## Part I · Motion planning and control
- [Modeling Robot Dynamics](https://porabook.com/book/modeling-robot-dynamics/): [[State_space_model]], [[Kinematic_vs_dynamic_models]], [[Nonholonomic_wheeled_robots]], [[Numerical_integration_and_simulation]]
- [Open-Loop Control & Trajectory Optimization](https://porabook.com/book/open-loop-control/): [[Optimal_control_problems]], [[Indirect_methods_and_Pontryagin]], [[Direct_methods_and_transcription]], [[Differential_flatness]]
- [Closed-Loop Control & Trajectory Tracking](https://porabook.com/book/closed-loop-control/): [[PID_control]], [[Linearization]], [[LQR]], [[Trajectory_tracking]], [[ILQR_and_DDP]], [[Model_predictive_control]]
- [Motion Planning](https://porabook.com/book/motion-planning/): [[Configuration_space]], [[Graph_search_and_A-star]], [[Sampling-based_planning_PRM_RRT]], [[Potential_field_methods]], [[Planning_with_dynamics]]

## Part II · Perception
- [Introduction to Robot Sensors](https://porabook.com/book/robot-sensors/): [[Robot_sensors]], [[Measurement_noise_models]]
- [Camera Models and Calibration](https://porabook.com/book/camera-models/): [[Pinhole_camera_model]], [[Intrinsics_extrinsics_and_calibration]]
- [Stereo Vision and Structure From Motion](https://porabook.com/book/stereo-vision/): [[Epipolar_geometry]], [[Stereo_depth_and_triangulation]], [[Structure_from_motion]], [[Visual_odometry_and_loop_closure]]
- [Classical Methods for Perception](https://porabook.com/book/classical-perception/): [[Feature_detection_and_matching]], [[Image_filtering_and_convolution]], [[Point_cloud_registration_ICP]], [[Classical_visual_recognition]]
- [Deep Learning Architectures for Perception](https://porabook.com/book/deep-learning-perception/): [[Convolutional_neural_networks]], [[Attention_and_vision_transformers]], [[Point_cloud_and_voxel_networks]]
- [Object Detection and Recognition](https://porabook.com/book/object-detection/): [[Object_detection_and_recognition]], [[3D_object_detection]], [[Semantic_and_instance_segmentation]]

## Part III · Localization and mapping
- [Introduction to Localization and Filtering](https://porabook.com/book/localization-filtering/): [[Probability]], [[Recursive_Bayes_filter]], [[Discrete_histogram_filter]]
- [Approximate Filters for State Estimation](https://porabook.com/book/approximate-filters/): [[Kalman_filter]], [[EKF_and_UKF]], [[Particle_filter]]
- [Robot Localization](https://porabook.com/book/robot-localization/): [[Probabilistic_motion_and_sensor_models]], [[EKF_localization]], [[Monte_Carlo_localization]]
- [Simultaneous Localization and Mapping (SLAM)](https://porabook.com/book/slam/): [[EKF_SLAM]], [[SLAM_front_end]], [[Graph_and_factor-graph_SLAM]]
- [Sensor Fusion and Object Tracking](https://porabook.com/book/sensor-fusion/): [[Sensor_fusion]], [[Object_tracking_and_data_association]], [[Learned_fusion_BEV_and_features]]

## Part IV · Decision making
- [Finite State Machines](https://porabook.com/book/finite-state-machines/): [[Finite_state_machines]]
- [Sequential Decision Making and Dynamic Programming](https://porabook.com/book/decision-making/): [[Markov_decision_processes]], [[dynamic_programming]]
- [Reinforcement Learning](https://porabook.com/book/reinforcement-learning/): [[Value_and_policy_iteration]], [[reinforcement_learning]], [[Monte_Carlo_and_TD_learning]], [[Value-based_RL_Q-learning]], [[Policy_gradients_and_actor-critic]], [[Model-based_RL_and_system_ID]]
- [Imitation Learning](https://porabook.com/book/imitation-learning/): [[Behavior_cloning]], [[Covariate_shift]], [[Inverse_reinforcement_learning]]

## Assumed background
[[Linear_algebra]], [[Ordinary_differential_equation]], [[Numerical_optimization]], [[Neural_network]]
