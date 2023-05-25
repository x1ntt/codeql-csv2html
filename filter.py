import re

filter_list = [
    "^/share/",
    "^/ctest/hj/task/",
    "^/ctest/hj/template/"
]

def test_file_name(file_name):
    for f in filter_list:
        if re.match(f, file_name) != None:
            return False
    return True

test_list = [
    "/utils/common/thread.h",
    "/ctest/hj/table/table.h",
    "/ctest/hj/template/555",
    "/ttpp/hh",
    ""
]

if __name__ == "__main__":
    for test in test_list:
        print (test +":" + str(test_file_name(test)))