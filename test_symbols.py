from symbols import Symbol

def test_empty_field_is_zero():
    assert Symbol.is_valid_color(1) == True
    assert Symbol.is_valid_color(6) == False