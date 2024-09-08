# venv\Scripts\activate
# deactivate

# Makefile
# 데이터 처리 스크립트 실행
run_data_processing:
	python scripts/data_processing/process_game_data.py

# 차트 시각화 스크립트 실행
run_data_visualization:
	python ./scripts/chart/data_visualization.py