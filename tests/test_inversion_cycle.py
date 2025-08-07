from src.ship_in.inversion_logic import invert_signal

def test_invert_signal():
    input_signal = {"momentum": 0.9, "sentiment": -0.3}
    inverted = invert_signal(input_signal)
    assert inverted["momentum"] == -0.9
    assert inverted["sentiment"] == 0.3
