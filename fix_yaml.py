import os
import re

# 设置你的 posts 文件夹路径
POSTS_DIR = 'content/posts'

# 正则表达式：匹配开头是 title: 或 linktitle: ，并且后面没有用引号包围的内容
# (?!["']) 的意思是“排除掉已经有双引号或单引号的情况”
pattern = re.compile(r'^(title|linktitle)(:\s*)(?!["\'])(.*)$', re.MULTILINE)

def fix_quotes(match):
    key = match.group(1)      # title 或 linktitle
    space = match.group(2)    # 冒号和空格
    value = match.group(3).strip() # 实际的标题内容
    
    # 将内容里原有的双引号转义 (变成 \")，防止破坏 YAML 结构
    value = value.replace('"', '\\"')
    
    return f'{key}{space}"{value}"'

def main():
    count = 0
    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(POSTS_DIR):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 将文件切分为 Front Matter 和 正文
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    front_matter = parts[1]
                    body = parts[2]

                    # 检查是否有需要修复的字段
                    if pattern.search(front_matter):
                        new_front_matter = pattern.sub(fix_quotes, front_matter)
                        new_content = f"---{new_front_matter}---{body}"

                        # 将修改后的内容写回文件
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                        print(f"✅ 已修复: {filepath}")

    print(f"\n🎉 批量处理完成！共修复了 {count} 篇文章。")

if __name__ == '__main__':
    main()