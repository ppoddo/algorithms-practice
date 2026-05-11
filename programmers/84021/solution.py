from collections import deque

# 테이블 위에 놓인 퍼즐 조각을 게임 보드의 빈 공간에 적절히 올려놓으려 합니다.
# 게임 보드와 테이블은 모두 각 칸이 1x1 크기인 정사각 격자 모양입니다.
# 이때, 다음 규칙에 따라 테이블 위에 놓인 퍼즐 조각을 게임 보드의 빈칸에 채우면 됩니다.

# 조각은 한 번에 하나씩 채워 넣습니다.
# 조각을 회전시킬 수 있습니다.
# 조각을 뒤집을 수는 없습니다.
# 게임 보드에 새로 채워 넣은 퍼즐 조각과 인접한 칸이 비어있으면 안 됩니다.

# 위 그림에서 왼쪽은 현재 게임 보드의 상태를, 오른쪽은 테이블 위에 놓인 퍼즐 조각들을 나타냅니다.
# 테이블 위에 놓인 퍼즐 조각들 또한 마찬가지로 [상,하,좌,우]로 인접해 붙어있는 경우는 없으며,
# 흰 칸은 퍼즐이 놓이지 않은 빈 공간을 나타냅니다. 모든 퍼즐 조각은 격자 칸에 딱 맞게 놓여있으며,
# 격자 칸을 벗어나거나, 걸쳐 있는 등 잘못 놓인 경우는 없습니다.

# 이때, 아래 그림과 같이 3,4,5번 조각을 격자 칸에 놓으면 규칙에 어긋나므로 불가능한 경우입니다.

# 3번 조각을 놓고 4번 조각을 놓기 전에 위쪽으로 인접한 칸에 빈칸이 생깁니다.
# 5번 조각의 양 옆으로 인접한 칸에 빈칸이 생깁니다.
# 다음은 규칙에 맞게 최대한 많은 조각을 게임 보드에 채워 넣은 모습입니다

# 최대한 많은 조각을 채워 넣으면 총 14칸을 채울 수 있습니다.

# 현재 게임 보드의 상태 game_board, 테이블 위에 놓인 퍼즐 조각의 상태 table이 매개변수로 주어집니다.
# 규칙에 맞게 최대한 많은 퍼즐 조각을 채워 넣을 경우,
# 총 몇 칸을 채울 수 있는지 return 하도록 solution 함수를 완성해주세요.

# 3 ≤ game_board의 행 길이 ≤ 50
# game_board의 각 열 길이 = game_board의 행 길이
# 즉, 게임 보드는 정사각 격자 모양입니다.
# game_board의 모든 원소는 0 또는 1입니다.
# 0은 빈칸, 1은 이미 채워진 칸을 나타냅니다.
# 퍼즐 조각이 놓일 빈칸은 1 x 1 크기 정사각형이 최소 1개에서 최대 6개까지 연결된 형태로만 주어집니다.
# table의 행 길이 = game_board의 행 길이
# table의 각 열 길이 = table의 행 길이
# 즉, 테이블은 game_board와 같은 크기의 정사각 격자 모양입니다.
# table의 모든 원소는 0 또는 1입니다.
# 0은 빈칸, 1은 조각이 놓인 칸을 나타냅니다.
# 퍼즐 조각은 1 x 1 크기 정사각형이 최소 1개에서 최대 6개까지 연결된 형태로만 주어집니다.
# game_board에는 반드시 하나 이상의 빈칸이 있습니다.
# table에는 반드시 하나 이상의 블록이 놓여 있습니다.

def solution(game_board, table):
    n = len(game_board) # 격자는 n * n

    # 상, 하, 좌, 우
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 좌표로 구성된 블록을 다른 블록과 모양만을 쉽게 비교할 수 있도록 좌표의 위치정보를 제거하는 함수
    def normalize(block):
        min_x = min(x for x, y in block)
        min_y = min(y for x, y in block)

        normalized = []

        for x, y in block:
            normalized.append((x - min_x, y - min_y))

        normalized.sort()
        return normalized

    # 보드에서 블록 덩어리 찾기
    def bfs(board, target):
        visited = [[False] * n for _ in range(n)]
        blocks = []

        # 보드 n * n 좌표 탐색해서 타겟에 해당하는 좌표면 거기서 부터 덩어리 찾아내기
        for i in range(n):
            for j in range(n):
                if board[i][j] == target and not visited[i][j]:
                    queue = deque()
                    queue.append((i, j))
                    visited[i][j] = True

                    block = []

                    while queue:
                        x, y = queue.popleft()
                        block.append((x, y))

                        for dx, dy in directions:
                            nx = x + dx
                            ny = y + dy

                            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if board[nx][ny] != target:
                                continue

                            visited[nx][ny] = True
                            queue.append((nx, ny))

                    # 완성된 블록을 정규화해서 넣기
                    blocks.append(normalize(block))

        return blocks

    # 블록 90도 회전
    def rotate(block):
        rotated = []

        for x, y in block:
            rotated.append((y, -x))

        #회전 후에는 음수 좌표가 생길 수 있으므로 다시 normalize 필요
        return normalize(rotated)

    # 시작
    empty_spaces = bfs(game_board, 0)
    puzzle_pieces = bfs(table, 1)

    used = [False] * len(puzzle_pieces)
    answer = 0

    for space in empty_spaces:
        for i in range(len(puzzle_pieces)):
            if used[i]:
                continue

            piece = puzzle_pieces[i]

            # 칸 수가 다르면 절대 들어갈 수 없음
            if len(space) != len(piece):
                continue

            current_piece = piece

            for _ in range(4):
                # 좌표리스트 전체 비교
                # 중요한건 이를 위해서는 정규화 시 반드시 소팅해줘야함!
                if space == current_piece:
                    used[i] = True
                    answer += len(space)
                    break

                current_piece = rotate(current_piece)

            # 현재 빈칸에 맞는 조각을 찾았으면
            # 다른 조각은 더 볼 필요 없음
            if used[i]:
                break

    return answer

if __name__ == "__main__":
    game_board = [[1,1,0,0,1,0],[0,0,1,0,1,0],[0,1,1,0,0,1],[1,1,0,1,1,1],[1,0,0,0,1,0],[0,1,1,1,0,0]]
    table = [[1,0,0,1,1,0],[1,0,1,0,1,0],[0,1,1,0,1,1],[0,0,1,0,0,0],[1,1,0,1,1,0],[0,1,0,0,0,0]]
    # game_board = [[0,0,0],[1,1,0],[1,1,1]]
    # table = [[1,1,1],[1,0,0],[0,0,0]]
    print(solution(game_board, table))
