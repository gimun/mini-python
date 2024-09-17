import json
import matplotlib.pyplot as plt
import koreanize_matplotlib
import polars as pl

# 'ggplot': 간단하고 깔끔한 스타일.
# 'seaborn': 미리 정의된 세련된 스타일.
# 'fivethirtyeight': 통계적 데이터 시각화에 사용.
# 'bmh': 비즈니스 및 관리 관련 시각화에 적합.
# 'dark_background': 어두운 배경에 밝은 텍스트와 요소를 사용
# 스타일 적용 (예: 'ggplot' 스타일 적용)
plt.style.use('ggplot')

# JSON 파일 경로
file_0908_path = '../../data/charts/member/member_data_240908.json'
file_0918_path = '../../data/charts/member/member_data_240918.json'

# JSON 파일 읽기
with open(file_0908_path, 'r', encoding='utf-8') as f_0908:
    data_0908 = json.load(f_0908)

with open(file_0918_path, 'r', encoding='utf-8') as f_0918:
    data_0918 = json.load(f_0918)

# Polars DataFrame으로 변환
df_0908 = pl.DataFrame(data_0908)
df_0918 = pl.DataFrame(data_0918)

# 두 DataFrame을 병합하여 rank 변화 비교
merged_df = df_0908.join(df_0918, on='name', suffix='_0918')

# rank 변화 계산
merged_df = merged_df.with_columns(
    (pl.col('rank') - pl.col('rank_0918')).alias('rank_change')
)

# 랭킹 변화가 0인 사람 제외
merged_df = merged_df.filter(pl.col('rank_change') != 0)

# Polars DataFrame을 Python list로 변환 (차트에 사용하기 위해)
merged_data = merged_df.select(['name', 'rank_change']).to_dicts()

# 차트 생성
plt.figure(figsize=(18, 10))  # 너비 16인치, 높이 9인치로 설정
# Vertical Bar Chart
# plt.barh([entry['name'] for entry in merged_data], [entry['rank_change'] for entry in merged_data], color='skyblue')

# Line Chart
plt.plot([entry['name'] for entry in merged_data], [entry['rank_change'] for entry in merged_data], marker='o',
         linestyle='-', color='red')

plt.xlabel('랭크 변화 (양수 = 랭크 상승, 음수 = 랭크 하락)', fontsize=10, labelpad=20)
plt.ylabel('', fontsize=10, labelpad=15)
plt.title('09.08 ~ 09.18 랭크 변화 (변동이 없는 사람 제외)', fontsize=13)
plt.xticks(rotation=0, ha='center', fontsize=13, color='#624E88', fontweight='bold')
plt.yticks(fontsize=13, fontweight='bold', color='darkblue')
plt.tight_layout()

# 차트 출력
plt.show()
