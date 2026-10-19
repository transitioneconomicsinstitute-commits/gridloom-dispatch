import pytest
from open_pcm.case import crf

def test_crf_zero_rate():
    assert crf(0, 20) == pytest.approx(1/20)

def test_crf_positive_rate():
    assert crf(0.08, 25) == pytest.approx(0.0936788, rel=1e-6)

def test_crf_rejects_bad_inputs():
    with pytest.raises(ValueError):
        crf(0.05, 0)
    with pytest.raises(ValueError):
        crf(-1, 10)
