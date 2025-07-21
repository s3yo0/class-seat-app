import streamlit as st
import pandas as pd

# 자리 정의
rows = ['A', 'B', 'C', 'D', 'E']
cols = ['1', '2', '3', '4', '5']
positions = [r + c for r in rows for c in cols]

# 데이터프레임 생성
score_data = pd.DataFrame({'자리': positions})

# 기준별 점수 계산
row_score = {'A': 2.0, 'B': 1.5, 'C': 1.0, 'D': 0.5, 'E': 0.0}
score_data['앞자리'] = score_data['자리'].apply(lambda x: row_score[x[0]])

def outlet_score(pos):
    if pos == 'C5':
        return 1.5
    elif pos in ['B5', 'D5']:
        return 1.0
    elif pos == 'A5':
        return 0.5
    else:
        return 0.0
score_data['콘센트'] = score_data['자리'].apply(outlet_score)
score_data['운동장창가'] = score_data['자리'].apply(lambda x: 1.0 if x[1] == '1' else 0.0)
score_data['에어컨'] = score_data['자리'].apply(lambda x: 1.0 if x in ['C2', 'C3', 'C4', 'D2', 'D3', 'D4'] else 0.0)
score_data['출입문기피'] = score_data['자리'].apply(lambda x: -1.0 if x in ['A5', 'E5'] else 0.0)
def front_desk_score(x):
    if x in ['A2', 'A3', 'A4']:
        return -1.0
    elif x in ['B2', 'B3', 'B4']:
        return -0.5
    else:
        return 0.0
score_data['교탁근처기피'] = score_data['자리'].apply(front_desk_score)

# Streamlit UI
st.title("🪑 교실 자리 추천기")
st.markdown("기준별 중요도를 설정하세요 (0 = 무시, 2 = 매우 중요)")

weights = {
    '앞자리': st.slider('앞자리 중요도', 0.0, 2.0, 1.0, 0.1),
    '콘센트': st.slider('콘센트 중요도', 0.0, 2.0, 1.0, 0.1),
    '운동장창가': st.slider('운동장 창가 중요도', 0.0, 2.0, 1.0, 0.1),
    '에어컨': st.slider('에어컨 근처 중요도', 0.0, 2.0, 1.0, 0.1),
    '출입문기피': st.slider('출입문 근처 기피 정도', 0.0, 2.0, 1.0, 0.1),
    '교탁근처기피': st.slider('교탁 근처 기피 정도', 0.0, 2.0, 1.0, 0.1)
}

# 총점 계산
def calculate_total(row, weights):
    return sum(row[k] * weights[k] for k in weights)

score_data['총점'] = score_data.apply(lambda row: calculate_total(row, weights), axis=1)
sorted_data = score_data.sort_values(by='총점', ascending=False).reset_index(drop=True)

# 결과 출력
st.subheader("📊 추천 순위")
st.dataframe(sorted_data[['자리', '총점']])

top3 = sorted_data.head(3)
st.success(f"🏆 추천 TOP 3 자리는: {', '.join(top3['자리'].tolist())}")

# 자리 시각화
st.subheader("🧭 자리 배치도 (총점 기준 색상 표시)")

# 자리 총점을 행렬 형태로 재배치
seat_matrix = pd.DataFrame(index=rows, columns=cols)
for _, row in score_data.iterrows():
    r, c = row['자리'][0], row['자리'][1]
    seat_matrix.loc[r, c] = round(row['총점'], 1)

# 스타일 적용 및 출력
st.dataframe(seat_matrix.style.background_gradient(cmap='YlOrRd', axis=None))
