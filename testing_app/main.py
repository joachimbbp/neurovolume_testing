import test_patterns
import render
import env

env.build()

test_patterns.test_hello()
test_patterns.test_pyramid()

test_patterns.download_test_data()
test_patterns.test_anat_static()
test_patterns.test_bold_seq_direct()

render.render_tests()
