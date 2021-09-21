# Project3
프로그래머스 자율주행 데브코스 미션통과 프로젝트

## Video
---

[![차선인식 주행 영상](https://img.youtube.com/vi/BE9nrN8bJFQ/0.jpg)](https://youtu.be/BE9nrN8bJFQ) 

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
  │    └─ ar_main.py               # xycar drive main code
  │    └─ ar_approach2.py
  │    └─ ar_parking.py
  │    └─ ar_turnback.py
  │    └─ dqn_drive_end.py
  │    └─ dqn_test.py
  │    └─ lidar_driving_daeyoon.py
  │    └─ yolo_drive.py
  └─ launch
  │     └─ ar_config.launch
  │     └─ ar_config_daeyoon.launch
  │     └─ ar_config_inprogress.launch
  │     └─ ar_config_sum.launch
  │     └─ ar_config_test.launch
~~~

## Usage
---
~~~bash
$ roslaunch ar_project ar_config.launch
~~~

## Procedure
---
### ar tag recognize
![image](https://user-images.githubusercontent.com/65532515/134163007-f12ea62a-dd49-44d7-9e91-f18af40789e9.png)
- /ar_pose_marker 토픽의 id값을 받아와 ar태그를 구분.
### algorithm driving
![image](https://user-images.githubusercontent.com/65532515/134163670-e9dd7f05-1408-4cf2-9a9c-cc80d9a86574.png)
- 전방 180도의 라이다 값을 다섯 부분으로 나눠 오른쪽이 왼쪽보다 더 크면 우회전, 왼쪽이 오른쪽보다 더 크면 좌회전, 앞 라이다 거리가 0.3 보다 작아지면 후진 하도록 함.
- 코너마다 카운트를 세서 코너라고 인식했을 때는 앵글값과 속도값을 크게 줘서 구석으로 가지않고 빨리 빠져나가도록 함.
### ar tag approach & turnback
- ar태그 까지의 x좌표 차이, z좌표 차이를 이용하여 arctan(dx/dz) 각도만큼 조향각을 주어 ar tag까지 전진 후 앞에서 정지.
- 1.8초 동안 왼쪽으로 꺾어서 후진
- 0.3초 동안 전진
- 위 두 단계를 5번 반복하여 U-turn 하도록 알고리즘 작성.
### dqn
### yolo driving
- darknet_ros의 bounding_boxes토픽을 받아와서 인식한 이미지의 Class와 정답 Class가 일치하면 해당 이미지 방향의 각도를 계산한 후 이미지 쪽으로 주행.
- 각도는 화면의 중앙과 bounding_box 중앙의 차이에 50만큼 곱하여 구함.(xycar의 최대 angle 토픽값 = 50)
### parking

### steering control
1. 화면의 중심을 기준으로 왼쪽 좌표와 오른쪽 좌표의 중심과의 차이를 구해서 error 도출
2. 한쪽 좌표가 없어졌을 때를 코너로 인식
3. 직선과 코너에 다르게 PID 제어

## Try
---
1. PID Control
2. Moving Average Filter
3. 2-way Lane Detection

## Limitations
---
- 바닥에 비친 형광등, 기둥을 차선으로 인식하여 차선을 벗어나는 경우가 있었다. 
  - 카메라 노출도 조정과 한쪽 차선만 검출하여 해결
- PID 제어를 사용할 때 직선 구간에서 똑바로 가지 못함 
  - PID값을 조절하여 P = 0.25, I = 0.0005, D = 0.25 으로 설정했을 때 가장 안정적이었음.
- 하지만 위 PID 값을 적용했을 때, 곡선에서 차선 이탈을 하는 문제가 있었음 
  - 곡선과 직선에서의 PID값을 따로 주어 해결 -> 곡선 P = 0.5, I = 0.0, D = 0.25 로 설정. 
## What I've learned
---
- hough
- PID
- MovingAverageFilter
