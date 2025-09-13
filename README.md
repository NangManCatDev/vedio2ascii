# Video to ASCII (컬러 버전)

터미널에서 동영상을 **ASCII 아트**로 변환하여 재생하는 간단한 프로젝트
OpenCV와 ffmpeg을 활용하여 프레임을 추출하고, ANSI 24bit 색상 코드를 사용해 터미널에서 재생

---

## ✨ 기능
- **영상 → 프레임 변환** (ffmpeg 사용)
- **ASCII 아트 변환** (문자 + ANSI 색상코드)
- **터미널에서 실시간 재생** (FPS 지정 가능)
- 재생 후 `frames/` 폴더 자동 정리(옵션)
  - 최하단 코드의 주석을 해제하면 가능

---

## 실행 환경
- Python 3.8+
- OpenCV (`pip install opencv-python`)
- ffmpeg (시스템에 설치 필요)

---

## 사용 방법

1. 저장소 클론 및 이동
```bash
git clone https://github.com/username/video2ascii.git
cd video2ascii
```

2. 파이썬 의존성 설치
```bash
pip install opencv-python
```
3. ffmpeg 설치
```bash
sudo apt-get install ffmpeg
```
4. 실행
```bash
python run_color.py # 컬러버전
python run.py   # 흑백버전
```
- input.mp4 파일을 같은 폴더에 넣어두면 자동으로 변환
- 터미널 크기에 맞춰 영상이 조정

## 설정 변경
```python
video_file = "input.mp4"   # 변환할 영상 파일
frame_rate = 30            # 초당 프레임
chars = "@$B%8&WM#*..."    # ASCII 문자셋
```