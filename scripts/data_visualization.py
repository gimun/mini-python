import json
import matplotlib.pyplot as plt
import koreanize_matplotlib

# JSON 파일 경로
json_file_path = '../data/games_data_4.json'

# JSON 파일 로드
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 데이터 준비
names = [game['name'] for game in data]
play_counts = [game['play_count'] for game in data]
scores = [game['score'] for game in data]
ranks = [game['rank'] for game in data]

# 차트 1: 게임별 플레이 횟수
plt.figure(figsize=(10, 6))
plt.bar(names, play_counts, color='skyblue')
plt.xticks(rotation=90)
plt.xlabel('게임 이름')
plt.ylabel('플레이 횟수')
plt.title('게임별 플레이 횟수')
plt.tight_layout()
plt.show()

# 차트 2: 게임별 점수
plt.figure(figsize=(10, 6))
plt.bar(names, scores, color='lightgreen')
plt.xticks(rotation=90)
plt.xlabel('게임 이름')
plt.ylabel('점수')
plt.title('게임별 점수')
plt.tight_layout()
plt.show()

# 차트 3: 게임별 순위 (낮을수록 좋음)
plt.figure(figsize=(10, 6))
plt.bar(names, ranks, color='salmon')
plt.xticks(rotation=90)
plt.xlabel('게임 이름')
plt.ylabel('순위')
plt.title('게임별 순위')
plt.tight_layout()
plt.show()
