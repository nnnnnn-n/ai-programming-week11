import csv
import pytest
from load_scores import load_scores


def test_정상_파일에서_유효한_점수만_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert kept == [("김하나", 88), ("최,네번", 77), ("김하나", 91), ("윤보람", 64), ("서한별", 95)]
    assert len(skipped) == 5


def test_빈_줄은_기록하지_않고_건너뛴다(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text("name,score\n가나다,80\n\n라마바,90\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [("가나다", 80), ("라마바", 90)]
    assert skipped == []


def test_이름에_쉼표가_있어도_하나의_이름으로_읽는다(tmp_path):
    path = tmp_path / "comma.csv"
    path.write_text('name,score\n"최,네번",77\n', encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [("최,네번", 77)]
    assert skipped == []


def test_없는_파일이면_FileNotFoundError가_난다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_헤더만_있는_파일은_빈_결과를_돌려준다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize("score, is_valid", [(0, True), (100, True), (101, False)])
def test_점수_경계값(score, is_valid, tmp_path):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n테스트,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert (len(kept) == 1) is is_valid
    if is_valid:
        assert kept == [("테스트", score)]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1
        assert skipped[0][2] == "점수가 0~100 밖"
