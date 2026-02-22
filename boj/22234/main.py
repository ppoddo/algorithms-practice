import sys
from collections import deque

# 가희는 창구가 하나인 은행을 운영하고 있습니다. 가희의 은행이 영업을 시작했을 때, 대기 줄에는 손님이 N명 있습니다.
# x번 손님에 대한 정보는 x번 손님의 id 값인 Px와 업무를 처리하는 데 필요한 시간인 tx초로 정보가 주어지게 됩니다.
# 은행이 영업을 시작하고 난 후에 들어오는 손님은 M명 있습니다. 이 손님들은 입력을 받은 순서대로 각각 N+1, N+2, ..., N+M번 손님이 됩니다.
# 이 손님들에 대한 정보는 x번 손님의 id 값인 Px와 업무를 처리하는 데 필요한 시간인 tx초, 영업 시작 cx초 후에 들어왔다는 정보가 주어지게 됩니다.
# 손님은 은행에 들어옴과 동시에, 대기 큐의 맨 뒤에 서게 됩니다. N+1번 손님이 은행을 영업을 시작하고 cN+1초 후에 들어왔다고 생각해 보겠습니다.

# N+1번 손님은 은행에 들어오자 마자 대기 큐의 맨 뒤에 줄을 서게 되므로, 영업을 시작하고 cN+1초 후에 대기 큐의 상태는 위와 같습니다.
# 창구에 있는 직원과 고객들은 아래와 같은 알고리즘으로 업무를 처리합니다.
# 대기 큐의 맨 앞에 있는 고객이 x번 손님이라고 하면, 창구에 있는 직원은
# tx가 T보다 크다면, x번 손님의 업무를 T초동안 처리합니다. 그 후, x번 손님의 업무가 끝나는 데 필요한 시간인 tx는 T만큼 감소합니다.
# 그렇지 않으면, x번 손님의 업무를 tx초 동안 처리합니다. 이후에, x번 손님의 업무가 끝나는 데 필요한 시간인 tx는 은 0이 됩니다.
# 대기 큐의 맨 앞에 있는 고객인 x번 손님은
# 업무가 끝나는 데 필요한 시간인 tx가 0이 되었다면, 은행 바깥으로 나가게 됩니다.
# 그렇지 않으면 대기 큐의 맨 뒤로 이동하게 됩니다. 만약에 이 때 도착한 손님이 있다면, 도착한 손님 뒤로 가게 됩니다.
# 대기 큐에 고객이 남았다면 1로 돌아갑니다.
# 은행이 영업을 시작할 때 부터 창구에 있는 직원은 일을 시작합니다.
# 은행이 영업을 시작한 시점으로부터 0초가 지났을 때 부터 W-1초가 지날 때 까지 창구에 있는 직원이 어떤 고객의 업무를 처리하는지 알려주세요.

# 첫 번째 줄에 N과 T, W가 공백을 구분으로 해서 주어집니다.
# 두 번째 줄 부터 N개의 줄에는 0초일 때, 대기 큐의 앞에 있는 고객부터, Px와 고객이 일을 처리하는 데 필요한 시간 tx가 공백으로 구분되어 주어집니다.
# N+2번째 줄에는, 1초 이후에 은행에 들어온 고객 수 M이 주어집니다.
# N+3번째 줄부터 M개의 줄에 걸쳐서, Px, tx, cx가 공백으로 구분되어 주어집니다. 입력된 순서대로 각각 N+1, ..., N+M번 고객입니다.
# 이는 고객 id가 Px인 고객은 일을 처리하는 데 필요한 시간이 tx초이고, 영업 시작 시간으로부터 cx초가 지났을 때 은행에 들어왔다는 것을 의미합니다.

def main() -> None:
    input = sys.stdin.readline
    # N: 최초 대기 줄 손님, T: 직원이 한 번에 처리할 수 있는 최대 업무 시간, W : 직원이 어떤 고객의 업무를 처리하는지 알려주는 시간 범위
    # N만큼 다음 N줄에 손님id와 손님의 업무 처리 시간이 주어짐
    # N + 1 번째 줄에 M이 주어짐
    # M만큼 늦게 온 손님의 정보가 주어짐 (손님id, 업무 처리 시간, 영업 시작 후 들어온 시간)
    N, T, W = map(int, input().strip().split())
    queue = deque()
    for _ in range(N):
        P, t = map(int, input().strip().split())
        queue.append((P, t))
    M = int(input().strip())
    late = []
    for _ in range(M):
        P, t, c = map(int, input().split())
        late.append((c, P, t))  # cx 먼저
    late.sort()

    j = 0
    current_time = 0
    result = []

    while current_time < W and (queue or j < M):
        if not queue:
            current_time = late[j][0]
            while j < M and late[j][0] <= current_time:
                queue.append((late[j][1], late[j][2]))
                j += 1
            continue

        P, t = queue.popleft()
        serve = min(t, T)

        result.extend([P] * min(serve, W - current_time))

        current_time += serve

        # 뒤늦게 합류하는 손님
        while j < M and late[j][0] <= current_time:
            queue.append((late[j][1], late[j][2]))
            j += 1

        # 업무가 끝나지 않은 경우는 맨 뒤로 이동
        if t > T:
            queue.append((P, t - T))

    print("\n".join(map(str, result)))

if __name__ == "__main__":
    main()
