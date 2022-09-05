
def is_not_none_and_not_eq(value, not_eq=""):
    if value and value != not_eq:
        return True
    return False
