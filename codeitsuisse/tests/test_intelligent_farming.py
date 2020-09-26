import pytest

from codeitsuisse.routes.intelligent_farming import intelligent_farming, get_dri_score


@pytest.mark.parametrize(
    "gene_seq,expected",
    (
            ("AAACCCAAAGGTTACTGAAAAG", "AAGAAGAAGAAGAATATTCCCC"),
            ("AAAAAACCTTTGGGGGGGTTTT", "AGAGAGAGAGAGCCTTTTTTT"),
    )
)
def test_intelligent_farming(gene_seq, expected):
    actual = intelligent_farming(gene_seq)
    print(actual)
    actual_score = get_dri_score(actual)
    expected_score = get_dri_score(expected)

    assert actual_score >= expected_score
