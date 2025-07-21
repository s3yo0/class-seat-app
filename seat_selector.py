import pandas as pd
import streamlit as st
import random

# 자리 정보 생성
rows = ['A', 'B', 'C', 'D', 'E']
cols = ['1', '2', '3', '4', '5']
positions = [r + c for r in rows for c in cols]

# 거리 가중치 정의
def seat_score(row, col):
    score = 0
    if row in ['A', 'E']:  # 가장 앞, 뒤
        score += 1
    elif row in ['B', 'D']:
        score += 2
    else:
        score += 3

    if col in ['1', '5']:  # 가장 왼쪽, 오른쪽
        score += 1
    elif col in ['2', '4']:
        score += 2
    else:
        score += 3
    return score

# 데이터프레임 생성
seat_data = []
for pos in positions:
    r, c = pos[0], pos[1]
    seat_data.append({'자리': pos, '점수': seat_score(r, c)})

df = pd.DataFrame(seat_data)

# 상위 3개 자리 추천
top3 = df.sort_values(by='점수', ascending=False).head(3)

# 추천 결과 출력
st.title("📌 자리 추천기")
st.subheader("🪑 추천된 상위 3개 자리:")
for idx, row in top3.iterrows():
    st.write(f"{idx+1}. 자리: **{row['자리']}**, 점수: {row['점수']}")

# 💡 자리 배치도 시각화
seat_map = ""
for r in rows:
    row_display = ""
    for c in cols:
        pos = r + c
        if pos in top3['자리'].values:
            row_display += f"🟩 {pos} "  # 추천 자리 강조
        else:
            row_display += f"⬜ {pos} "  # 일반 자리
    seat_map += row_display + "\n\n"

st.subheader("🗺️ 전체 자리 배치도 (추천 자리 강조됨)")
st.markdown(f"```\n{seat_map}\n```")
