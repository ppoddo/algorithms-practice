import sys
from collections import deque

# 그래프를 DFS로 탐색한 결과와 BFS로 탐색한 결과를 출력하는 프로그램을 작성하시오.
# 단, 방문할 수 있는 정점이 여러 개인 경우에는 정점 번호가 작은 것을 먼저 방문하고,
# 더 이상 방문할 수 있는 점이 없는 경우 종료한다. 정점 번호는 1번부터 N번까지이다.

# 첫째 줄에 정점의 개수 N(1 ≤ N ≤ 1,000), 간선의 개수 M(1 ≤ M ≤ 10,000), 탐색을 시작할 정점의 번호 V가 주어진다.
# 다음 M개의 줄에는 간선이 연결하는 두 정점의 번호가 주어진다. 어떤 두 정점 사이에 여러 개의 간선이 있을 수 있다.
# 입력으로 주어지는 간선은 양방향이다.

# DFS 재귀 호출 깊이 제한 완화
sys.setrecursionlimit(10000)

def dfs(v, graph, visited, result):
    visited[v] = True
    result.append(v)

    # 현재 점과 간선으로 연결된 점들 중 방문 안한 점만 방문
    for nextV in graph[v]:
        if not visited[nextV]:
            dfs(nextV, graph, visited, result)

def bfs(start, graph, visited):
    q = deque([start])
    visited[start] = True
    result = []

    while q:
        v = q.popleft()
        result.append(v)

        # 방문이 필요한 점은 q에 쌓는다.
        for nextV in graph[v]:
            if not visited[nextV]:
                visited[nextV] = True
                q.append(nextV)

    return result

def main() -> None:
    input = sys.stdin.readline
    N, M, V = map(int, input().split())
    graph = [[] for _ in range(N + 1)]

    for _ in range(M):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    # 특정 점 기준 해당 점이 가지고 있는
    # 다른 점 번호들 중에 작은 점부터 방문하기 위해서 미리 정렬하기
    for i in range(1, N + 1):
        graph[i].sort()

    visited_dfs = [False] * (N + 1)
    dfs_result = []
    dfs(V, graph, visited_dfs, dfs_result)

    visited_bfs = [False] * (N + 1)
    bfs_result = bfs(V, graph, visited_bfs)

    print(*dfs_result)
    print(*bfs_result)
if __name__ == "__main__":
    main()
