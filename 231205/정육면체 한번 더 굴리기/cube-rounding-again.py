from collections import deque

def move_dice(d):
    ndice = [0] * 6

    # 동쪽
    if d == 0:
        ndice[0] = dice[0]
        ndice[1] = dice[4]
        ndice[2] = dice[2]
        ndice[3] = dice[5]
        ndice[4] = dice[3]
        ndice[5] = dice[1]
    # 북쪽
    elif d == 1:
        ndice[0] = dice[3]
        ndice[1] = dice[0]
        ndice[2] = dice[1]
        ndice[3] = dice[2]
        ndice[4] = dice[4]
        ndice[5] = dice[5]
    # 서쪽
    elif d == 2:
        ndice[0] = dice[0]
        ndice[1] = dice[5]
        ndice[2] = dice[2]
        ndice[3] = dice[4]
        ndice[4] = dice[1]
        ndice[5] = dice[3]
    # 남쪽
    else:
        ndice[0] = dice[3]
        ndice[1] = dice[0]
        ndice[2] = dice[1]
        ndice[3] = dice[2]
        ndice[4] = dice[4]
        ndice[5] = dice[5]

    # 원래 주사위에 복사
    for i in range(6):
        dice[i] = ndice[i]


def cal_point(x, y):
    visited = [[0] * n for _ in range(n)]
    number = board[x][y]
    cnt = 1
    q = deque([(x, y)])
    visited[x][y] = 1

    while q:
        x, y = q.popleft()

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and board[nx][ny] == number:
                q.append((nx, ny))
                cnt += 1
                visited[nx][ny] = 1

    point = cnt * number
    return point




n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
dice = [5, 1, 2, 6, 4, 3] # 초기 상태
point = 0
# 시계방향
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
d = 0
sx, sy = 0, 0


# 주사위 m 번 굴리기
for _ in range(m):
    # 주사위 굴리기
    move_dice(d)
    
    # 칸 이동
    nx = sx + dx[d]
    ny = sy + dy[d]

    # 범위 벗어나면 반대 방향
    if nx < 0 or nx >= n or ny < 0 or ny >= n:
        d = (d + 2) % 4
        continue

    # 점수 계산 하기
    cur_point = cal_point(nx, ny)
    point += cur_point

    # 주사위 > 칸 -> 시계방향
    if board[nx][ny] < dice[3]:
        d = (d + 1) % 4
    # 주사위 < 칸 -> 반시계방향
    elif board[nx][ny] > dice[3]:
        d = (d + 3) % 4

    # 주사위 위치 바꿔주기
    sx, sy = nx, ny

print(point)