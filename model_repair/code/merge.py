import os
import re
import shutil

# 将单行注释转换为多行注释
def convert_single_to_multi_line_comments(lines: list[str]) -> list[str]:
    converted_lines = []
    single_line_comment_pattern = re.compile(r'^(.*)//(.*)$')

    for line in lines:
        match = single_line_comment_pattern.match(line)
        if match:
            code_part = match.group(1)
            comment_part = match.group(2)
            converted_line = f"{code_part}/*{comment_part}*/\n"
            converted_lines.append(converted_line)
        else:
            converted_lines.append(line)

    return converted_lines

# 提取 <BUGS> 和 <BUGE> 之间的内容
def extract_bug_content(buggy_line: str) -> str:
    pattern = r'<BUGS>(.*?)<BUGE>'
    match = re.search(pattern, buggy_line)
    if match:
        bug_content = match.group(1).strip()
    else:
        bug_content = ''
    
    return bug_content

# 提取 <FIXS> 和 <FIXE> 之间的内容
def extract_patch_content(patch: str) -> str:
    pattern = r'<FIXS>(.*?)<FIXE>'
    match = re.search(pattern, patch)
    if match:
        patch_content = match.group(1).strip()
    else:
        patch_content = ''
    
    return patch_content


info_file = '/home/share/info_v2.txt'
input_file = '/home/share/input_v2.txt'
output_file = '/home/share/output_v2.txt'

with open(info_file, 'r') as f:
    info_lines = f.readlines()

with open(input_file, 'r') as f:
    input_lines = f.readlines()

with open(output_file, 'r') as f:
    output_lines = f.readlines()

for i, line in enumerate(info_lines):
    if line.strip() != '':
        project_name, bug_id, to_fix_file, start, end = line.strip().split(';')
        print(project_name, bug_id, to_fix_file, start, end)

        merged_file = to_fix_file.replace('/tmp', '/home/zhengjie/Desktop/ccf_competition/merged')
        # 如果merged_file文件不存在
        if not os.path.exists(merged_file):
            merged_dir = os.path.dirname(merged_file)
            if not os.path.exists(merged_dir):
                os.makedirs(merged_dir)
            shutil.copy(to_fix_file, merged_file)
        
        start = int(start)
        end = int(end)
        with open(merged_file, 'r') as f:
            lines = f.readlines()

        to_fix_lines = lines[start - 1:end]

        to_fix_lines = convert_single_to_multi_line_comments(to_fix_lines)
        to_fix_single_line = ''
        for to_fix_line in to_fix_lines:
            to_fix_single_line += to_fix_line.strip() + ' '

        bug_content = extract_bug_content(input_lines[i]).strip()
        patch_content = extract_patch_content(output_lines[i]).strip()

        # 将 to_fix_single_line 中匹配 bug_content 的字符替换为 patch_content
        pattern = re.escape(bug_content)
        patched_single_line = re.sub(pattern, patch_content, to_fix_single_line)
        
        lines[start - 1] = patched_single_line.strip() + '\n'
        for i in range(start, end):
            lines[i] = '\n'
        
        with open(merged_file, 'w') as f:
            f.writelines(lines)
            
            










        