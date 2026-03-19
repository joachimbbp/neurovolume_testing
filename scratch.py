import setup
import test_patterns

setup.from_local()

setup.build_and_link()

test_patterns.download_test_data()
