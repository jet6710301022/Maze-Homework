import os
import time
from colorama import Fore, Style, init

init(autoreset=True)  # ทำให้สีรีเซ็ตอัตโนมัติหลังจากใช้

# ฟังก์ชันแสดงเขาวงกต
def display_maze(maze, player_pos):
    os.system('cls' if os.name == 'nt' else 'clear')  # เคลียร์หน้าจอ
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if (i, j) == player_pos:
                print(Fore.YELLOW + "0", end=" ")  # แสดงตำแหน่งผู้เล่นเป็นสีเหลือง
            else:
                print(col, end=" ")
        print("")
    print("")

# ฟังก์ชันค้นหาเส้นทางด้วย DFS
def find_path(maze, start, end):
    stack = [start]  # ใช้ stack ในการเก็บเส้นทาง
    visited = set()  # เก็บตำแหน่งที่เคยเยี่ยมชม
    parent = {}  # เก็บตำแหน่งก่อนหน้าเพื่อสร้างเส้นทางย้อนกลับ

    while stack:
        current = stack.pop()  # นำตำแหน่งปัจจุบันออกจาก stack
        if current == end:  # หากถึงจุดหมายแล้ว
            path = []
            while current:  # ย้อนกลับจากจุดหมายไปยังจุดเริ่มต้น
                path.append(current)
                current = parent.get(current)
            return path[::-1]  # กลับทิศทางเส้นทาง

        visited.add(current)
        x, y = current
        # ตรวจสอบทิศทางที่สามารถไปได้ (ขึ้น, ลง, ซ้าย, ขวา)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (x + dx, y + dy)
            if (
                0 <= next_pos[0] < len(maze) and  # อยู่ในเขตเขาวงกต
                0 <= next_pos[1] < len(maze[0]) and
                maze[next_pos[0]][next_pos[1]] == " " and  # เป็นทางเดิน
                next_pos not in visited  # ยังไม่เยี่ยมชม
            ):
                stack.append(next_pos)
                parent[next_pos] = current  # บันทึกตำแหน่งก่อนหน้า

    return None  # หากไม่มีเส้นทาง

# เขาวงกต
maze = [
    ["I", "I", "I", "I", "I", "I", "I"],
    ["I", " ", " ", "I", " ", " ", "I"],
    ["I", "I", " ", "I", " ", "I", "I"],
    ["I", " ", " ", " ", " ", " ", "I"],
    ["I", "I", "I", "I", "I", " ", "I"],
    ["I", " ", " ", " ", "I", " ", "I"],
    ["I", "I", "I", "I", "I", " ", "I"],
]

# ตำแหน่งเริ่มต้นและสิ้นสุด
start = (1, 1)
end = (5, 5)

# ค้นหาเส้นทาง
path = find_path(maze, start, end)

# แสดงผลการเดินอัตโนมัติ + บันทึกสถิติ
if path:
    input(Fore.CYAN + "กด Enter เพื่อเริ่มเดินทางอัตโนมัติ...")  # กดแค่ครั้งเดียว
    
    step_count = len(path) - 1  # นับจำนวนก้าวที่เดิน (ไม่นับจุดเริ่มต้น)
    start_time = time.time()  # เวลาที่เริ่มเดิน
    
    for pos in path:
        display_maze(maze, pos)  # แสดงตำแหน่งปัจจุบัน
        time.sleep(0.5)  # หน่วงเวลาให้เห็นการเดิน
    
    end_time = time.time()  # เวลาที่เดินถึงจุดหมาย
    elapsed_time = round(end_time - start_time, 2)  # คำนวณเวลาใช้จริง (วินาที)

    # เอฟเฟกต์พิเศษเมื่อถึงเส้นชัย
    print(Fore.GREEN + Style.BRIGHT + "🎉 คุณชนะ! เดินทางถึงจุดหมายแล้ว 🎉")
    print(Fore.MAGENTA + f"🚀 จำนวนก้าวที่ใช้: {step_count} ก้าว")
    print(Fore.BLUE + f"⏳ เวลาเดินทาง: {elapsed_time} วินาที")
    
    # บันทึกลงไฟล์
    with open("maze_stats.txt", "a", encoding="utf-8") as file:
        file.write(f"จำนวนก้าว: {step_count}, เวลา: {elapsed_time} วินาที\n")
        print(Fore.YELLOW + "✅ บันทึกสถิติการเดินทางลงไฟล์ maze_stats.txt แล้ว!")

else:
    print(Fore.RED + "ไม่พบเส้นทางไปยังจุดหมาย!")
