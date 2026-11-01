
import subprocess
import cv2
import time

ADB = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
REMOTE = "/sdcard/screen.png"
LOCAL = "screen.png"

print("Live capture started. Press Q to quit.")

# Create the first screenshot inside BlueStacks
subprocess.run(
    [ADB, "shell", "screencap", "-p", REMOTE],
    check=True
)

while True:
    result = subprocess.run(
        [ADB, "pull", REMOTE, LOCAL],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Pull failed:", result.stderr)
        break

    frame = cv2.imread(LOCAL)

    if frame is None:
        print("Could not read screenshot.")
        break

    cv2.imshow("Live Shadow Fight 4 Screen", frame)

    # Capture a fresh screenshot for the next iteration
    subprocess.run(
        [ADB, "shell", "screencap", "-p", REMOTE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    time.sleep(0.2)

cv2.destroyAllWindows()
