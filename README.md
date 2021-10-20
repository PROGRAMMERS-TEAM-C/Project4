# Programmers Autonomous-Driving Dev course. Mission Pass Competition

## Video
---

[![차선인식 주행 영상](https://img.youtube.com/vi/tXYGs7sStSA/0.jpg)](https://youtu.be/tXYGs7sStSA) 

## Member Roles

| 이름         | 담당                                         |
| ------------ | :------------------------------------------- |
| 조영진(팀장) | DQN, YOLO, AR 태그 인식 기능 구현 |
| 구민상       | 라이다 인식 주행, 주차 기능, 모드 통합 구현 |
| 고세람       | 라이다 인식 주행, 주차 기능, 모드 통합 구현 |
| 임경묵       | DQN, YOLO, AR 태그 인식 기능 구현 |

## Goal
---
![image](https://user-images.githubusercontent.com/65532515/134160737-51b302eb-60bc-42e6-b3b6-248a266e1a76.png)  
1) AR 코드를 인식하여 우선 알고리즘 기반으로 충돌회피 주행 수행하기
2) 정지선 인식하면 정차. AR 코드 인식해서 방향 전환 수행하기 (반대 방향으로 주행 준비)
3) 정면에 AR 코드를 인식하여 머신러닝 기반으로 충돌회피 주행 수행하기
4) AR 코드를 인식하여 퀴즈 문제 입수하고 Yolo 기반 주행 수행하기
5) Yolo 이용해서 첫번째 정답 이미지 찾아서 그쪽 방향으로 주행하기
6) Yolo 이용해서 두번째 정답 이미지 찾아서 그쪽 방향으로 주행하기
7) AR 인식하여 50센치 떨어진 위치에 정차하기
8) AR 코드 인식하여 주차 시작하기 + 주차영역의 AR 인식하여 정해진 영역 안에 주차하기

## Environment
---
- Ubuntu 18.04
- ROS Melodic
- Xycar Model B
- Nvidia TX2

## Structure
---
~~~
Project3
  └─ src
  │    └─ ar_main.py                      # xycar drive main
  │    └─ ar_approach.py                  # AR 코드를 인식하여 50센치 떨어진 위치에 정차
  │    └─ ar_parking.py                   # AR 코드를 인식하여 주차
  │    └─ ar_turnback.py                  # AR 코드를 인식하여 주차 시작하기 전까지 주행
  │    └─ dqn_drive_end.py                # 학습(dqn) 주행한 drive 이후 Yolo 미션 시작 전까지 주행
  │    └─ dqn_test.py                     # 라이다 값으로 학습(dqn) 주행 (구현 실패)
  │    └─ lidar_driving.py                # 라이다 값으로 충돌회피 주행
  │    └─ yolo_drive.py                   # Yolo를 이용해서 정답 이미지 방향으로 주행
  └─ launch
  │    └─ ar_config.launch                # 전체 프로그램 launch
~~~

## Usage
---
~~~bash
$ roslaunch ar_project ar_config.launch
~~~

## Procedure
---
### AR Tag Recognize
![image](https://user-images.githubusercontent.com/65532515/134163007-f12ea62a-dd49-44d7-9e91-f18af40789e9.png)  
- /ar_pose_marker 토픽의 id값을 받아와 ar태그를 구분

### LiDAR Algorithm Driving
<img src="./img/lidar.png" Width="640" Height="320"/>

- 전방 180도의 라이다 값을 다섯 부분으로 나눠 오른쪽이 왼쪽보다 더 크면 우회전, 왼쪽이 오른쪽보다 더 크면 좌회전, 앞 라이다 거리가 0.3 보다 작아지면 후진 하도록 함.
- 코너마다 카운트를 세서 코너라고 인식했을 때는 앵글값과 속도값을 크게 줘서 구석으로 가지않고 빨리 빠져나가도록 함.

### AR Tag Approach & Turnback
- AR 태그까지의 x좌표 차이, z좌표 차이를 이용하여 arctan(dx/dz) 각도만큼 조향각을 주어 AR 태그까지 전진 후 앞에서 정지.
- 1.8초 동안 왼쪽으로 꺾어서 후진
- 0.3초 동안 전진
- 위 두 단계를 5번 반복하여 U-turn 하도록 알고리즘 작성.

### DQN Driving(구현 실패)
- 시뮬레이터에서 dqn 네트워크를 사용해서 학습시킨 .pth 값을 사용해서 주행

### YOLO Driving
<img src="./img/yolo.png" Width="640" Height="320"/>

- darknet_ros의 bounding_boxes토픽을 받아와서 인식한 이미지의 Class와 정답 Class가 일치하면 해당 이미지 방향의 각도를 계산한 후 이미지 쪽으로 주행.
- 각도는 화면의 중앙과 bounding_box 중앙의 차이에 50만큼 곱하여 구함.(xycar의 최대 angle 토픽값 = 50)

### AR Parking
<img src="./img/ar_parking.png" Width="640" Height="320"/>

- AR 태그가 보일 때까지 일정 거리동안 후진 및 전진
- AR 태그까지의 x좌표 차이, z좌표 차이를 이용하여 arctan(dx/dz) 각도만큼 조향각을 주어 AR 태그의 일정 거리 앞에서 정지

## Limitations
---
- LiDAR 센서의 위치가 정확하지 않음
  - 센서 테스트를 통해서 550개 값 중에서 정확한 0도(Index 90)의 지점 파악  
- LiDAR 센서의 noise가 다양함
  - LiDAR 센서에 들어오는 최대 길이를 지정해주고 0인 부분을 제외한 후, 계산  
- YOLO를 사용한 정답 찾기 미션에서 앞 미션의 정답과 뒤 미션의 정답이 동시에 보임
  - 두 개가 보일 때, Bounding box의 크기로 앞에 있는 미션을 판단한 후, 주행  
- DQN 학습을 진행할 때 시뮬레이터와 실제 환경이 다름
  
## What I've learned
---
- LiDAR 센서를 사용하기 전에는 센서 초기화와 센서의 정확한 판단이 중요
- LiDAR 센서를 사용할 때 들어오는 noise 처리 방법에 대해서 다양하게 생각해봄
