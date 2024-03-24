import re

test_string = """
aaa@bbb.com
123@abc.co.kr
test@test.io
do@do.co.en
qwe@qwe.net
qwe@qwe.net
qwe@qwe.net
"""

# results = re.findall(r'[\w\.-]+@[\w\.-]+', test_string)
# results = list(set(results))

results = list(set(re.findall(r'[\w\.-]+@[\w\.-]+', test_string)))

print(results)