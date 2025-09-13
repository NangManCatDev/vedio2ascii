import cv2
import os
import time
import sys
import shutil
import subprocess

# === 설정 ===
video_file = "input.mp4"    # 변환할 영상
frame_rate = 30             # 초당 프레임
# width는 터미널 크기에 따라 자동으로 설정됨

# 더 디테일한 문자 집합
chars = "@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# === ffmpeg으로 프레임 추출 ===
if not os.path.exists("frames"):
    os.makedirs("frames")
else:
    for f in os.listdir("frames"):
        os.remove(os.path.join("frames", f))

subprocess.run([
    "ffmpeg", "-i", video_file,
    "-vf", f"fps={frame_rate}",
    "frames/frame_%04d.png"
])

# === ASCII 변환 함수 ===
def frame_to_ascii(image):
    # 터미널 너비 자동 설정
    columns, rows = shutil.get_terminal_size(fallback=(120, 30))
    width = columns  # 터미널 가로 칸 수

    if len(image.shape) == 2:
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 세로 비율 조정(1.2로 변경)
    height = int(gray.shape[0] * width / gray.shape[1] / 1.2)
    gray = cv2.resize(gray, (width, height))

    ascii_str = ""
    for row in gray:
        for pixel in row:
            pixel_int = int(pixel)
            ascii_str += chars[pixel_int * len(chars) // 256]
        ascii_str += "\n"
    return ascii_str


# === 프레임 재생 ===
files = sorted(os.listdir("frames"))
try:
    for f in files:
        img = cv2.imread(os.path.join("frames", f), cv2.IMREAD_GRAYSCALE)
        ascii_frame = frame_to_ascii(img)
        # 터미널 지우기
        if sys.platform.startswith('win'):
            os.system('cls')
        else:
            os.system('clear')
        print(ascii_frame)
        time.sleep(1/frame_rate)
except KeyboardInterrupt:
    print("중단됨")

# === 끝나면 frames 폴더 삭제 (선택사항) ===
# shutil.rmtree("frames")
