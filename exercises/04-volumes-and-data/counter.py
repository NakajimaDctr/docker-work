import os

DATA_DIR = "/data"
COUNT_FILE = os.path.join(DATA_DIR, "count.txt")

os.makedirs(DATA_DIR, exist_ok=True)

if os.path.exists(COUNT_FILE):
    with open(COUNT_FILE, "r") as f:
        count = int(f.read().strip())
else:
    count = 0

count += 1

with open(COUNT_FILE, "w") as f:
    f.write(str(count))

print(f"このコンテナは {count} 回目の起動です。")
