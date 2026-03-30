import sys
from itertools import combinations

# 오늘은 스타트링크에 다니는 사람들이 모여서 축구를 해보려고 한다. 축구는 평일 오후에 하고 의무 참석도 아니다.
# 축구를 하기 위해 모인 사람은 총 N명이고 신기하게도 N은 짝수이다.
# 이제 N/2명으로 이루어진 스타트 팀과 링크 팀으로 사람들을 나눠야 한다.

# BOJ를 운영하는 회사 답게 사람에게 번호를 1부터 N까지로 배정했고, 아래와 같은 능력치를 조사했다.
# 능력치 Sij는 i번 사람과 j번 사람이 같은 팀에 속했을 때, 팀에 더해지는 능력치이다. 팀의 능력치는 팀에 속한 모든 쌍의 능력치 Sij의 합이다.
# Sij는 Sji와 다를 수도 있으며, i번 사람과 j번 사람이 같은 팀에 속했을 때, 팀에 더해지는 능력치는 Sij와 Sji이다.

# N=4이고, S가 아래와 같은 경우를 살펴보자.
# 예를 들어, 1, 2번이 스타트 팀, 3, 4번이 링크 팀에 속한 경우에 두 팀의 능력치는 아래와 같다.

# 스타트 팀: S12 + S21 = 1 + 4 = 5
# 링크 팀: S34 + S43 = 2 + 5 = 7
# 1, 3번이 스타트 팀, 2, 4번이 링크 팀에 속하면, 두 팀의 능력치는 아래와 같다.

# 스타트 팀: S13 + S31 = 2 + 7 = 9
# 링크 팀: S24 + S42 = 6 + 4 = 10
# 축구를 재미있게 하기 위해서 스타트 팀의 능력치와 링크 팀의 능력치의 차이를 최소로 하려고 한다.
# 위의 예제와 같은 경우에는 1, 4번이 스타트 팀, 2, 3번 팀이 링크 팀에 속하면 스타트 팀의 능력치는 6,
# 링크 팀의 능력치는 6이 되어서 차이가 0이 되고 이 값이 최소이다.


def main() -> None:
    input = sys.stdin.readline
    N = int(input().strip())
    S = [list(map(int, input().strip().split())) for _ in range(N)]

    min_score_diff = float("inf")

    # 0번 사람은 스타트 팀에 고정
    # 스타트/링크 팀은 이름만 바뀌면 같은 경우이므로
    # 0번을 한쪽 팀에 고정해서 중복 조합을 절반으로 줄인다.
    for rest in combinations(range(1, N), N // 2 - 1):
        start_team = (0,) + rest
        link_team = [i for i in range(N) if i not in start_team]

        start_team_score = 0
        # 팀 내부의 모든 2인 조합에 대해
        # S[a][b] + S[b][a] 를 더한다.
        for i in range(N // 2):
            for j in range(i + 1, N // 2):
                start_team_score += S[start_team[i]][start_team[j]]
                start_team_score += S[start_team[j]][start_team[i]]

        link_team_score = 0
        for i in range(N // 2):
            for j in range(i + 1, N // 2):
                link_team_score += S[link_team[i]][link_team[j]]
                link_team_score += S[link_team[j]][link_team[i]]
        
        # 현재 조합에서 두 팀의 능력치 차이
        score_diff = abs(start_team_score - link_team_score)
        if score_diff == 0:
            print(0)
            return
        min_score_diff = min(min_score_diff, score_diff)
    
    print(min_score_diff)

if __name__ == "__main__":
    main()