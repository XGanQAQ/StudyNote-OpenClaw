#!/usr/bin/env python3
"""
Markdown文件时间范围筛选工具
用于列出指定时间范围内的md文件，方便学习内容分析
"""

import os
import re
from datetime import datetime
import argparse
from pathlib import Path

def extract_date_from_filename(filename):
    """
    从文件名中提取日期
    支持格式: YYYY-MM-DD, YYYYMMDD, YYYY_MM_DD 等
    """
    # 常见日期格式的正则表达式
    date_patterns = [
        r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
        r'(\d{4})\.(\d{2})\.(\d{2})',  # YYYY.MM.DD
        r'(\d{4})_(\d{2})_(\d{2})',  # YYYY_MM_DD
        r'(\d{4})(\d{2})(\d{2})',  # YYYYMMDD
        r'(\d{2})-(\d{2})-(\d{4})',  # DD-MM-YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                try:
                    # 根据格式判断年月日顺序
                    if pattern == r'(\d{2})-(\d{2})-(\d{4})':
                        # DD-MM-YYYY 格式
                        return datetime(int(groups[2]), int(groups[1]), int(groups[0]))
                    else:
                        # 其他格式默认是 YYYY-MM-DD 或变体
                        year_idx = 0 if len(groups[0]) == 4 else 2
                        month_idx = 1 if year_idx == 0 else (0 if len(groups[0]) == 2 else 1)
                        day_idx = 2 if year_idx == 0 else (1 if month_idx == 0 else 0)
                        
                        year = int(groups[year_idx]) if len(groups[year_idx]) == 4 else int(groups[year_idx]) + 2000
                        return datetime(year, int(groups[month_idx]), int(groups[day_idx]))
                except (ValueError, IndexError):
                    continue
    return None

def get_file_creation_time(filepath):
    """获取文件的创建时间"""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath))
    except:
        return None

def get_file_modification_time(filepath):
    """获取文件的修改时间"""
    try:
        return datetime.fromtimestamp(os.path.getmtime(filepath))
    except:
        return None

def find_md_files_by_date_range(directory, start_date, end_date, use_date_from=None):
    """
    在指定时间范围内查找md文件
    
    Args:
        directory: 要搜索的目录
        start_date: 开始日期
        end_date: 结束日期
        use_date_from: 使用哪种时间判断方式
            'filename' - 从文件名提取日期
            'ctime' - 文件创建时间
            'mtime' - 文件修改时间
            'all' - 使用最早可用的时间
    """
    md_files = []
    
    # 确保目录存在
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        return []
    
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.md'):
                file_path = os.path.join(root, file)
                
                # 获取文件日期
                file_date = None
                
                if use_date_from in ['filename', 'all']:
                    file_date = extract_date_from_filename(file)
                
                if not file_date and use_date_from in ['ctime', 'all']:
                    file_date = get_file_creation_time(file_path)
                
                if not file_date and use_date_from in ['mtime', 'all']:
                    file_date = get_file_modification_time(file_path)
                
                if file_date:
                    # 检查是否在时间范围内
                    if start_date <= file_date <= end_date:
                        # 获取相对路径以便阅读
                        rel_path = os.path.relpath(file_path, directory)
                        md_files.append({
                            'path': rel_path,
                            'date': file_date,
                            'full_path': file_path
                        })
    
    # 按日期排序
    md_files.sort(key=lambda x: x['date'])
    return md_files

def export_to_txt(files, output_file, include_date=True):
    """将结果导出到文本文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"找到 {len(files)} 个Markdown文件:\n")
        f.write("=" * 60 + "\n\n")
        
        for file_info in files:
            if include_date:
                date_str = file_info['date'].strftime("%Y-%m-%d")
                f.write(f"{date_str} - {file_info['path']}\n")
            else:
                f.write(f"{file_info['path']}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("文件分析提示：\n")
        f.write("1. 将上述列表提供给AI进行分析\n")
        f.write("2. 可以请AI识别学习主题的分布\n")
        f.write("3. 可以请AI分析学习内容的演变趋势\n")
        f.write("4. 可以请AI建议未来的学习方向\n")

def main():
    parser = argparse.ArgumentParser(description='查找指定时间范围内的Markdown文件')
    parser.add_argument('directory', help='要搜索的目录路径')
    parser.add_argument('--start', required=True, help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end', required=True, help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--output', default='md_files_list.txt', help='输出文件名 (默认: md_files_list.txt)')
    parser.add_argument('--date-from', default='all', 
                       choices=['filename', 'ctime', 'mtime', 'all'],
                       help='日期来源: filename(文件名), ctime(创建时间), mtime(修改时间), all(自动选择)')
    parser.add_argument('--no-date', action='store_true', help='输出时不包括日期')
    
    args = parser.parse_args()
    
    # 解析日期
    try:
        start_date = datetime.strptime(args.start, '%Y-%m-%d')
        end_date = datetime.strptime(args.end, '%Y-%m-%d')
    except ValueError:
        print("错误: 日期格式应为 YYYY-MM-DD")
        return
    
    print(f"搜索目录: {args.directory}")
    print(f"时间范围: {args.start} 到 {args.end}")
    print(f"日期来源: {args.date_from}")
    print("正在搜索...")
    
    # 查找文件
    md_files = find_md_files_by_date_range(
        args.directory, 
        start_date, 
        end_date,
        args.date_from
    )
    
    if not md_files:
        print("在指定时间范围内未找到Markdown文件")
        return
    
    # 输出到控制台
    print(f"\n找到 {len(md_files)} 个Markdown文件:")
    print("=" * 60)
    for file_info in md_files[:10]:  # 只显示前10个
        date_str = file_info['date'].strftime("%Y-%m-%d")
        print(f"{date_str} - {file_info['path']}")
    
    if len(md_files) > 10:
        print(f"... 还有 {len(md_files) - 10} 个文件")
    
    # 导出到文件
    export_to_txt(md_files, args.output, not args.no_date)
    print(f"\n完整列表已保存到: {args.output}")
    
    # 生成AI分析提示
    print("\n" + "=" * 60)
    print("你可以将生成的文件内容复制给AI，并使用以下提示语：")
    print("""
请分析我过去一年多的学习记录文件列表：
1. 请根据文件名识别和分类我的学习主题（如编程、语言、专业知识等）
2. 分析我在不同时间段的学习重点和演变趋势
3. 统计各个主题的学习频率和分布
4. 基于我的学习历史，建议我应该深化哪些领域或探索哪些新方向
5. 指出可能存在的时间安排或主题分布上的改进空间
""")

if __name__ == "__main__":
    main()