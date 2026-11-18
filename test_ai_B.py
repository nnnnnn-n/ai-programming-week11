# 임시 초안입니다. 과제 규칙상 명세만 제공한 별도 AI 대화의 원본으로 교체해야 합니다.
import pytest
from load_scores import load_scores


def test_valid_rows_and_invalid_rows_are_separated():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5
    assert len(skipped) == 5


def test_blank_line_is_ignored_without_skip_record(tmp_path):
    p = tmp_path / "blank.csv"
    p.write_text("name,score\nA,70\n\nB,80\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("A", 70), ("B", 80)]
    assert skipped == []


def test_comma_in_quoted_name_is_preserved(tmp_path):
    p = tmp_path / "comma.csv"
    p.write_text('name,score\n"A,B",90\n', encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("A,B", 90)]
    assert skipped == []


def test_missing_path_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_scores("missing.csv")


@pytest.mark.parametrize("score,valid", [(0, True), (100, True), (101, False)])
def test_score_range(score, valid, tmp_path):
    p = tmp_path / "range.csv"
    p.write_text(f"name,score\nA,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert bool(kept) is valid
    assert len(skipped) == (0 if valid else 1)
