import cv2
import os
import time
import sys
import shutil
import subprocess

# === 설정 ===
video_file = "input.mp4"    # 변환할 영상
frame_rate = 30             # 초당 프레임
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

# === 컬러 + ASCII 변환 함수 ===
def frame_to_ascii_color(image):
    # 터미널 크기 가져오기
    columns, rows = shutil.get_terminal_size(fallback=(120, 30))
    width = columns

    # BGR → RGB
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 원래 세로 비율 계산
    raw_height = int(rgb_img.shape[0] * width / rgb_img.shape[1] / 2)

    # 🔹 터미널 세로 크기에 맞게 강제 제한 (짤림 방지)
    height = min(raw_height, rows - 2)

    # 리사이즈
    rgb_img = cv2.resize(rgb_img, (width, height))

    # 문자 선택용 회색조
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)

    ascii_lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            r, g, b = rgb_img[y, x]
            pixel_int = int(gray_img[y, x])
            char = chars[pixel_int * len(chars) // 256]
            # ANSI 24bit 색상코드
            line += f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m"
        ascii_lines.append(line)
    return "\n".join(ascii_lines)

# === 프레임 재생 ===
files = sorted(os.listdir("frames"))
try:
    for f in files:
        img = cv2.imread(os.path.join("frames", f))  # 컬러로 읽기
        ascii_frame = frame_to_ascii_color(img)
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
