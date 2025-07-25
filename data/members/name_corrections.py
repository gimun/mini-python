# name_corrections.py

# 사용자 제공 오류 로그 기반으로 잘못된 이름과 정정해야 할 이름 매핑 생성
# 업로드한 파일(name_corrections.json)에 정의된 잘못된 이름들을 바탕으로 자동 보정해서 결과에 반영해줘.
# 이름 자동 정정 시 아래 NAME_CORRECTIONS 참조해줘

### 요청
# 업로드한 이미지에서 JSON 데이터를 추출해서 복사 가능한 형태로 보여줘.
# 이름 자동 정정은 `name_corrections.py` 파일의 `NAME_CORRECTIONS`를 참조해줘.
# 결과는 반드시 JSON 형식으로 보여줘.

NAME_CORRECTIONS = {
    "무명이느 야옹": "무명이는 야옹",
    "제타몽": "졔타몽",
    "비성이는 야옹": "비셩이는 야옹",
    "윤쭝쭝": "윤쫑쫑",
    "보라너쿨": "보라너굴",
    "뭉이완다": "뭉이완댜",
    "몽이완댜": "뭉이완댜",
    "하늘": "하눌",
    "슾찌": "승찌",
    "란게링": "란계링",
    "전애용이다옹": "전애옹이다옹",
    "부르쥬아": "부르주아",
    "모연": "묘연",
    "다공": "다곰",
}
