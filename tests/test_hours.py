import pytest
import open_pcm as gd

def test_bad_hours_rejected():
    c = gd.Case('examples/synthetic_4node')
    with pytest.raises(ValueError):
        gd.dispatch(c, 2027, range(10, 5))
    with pytest.raises(ValueError):
        gd.dispatch(c, 2027, range(8750, 8770))
