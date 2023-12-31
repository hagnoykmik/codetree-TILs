from collections import deque

# 공격할 포탑과 공격대상 포탑 선정하기
def select():
    global sx, sy, goal_x, goal_y, end
    turret = []

    for x in range(N):
        for y in range(M):
            # 부서진 포탑이 아니라면 담기
            if board[x][y] != 0:
                # 공격력, 행, 열
                turret.append((board[x][y], x, y))

    if len(turret) == 1:
        end = True
        return

    turret.sort(key=lambda x: (x[0], -(x[1] + x[2]), -x[2]))

    attack_turret = turret[0]
    goal_turret = turret[-1]

    sx, sy = attack_turret[1], attack_turret[2]
    goal_x, goal_y = goal_turret[1], goal_turret[2]

    # 우선순위 두번째 최근에 공격한 포탑!
    for i in range(1, len(turret)):
        ax, ay = turret[i][1], turret[i][2]
        if turret[i][0] == attack_turret[0]:
            if attack_list[(sx, sy)] < attack_list[(ax, ay)]:
                sx, sy = ax, ay
        else:
            break

    # 우선순위 두번째 최근에 공격한 포탑!
    for j in range(len(turret) - 1, -1, -1):
        cx, cy = turret[j][1], turret[j][2]
        if turret[j][0] == goal_turret[0]:
            if attack_list[(cx, cy)] < attack_list[(goal_x, goal_y)]:
                goal_x, goal_y = cx, cy
        else:
            break


# 레이저공격
def attack(sx, sy):
    # 우, 하, 좌, 상
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    visited = [[0] * M for _ in range(N)]
    q = deque([(sx, sy, [])])
    visited[sx][sy] = 1

    while q:
        sx, sy, route = q.popleft()

        for d in range(4):
            nx = sx + dx[d]
            ny = sy + dy[d]

            # 범위 바꿔주기
            if 0 > nx or nx >= N or 0 > ny or ny >= M:
                nx = (nx + N) % N
                ny = (ny + M) % M

            # 부서진 포탑이 아니라면 지나갈 수 있다
            if board[nx][ny] != 0 and not visited[nx][ny]:
                # 공격 위치에 도달하면 멈춤
                if(nx, ny) == (goal_x, goal_y):
                    route.append((nx, ny))

                    return route
                new_route = route[:]
                new_route.append((nx, ny))
                q.append((nx, ny, new_route))
                visited[nx][ny] = 1

    return False


# 포탄던지기
def push():
    global is_push
    is_push = True # 포탄던지기로 한 것을 명시
    route = []

    # 8방향
    dx = [0, 1, 0, -1, -1, -1, 1, 1]
    dy = [1, 0, -1, 0, -1, 1, -1, 1]

    for d in range(8):
        nx = goal_x + dx[d]
        ny = goal_y + dy[d]

        # 범위 바꿔주기
        if 0 > nx or nx >= N or 0 > ny or ny >= M:
            nx = (nx + N) % N
            ny = (ny + M) % M

        # 부서진 포탑이 아니라면 지나갈 수 있다 + 자기자신도 부시면 안된다!(주의)
        if board[nx][ny] != 0 and (nx, ny) != (sx, sy):
            route.append((nx, ny))

    return route


# 포탑 부시기
def crush():
    # 포탄던지기면 다 해야함
    if is_push:
        for p in attacked_list:
            ax, ay = p[0], p[1]
            board[ax][ay] -= (score // 2)
            if board[ax][ay] < 0:
                board[ax][ay] = 0
    # 레이저면 경로 마지막거는 빼주기
    else:
        # 경로에 있는 포탑은 공격력의 반만 부서짐
        for p in attacked_list[:-1]:
            ax, ay = p[0], p[1]
            board[ax][ay] -= (score // 2)
            if board[ax][ay] < 0:
                board[ax][ay] = 0

    # 목표물은 공격력만큼 부서짐
    board[goal_x][goal_y] -= score
    if board[goal_x][goal_y] < 0:
        board[goal_x][goal_y] = 0


# 포탑 재정비
def repair():
    no_repair = set(attacked_list)
    no_repair.add((sx, sy))
    no_repair.add((goal_x, goal_y))

    for x in range(N):
        for y in range(M):
            if board[x][y] != 0 and (x, y) not in no_repair:
                board[x][y] += 1

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

turret = []
attack_list = {(n, m) : 0 for n in range(N) for m in range(M)} # 공격한 포탑 저장
result = 0

end = False # 만약 부서지지 않은 포탑이 1개가 된다면 그 즉시 중지됩니다.
for k in range(K):
    is_push = False

    sx, sy = -1, -1
    goal_x, goal_y = -1, -1

    # 맨 앞에 있는게 공격할 대상
    select()

    if end:
        break

    attack_list[(sx, sy)] = k + 1  # k번째에 공격함(숫자가 클수록 최신)
    board[sx][sy] += N + M  # 공격력 초기화
    score = board[sx][sy]

    # 공격
    attacked_list = attack(sx, sy)

    if not attacked_list:
        # 포탄 던지기
        attacked_list = push()

    # 포탑 부서짐
    crush()

    # 포탑 정비
    repair()


for line in board:
    point = max(line)
    if point > result:
        result = point

print(result)