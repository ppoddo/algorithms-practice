import sys
from collections import deque

# 미로에서 1은 이동할 수 있는 칸을 나타내고, 0은 이동할 수 없는 칸을 나타낸다.
# 이러한 미로가 주어졌을 때, (1, 1)에서 출발하여 (N, M)의 위치로 이동할 때 지나야 하는 최소의 칸 수를 구하는 프로그램을 작성하시오
# 한 칸에서 다른 칸으로 이동할 때, 서로 인접한 칸으로만 이동할 수 있다.
# 위의 예에서는 15칸을 지나야 (N, M)의 위치로 이동할 수 있다. 칸을 셀 때에는 시작 위치와 도착 위치도 포함한다.
# 첫째 줄에 두 정수 N, M(2 ≤ N, M ≤ 100)이 주어진다. 다음 N개의 줄에는 M개의 정수로 미로가 주어진다.
# 각각의 수들은 붙어서 입력으로 주어진다.

def main() -> None:
    input = sys.stdin.readline
    N, M = map(int, input().split())
    maze = [input().rstrip() for _ in range(N)]
    
    # 거리 저장
    distance = [[0] * M for _ in range(N)]

    # 상하좌우
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    searchQ = deque()
    searchQ.append((0, 0))
    distance[0][0] =1

    while searchQ:
        r, c = searchQ.popleft()

        for k in range(4):
            nr = r + dr[k]
            nc = c + dc[k]

            if 0 <= nr < N and 0 <= nc < M:
                if maze[nr][nc] == '1' and distance[nr][nc] == 0:
                    distance[nr][nc] = distance[r][c] + 1
                    searchQ.append((nr,nc))

    print (distance[N - 1][M - 1])
if __name__ == "__main__":
    main()
