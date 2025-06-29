# Modified from [Catch It! Learning to Catch in Flight with Mobile Dexterous Hands](https://mobile-dex-catch.github.io/)

# Installation
- Create conda environment and install pytorch:
```
conda create -n dcmm python=3.8
conda activate dcmm
pip install torch torchvision torchaudio
```
- Clone this repo and install our `gym_dcmm`:
```
git clone https://github.com/hang0610/catch_it.git
cd catch_it && pip install -e .
```
- Install additional packages in `requirements.txt`:
```
pip install -r requirements.txt
```

<!-- # Space Definition
## Observation Space (dim=30)
- base (dim=2): Dict
  - v_lin: 2d linear velocities
- arm (dim=10): Dict
  - ee_pos3d: 3d position of the end-effector
  - ee_v_lin_3d: 3d linear veloity of the end-effector
  - ee_quat: quaternion of the end-effector
- hand (dim=12): 12 joint positions of the hand
- object (dim=6): Dict
  - pos3d: 3d position of the object
  - v_lin_3d: 3d linear velocity of the object
## Actions Space (dim=18)
- base (dim=2): 2d linear velocities of the mobile base
- arm (dim=4): delta x-y-z and delta roll of the arm
- hand (dim=12): 12 delta joint positions of the hand -->

# Simulation Environment Test

## Global Setting

In `configs/config.yaml`:: set 
  ```yaml
  global_task: Bounce
  ```
for the bounce, or
  ```yaml
  global_task: Original
  ```
for the original.

## Keyboard Control Test

Under `gym_dcmm/envs/`, run:
```bash
python3 DcmmVecEnv.py --viewer --imshow_cam
```

Keyboard control:

1. `→` (262) : increase the y linear velocity (base frame) by 0.2 m/s;
2. `←` (263) : decrease the y linear velocity (base frame) by 0.2 m/s;
3. `↓` (264) : increase x linear velocity (base frame) by 0.2 m/s;
4. `↑` (265) : decrease x linear velocity (base frame) by 0.2 m/s;
5. `0` (320) : decrease counter-clockwise angular velocity by 0.5 rad/s;
6. `.` (330) : increase counter-clockwise angular velocity by 0.5 rad/s;
7. `8` (328): increase the position of the arm end effector by (-0.1, 0.0, 0.0) m;
8. `2` (322): decrease the position of the arm end effector by (0.1, 0.0, 0.0) m;
9. `4` (324): increase the position of the arm end effector by (0.0, -0.1, 0.0) m;
10. `6` (326): decrease the position of the arm end effector by (0.0, 0.1, 0.0) m;
9. `-` (333): increase the position of the arm end effector by (0.0, 0.0, 0.2) m;
10. `+` (334): decrease the position of the arm end effector by (0.0, 0.0, -0.2) m;
11. `7` (327): increase the joint position of the hand by (0.2, 0.2, 0.2, 0.2) rad;
12. `9` (329): decrease the joint position of the hand by (0.2, 0.2, 0.2, 0.2) rad;

# Simulation Training/Testing
<div style="display: flex; align-items: center;">
    <img src="./assets/media/videos/train.gif" alt="train" style="margin-right: 10px;">
</div>

## Training/Testing Settings

1. `configs/config.yaml`: 

    ```yaml
    # Disables viewer or camera visualization
    viewer: False
    imshow_cam: False
    # RL Arguments
    test: False # False, True
    global_task: Bounce # Bounce or Original
    task: Tracking # Catching_TwoStage, Catching_OneStage, Tracking
    num_envs: 32 # This should be no more than 2x your CPUs (1x is recommended)
    object_eval: False
    # used to set checkpoint path
    checkpoint_tracking: ''
    checkpoint_catching: ''
    # checkpoint_tracking: 'assets/models/track.pth'
    # checkpoint_catching: 'assets/models/catch_two_stage.pth'
    ```
    * `num_envs (int)`: the number of paralleled environments;
    * `task (str)`: task type (Tracking or Catching);
    * `test (bool)`: Setting to True enables testing mode, while setting to False enables training mode;
    * `checkpoint_tracking/catching (str)`: Load the pre-trained model for training/testing;
    * `viewer (bool)`: Launch the Mujoco viewer or not;
    * `imshow_cam (bool)`: Visualize the camera scene or not;
    * `object_eval (bool)`: Use the unseen objects or not;
2. `configs/train/DcmmPPO.yaml`:
    * `minibatch_size`: The batch size for network input during PPO training;
    * `horizon_length`: The number of steps collected in a single trajectory during exploration;

    **Note**: In the training mode, must satisfy: `num_envs` * `horizon_length` = n * `minibatch_size`, where n is a positive integer.

## Testing
We provide our tracking model and catching model trained in a two-stage manner, which are `assets/models/track.pth` and `assets/models/catch_two_stage.pth`. You can test them for the tracking and catching task. Also, You can choose to evaluate on the training objects or the unseen objects by setting `object_eval`.

### Testing on the Tracking Task

Under the root `catch_it`: run either
```bash
python3 train_DCMM.py test=True task=Tracking num_envs=1 checkpoint_tracking="/home/yifan/Robotics/BaseKeeper/assets/models/track.pth" object_eval=False viewer=True imshow_cam=True
python3 train_DCMM.py test=True task=Tracking num_envs=1 checkpoint_tracking="/home/yifan/Robotics/BaseKeeper/assets/models/track.pth" object_eval=True viewer=True imshow_cam=True
```
### Testing on the Catching Task

Under the root `catch_it`: run either
```bash
python3 train_DCMM.py test=True task=Catching_TwoStage num_envs=1 checkpoint_catching="/home/yifan/Robotics/BaseKeeper/assets/models/catch_two_stage.pth" object_eval=False viewer=True imshow_cam=True
python3 train_DCMM.py test=True task=Catching_TwoStage num_envs=1 checkpoint_catching="/home/yifan/Robotics/BaseKeeper/assets/models/catch_two_stage.pth" object_eval=True viewer=True imshow_cam=True
```

## Two-Stage Training From Scratch
**Reminder**: 
Please check these three parameters again `num_envs * horizon_length = n * minibatch_size`, where `n` is a positive integer. 
### Stage 1: Tracking Task
Under the root `catch_it`, train the base and arm to **track** the randomly thrown objects:
```bash
python3 train_DCMM.py test=False task=Tracking num_envs=$(number_of_CPUs)
```

### Stage 2: Catching Task
* Firts, load the tracking model from stage 1, and fill its path to the `checkpoint_tracking` in `configs/config.yaml`.

  We provide our tracking model, which is `assets/models/track.pth`, which can be used to train the catching task (stage 2) directly.

* Second, train the whole body (the base, arm and hand) to **catch** the randomly thrown objects:
  ```bash
  python3 train_DCMM.py test=False task=Catching_TwoStage num_envs=$(number_of_CPUs) checkpoint_tracking=$(path_to_tracking_model)
  ``` 

## One-Stage Training From Scratch
In the one-stage training baseline, we don't pre-train a tracking model but directly train a catching model from scratch. Similar to the setting of training tracking model, run:
```bash
python3 train_DCMM.py test=False task=Catching_OneStage num_envs=$(number_of_CPUs)
```
## Logger
You can visualize the training curves and metrics via `wandb`. In `configs/config.yaml`:
```yaml
# wandb config
output_name: Dcmm
wandb_mode: "disabled"  # "online" | "offline" | "disabled"
wandb_entity: 'Your_username'
# wandb_project: 'RL_Dcmm_Track_Random'
wandb_project: 'RL_Dcmm_Catch_Random'
```

# Real-Robot Deployment
## System Overview
<div style="display: flex; align-items: center;">
    <img src="./assets/media/imgs/real_robot.png" alt="real_robot" style="margin-right: 10px;">
</div>
<br>


* Mobile Base: [Ranger Mini V2](https://global.agilex.ai/products/ranger-mini)
* Arm: [XArm6](https://www.ufactory.cc/xarm-collaborative-robot/)
* Dexterous Hand: [LEAP Hand](https://leaphand.com/)
* Perception: [Realsense D455](https://www.intelrealsense.com/depth-camera-d455/)
* Onboard Computer: [Thunderobot MIX MiniPC](https://www.amazon.com/WEELIAO-ThundeRobot-Desktop-i7-13620H-Bluetooth/dp/B0CZ91ZVK3)

## Deployment Code
Our code is build upon Ubuntu 20.04, ROS Noetic. Lower or higher version may also work (not guaranteed).
* Ranger Mini V2: [ranger_ros](https://github.com/agilexrobotics/ranger_ros)
* XArm6: [xarm-ros](https://github.com/xArm-Developer/xarm_ros)
* LEAP Hand: [LEAP Hand ROS1 SDK](https://github.com/leap-hand/LEAP_Hand_API/tree/main/ros_module)
* Realsense D455: [realsense-ros](https://github.com/IntelRealSense/realsense-ros) and [realsense-sdk](https://github.com/IntelRealSense/librealsense)
* Camera Calibration: [easy_handeye](https://github.com/IFL-CAMP/easy_handeye)

# Trouble Shooting
## Contact
Yuanhang Zhang: yuanhanz@andrew.cmu.edu

## Issues
You can create an issue if you meet any other bugs.

* If some mujoco rendering errors happen `mujoco.FatalError: gladLoadGL error`, try adding the following line before `main()` in the `train_DCMM.py` and `gym_dcmm/envs/DcmmVecEnv.py`:
  ```python
  os.environ['MUJOCO_GL'] = 'egl'
  ```


# Citation

Please consider citing our paper if you find this repo useful:
```bibtex
@article{zhang2024catchitlearningcatch,
  title={Catch It! Learning to Catch in Flight with Mobile Dexterous Hands},
  author={Zhang, Yuanhang and Liang, Tianhai and Chen, Zhenyang and Ze, Yanjie and Xu, Huazhe},
  year={2024},
  journal={arXiv preprint arXiv:2409.10319}
}
```
# LICENSE
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
