import sys

# N개의 정수가 주어진다. 이때, 최솟값과 최댓값을 구하는 프로그램을 작성하시오.
def main() -> None:
    input = sys.stdin.readline

    N = int(input().strip())
    numbers = list(map(int, input().strip().split()))

    print(min(numbers), max(numbers))

if __name__ == "__main__":
    main()
