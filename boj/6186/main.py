import sys

# 베시는 부드러운 봄풀을 뜯어 먹으며 하루를 보낼 계획이다.
# 그리고 농부 존이 정성껏 R행 C열 격자로 나누어 놓은 목초지를 바라보고 있다.
# 베시는 이 목초지에 있는 **풀 덩어리(grass clump)**의 개수를 세고 싶어 한다.
# 각 풀 덩어리는 지도에서 다음과 같이 표시된다.
# 기호 하나만 있는 경우
# 또는 # 기호 두 개가 가로 또는 세로로 서로 붙어 있는 경우
# 단, 대각선으로 붙어 있는 경우는 없다
# 또한 서로 다른 두 풀 덩어리가 인접해 붙어 있는 일도 없다
# 목초지 지도가 주어졌을 때, 풀 덩어리가 총 몇 개인지 구하라는 문제이다.
# 예를 들어 R = 5, C = 6이고 목초지 지도가 다음과 같다고 하자.
# .#....
# ..#...
# ..#..#
# ...##.
# .#....
# 이 경우 풀 덩어리는 총 5개이다.
# 1행에 있는 것 하나
# 2행과 3행의 2열에 걸쳐 세로로 이어진 것 하나
# 3행에 혼자 있는 것 하나
# 4행의 4열과 5열에 가로로 이어진 것 하나
# 5행에 있는 것 하나
# 즉, 이 예시의 정답은 5이다.

# 정리하자면 풀 덩어리는 한 칸, 가로 두개, 세로 두개로 이루어진 조합을 가짐

def main() -> None:
    input = sys.stdin.readline
    R, C = map(int, input().split())
    pasture = [input().rstrip() for _ in range(R)]
    count = 0
    for i in range(R):
        for j in range(C):
            if pasture[i][j] == "#":
                up = (i > 0 and pasture[i - 1][j] == '#')
                left = (j > 0 and pasture[i][j - 1] == '#')

                if not up and not left:
                    count += 1
    print(count)

if __name__ == "__main__":
    main()
