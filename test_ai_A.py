# 임시 초안입니다. 과제 규칙상 별도 AI 대화에서 받은 원본으로 교체해야 합니다.
import pytest
from load_scores import load_scores


def test_scores_csv_has_five_valid_records():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5
    assert len(skipped) == 5


def test_empty_csv_returns_empty_lists():
    assert load_scores("empty.csv") == ([], [])


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_scores("missing.csv")


def test_zero_and_hundred_are_valid(tmp_path):
    p = tmp_path / "edges.csv"
    p.write_text("name,score\nA,0\nB,100\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("A", 0), ("B", 100)]
    assert skipped == []
