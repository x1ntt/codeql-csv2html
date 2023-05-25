import filter

import pandas as pd
import sys
import time

# 生成规则标题行
def gen_tr_rule_title(item, rule_id, error_num):
    tmp_str = """
        <tr onclick="hide_item(this, '{{rule_id}}', false)">
            <td colspan="4" class="title_row">
                <div>
                    <h3>{{rule_name}} <span class="error_num">{{error_num}}<span></h3>
                    <p>{{rule_desc}}</p>
                </div>
            </td>
        </tr>
    """
    tmp_str = tmp_str.replace("{{rule_id}}", rule_id)
    tmp_str = tmp_str.replace("{{rule_name}}", str(item[1]))
    tmp_str = tmp_str.replace("{{rule_desc}}", str(item[2]))
    tmp_str = tmp_str.replace("{{error_num}}", str(error_num))
    return tmp_str

# 生成规则行
def gen_tr_rule_line(item, rule_id):
    tmp_str = """
        <tr class="data_item data_item_none {{rule_id}} etype_{{error_level}}" style="display: none;">
            <td>{{file_name}}</td>
            <td>{{rule_info}}</td>
            <td>{{error_level}}</td>
            <td>{{loction}}</td>
        </tr>
    """
    tmp_str = tmp_str.replace("{{rule_id}}", rule_id)
    tmp_str = tmp_str.replace("{{file_name}}", str(item[5]))
    tmp_str = tmp_str.replace("{{rule_info}}", str(item[4]))
    tmp_str = tmp_str.replace("{{error_level}}", str(item[3]), 2)
    tmp_str = tmp_str.replace("{{loction}}", str(item[6])+"行"+str(item[7])+"列")
    return tmp_str

# 生成过滤器
def gen_error_filter(error_type_set):
    tmp_str = ""
    for type in error_type_set:
        tmp_str += "<button id=\"etype_" + str(type) + "\" class=\"filter_btn\" onclick=\"hide_error(this)\">" + str(type) + "</button>";
    return tmp_str

# 生成提示信息
def gen_info_tips(rule_num, rule_type_num):
    tmp_str = "Trigger <b>"+str(rule_type_num)+"</b> rules for a total of <b>"+ str(rule_num) +"</b> reports, file generation time: " + time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()));
    return tmp_str

# 生成表里面的内容
def gen_table_html(rmap):
    cnt = 0
    total_table_html = ""

    for k,v in rmap.items():
        if len(v) == 0:
            continue
        rule_id = "rule_"+str(cnt)
        total_table_html += gen_tr_rule_title(v[0], rule_id, len(v))
        for item in v:
            total_table_html += gen_tr_rule_line(item, rule_id)
        cnt += 1
    return total_table_html

# 组装
def render_html(table_content, error_content, info_tips_content, template_file):
    template_str = ""
    with open(template_file, "r") as f:
        template_str = f.read()
    template_str = template_str.replace("{{error_content}}", error_content)
    template_str = template_str.replace("{{table_content}}", table_content)
    template_str = template_str.replace("{{info_tips_content}}", info_tips_content)
    return template_str

def main(template_file, csv_file, target_file):
    df = pd.read_csv(csv_file)
    rule_map = {}
    error_type_set = set()
    rule_num = 0
    rule_type_num = 0

    for row in df.itertuples():
        rule_name = str(row[1])
        if not filter.test_file_name(str(row[5])):
            continue
        if rule_name in rule_map.keys():
            rule_map[rule_name].append(row)
            rule_num += 1
        else:
            rule_map[rule_name] = [row]
            rule_type_num += 1
            rule_num += 1
        error_type_set.add(row[3])

    table_content = gen_table_html(rule_map)
    error_content = gen_error_filter(error_type_set)
    info_tips_content = gen_info_tips(rule_num, rule_type_num)
    final_html = render_html(table_content, error_content, info_tips_content, template_file)
    
    with open(target_file, "w") as f:
        f.write(final_html)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Rendering cvs files to template.html")
        print("usage: ./" + sys.argv[0] + " template.html ctest.csv index.html")
        exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
