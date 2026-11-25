import pandas as pd


def 정제(df):
    """명세에 따라 성적 데이터를 정제하고 단계별 행 수를 출력한다."""
    df = df.copy()
    print("시작:", len(df))

    # 점수가 비어 있는 행을 제거한다.
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거:", len(df))

    # 모든 열의 값이 완전히 같은 중복 행을 제거한다.
    df = df.drop_duplicates()
    print("중복 제거:", len(df))

    # 반과 과목의 앞뒤 공백을 제거한다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()

    # 점수가 0점 미만 또는 100점 초과인 행을 제거한다.
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거:", len(df))

    return df


def 반별평균(df):
    """반별 통계표를 출력하고 반 이름을 키로 하는 평균 Series를 반환한다."""
    통계 = df.groupby("반")["점수"].agg(
        ["count", "mean", "median", "max"]
    ).round(2)
    print(통계)
    return 통계["mean"]


if __name__ == "__main__":
    from pathlib import Path

    폴더 = Path(__file__).parent
    원본 = pd.read_csv(폴더 / "scores_2026.csv")
    정제된 = 정제(원본)

    # 수학 과목만 필터링한다.
    수학 = 정제된[정제된["과목"] == "수학"]
    print("수학 행 수:", len(수학))

    # 1반이면서 90점 이상인 행만 필터링한다.
    일반_90점이상 = 정제된[
        (정제된["반"] == "1반") & (정제된["점수"] >= 90)
    ]
    print("1반 90점 이상 행 수:", len(일반_90점이상))

    # 반별 평균을 계산한다.
    print("반별 평균:")
    print(정제된.groupby("반")["점수"].mean())

    # 과목과 반 두 기준으로 평균을 계산한다.
    print("과목 × 반 평균:")
    print(정제된.groupby(["과목", "반"])["점수"].mean())

    # 반별 개수·평균·중앙값·최댓값을 출력한다.
    print("반별 통계:")
    반별평균(정제된)

    # 그룹 합계와 전체 합계, 그룹 개수와 전체 행 수를 검증한다.
    print("그룹 합계:", 정제된.groupby("반")["점수"].sum().sum())
    print("전체 합계:", 정제된["점수"].sum())
    print("그룹 개수:", 정제된.groupby("반")["점수"].count().sum())
    print("전체 행 수:", len(정제된))
