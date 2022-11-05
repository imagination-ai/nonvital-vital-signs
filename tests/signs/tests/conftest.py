import sys
from os.path import abspath, dirname

try:
    import signs
except ModuleNotFoundError:
    base_path = abspath(dirname(dirname(__file__)))
    print(base_path)
    sys.path.insert(1, base_path)
    import signs


# @pytest.fixture('session')
# def
