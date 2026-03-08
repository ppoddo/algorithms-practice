import sys
from collections import Counter, defaultdict

# 스트리밍 사이트에서 장르 별로 가장 많이 재생된 노래를 두 개씩 모아 베스트 앨범을 출시하려 합니다.
# 노래는 고유 번호로 구분하며, 노래를 수록하는 기준은 다음과 같습니다.
# 1. 속한 노래가 많이 재생된 장르를 먼저 수록합니다.
# 2. 장르 내에서 많이 재생된 노래를 먼저 수록합니다.
# 3. 장르 내에서 재생 횟수가 같은 노래 중에서는 고유 번호가 낮은 노래를 먼저 수록합니다.
# 노래의 장르를 나타내는 문자열 배열 genres와 노래별 재생 횟수를 나타내는 정수 배열 plays가 주어질 때,
# 베스트 앨범에 들어갈 노래의 고유 번호를 순서대로 return 하도록 solution 함수를 완성하세요.

def solution(genres, plays):
    answer = []
    # 같은 인덱스번호에 있는 장르와 재생횟수는 하나의 노래
    genre_total = Counter()
    genre_songs = {}
    
    for i, (g, p) in enumerate(zip(genres, plays)):
        genre_total[g] += p
        genre_songs.setdefault(g, []).append((i, p))
    
    answer = []
    # 많이 재생된 장르 먼저 정렬해서 뽑기
    for genre, _ in genre_total.most_common():
        # 장르 내 노래를 재생횟수가 많거나, 같으면 고유번호 기준으로 낮은순으로 정렬
        sorted_songs = sorted(genre_songs[genre], key=lambda x: (-x[1], x[0]))
        # 장르당 최대 2곡
        answer.extend([i for i, _ in sorted_songs[:2]])
    
    return answer
if __name__ == "__main__":
    genres = ["classic", "pop", "classic", "classic", "pop"]
    plays = [500, 600, 150, 800, 2500]
    print(solution(genres, plays))
