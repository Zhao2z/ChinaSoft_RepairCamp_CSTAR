import re
import os

# !重要：默认行号从1开始

"""
# 项目名
project_name = 'AaltoXml'  # TODO: 修改为实际的项目名

# 项目对应的 bug ids
bug_ids = [1, 2, 3, 4, 5, 7, 8, 9]  # TODO: 修改为实际的bug id  

# 待修复文件所在包的目录
package_dir = "<project_dir>/src/main/java"  # TODO: 修改为实际的包目录

# 模型输入文件
src_test_txt = f'./src_test.txt'  # TODO: 修改为实际的文件路径

# 信息记录文件，便于合成最终的修复结果
info_file = f'./info.txt'  # TODO: 修改为实际的文件路径
"""

def gen_input_file(project_name, bug_id, package_dir, src_test_txt, info_file, package_name , java_file_name, line_numbers, function_start_line, function_end_line):

    def convert_single_to_multi_line_comments(lines):
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


    # 找到连续的行号
    def find_consecutive_numbers(numbers):
        if not numbers:
            return []
        
        numbers.sort()
        consecutive_groups = []
        current_group = [numbers[0]]

        for i in range(1, len(numbers)):
            if numbers[i] == numbers[i - 1] + 1:
                current_group.append(numbers[i])
            else:
                consecutive_groups.append(current_group)
                current_group = [numbers[i]]
        
        consecutive_groups.append(current_group)

        return consecutive_groups

    consecutive_groups = find_consecutive_numbers(line_numbers)
    # 生成待修复文件路径
    to_fix_file = package_dir


    # 获取待修复行的上下文
    def get_context(lines, start, end, function_start_line, function_end_line, line_limit=30):
        total_lines = len(lines)
        context_lines = []

        # 计算函数的总行数
        function_lines_count = function_end_line - function_start_line + 1

        # 如果函数的总行数不超过 line_limit 行，则将整个函数作为上下文
        if function_lines_count <= line_limit:
            context_lines = lines[function_start_line - 1:function_end_line]
        else:
            # 计算从函数起始行到 end 行的行数
            func_start_to_end_count = end - function_start_line + 1

            if func_start_to_end_count <= line_limit:
                # 将 [function_start_line, end] 范围的行纳入上下文
                context_lines = lines[function_start_line - 1:end]

                # 从 end 行向下寻找，直到上下文加上 [start, end] 行的行数达到 line_limit 行
                remaining_lines = line_limit - func_start_to_end_count
                context_lines.extend(lines[end:min(end + remaining_lines, total_lines)])
            else:
                # 将 (line_limit - (end - start + 1)) 行平均分配给start前和end后的行
                remaining_lines = line_limit - (end - start + 1)
                before_start_lines = remaining_lines // 2
                after_end_lines = remaining_lines - before_start_lines

                # 获取start前的行
                context_lines.extend(lines[max(function_start_line - before_start_lines - 1, 0):function_start_line - 1])

                # 获取[start, end]范围的行
                context_lines.extend(lines[start - 1:end])

                # 获取end后的行
                context_lines.extend(lines[end:min(end + after_end_lines, total_lines)])

        return context_lines

    for consecutive_group in consecutive_groups:
        start = consecutive_group[0] - 1
        end = consecutive_group[-1] - 1
        
        # print(f"start: {start}, end: {end}")

        # 读取待修复文件
        with open(to_fix_file, 'r') as file:
            lines = file.readlines()

        # 保证 start 和 end 在合理范围内
        start = max(0, start)
        end = min(len(lines) - 1, end)

        lines[start] = '<BUGS> ' + lines[start].lstrip()
        lines[end] = lines[end].rstrip() + ' <BUGE>\n'

        context_lines = get_context(lines, start, end, function_start_line, function_end_line)

        context_lines = convert_single_to_multi_line_comments(context_lines)


        # 把 context_lines 改成单行字符串
        single_line_context = ''
        for context_line in context_lines:
            single_line_context += context_line.strip() + ' '
        
        single_line_context = single_line_context.strip()

        with open(src_test_txt, 'a') as f1:
            f1.write(single_line_context + '\n')
        
        with open(info_file, 'a') as f2:
            f2.write(f'{project_name};{bug_id};{to_fix_file};{start + 1};{end + 1}\n')


# project_name = 'Bcel'  # TODO: 修改为实际的项目名

# # 项目对应的 bug ids
# bug_ids = [1]  # TODO: 修改为实际的bug id

# # 待修复文件所在包的目录
# package_dir = "/tmp/Bcel_1_buggy/src/main/java"  # TODO: 修改为实际的包目录

# # 模型输入文件
# src_test_txt = f'./src_test.txt'  # TODO: 修改为实际的文件路径

# # 信息记录文件，便于合成最终的修复结果
# info_file = f'./info.txt'  # TODO: 修改为实际的文件路径

# gen_input_file(project_name, bug_ids[0], package_dir, src_test_txt, info_file, 69, 79)