import os
import time

def generate_md_toc(root_dir):
    """
    生成Markdown格式的目录

    Args:
        root_dir (str): 根目录路径

    Returns:
        str: Markdown格式的目录
    """
    toc = ""
    for root, dirs, files in os.walk(root_dir):
        # 忽略.assets结尾的文件夹
        if os.path.basename(root).endswith(".assets"):
            continue
        # 忽略没有.md文件的文件夹
        md_files = [f for f in files if f.endswith(".md")]
        if not md_files:
            continue
        # 当前目录和README文档不作为标题
        if root == root_dir or "README.md" in md_files:
            continue
        # 大标题为文件夹名
        toc += f"### {os.path.basename(root)}\n"
        for file in sorted(md_files):
            # 文件名作为小标题，去掉扩展名
            title = os.path.splitext(file)[0]
            # 相对路径
            relative_path = os.path.relpath(os.path.join(root, file), root_dir)
            # 添加链接
            toc += f"  - [{title}]({relative_path})"
            # 获取文件上次修改时间
            last_update_time = time.strftime(" _Last updated: %Y-%m-%d %H:%M:%S_", time.localtime(os.path.getmtime(os.path.join(root, file))))
            # 在文件链接后面添加上次更新时间的备注
            toc += last_update_time + "\n"
    return toc

def write_to_readme(toc):
    """
    将目录写入README.md文件中

    Args:
        toc (str): Markdown格式的目录
    """
    with open("README.md", "w") as f:
        f.write(toc)

def create_readme_if_not_exists():
    """
    如果不存在README.md文件，则创建一个空的README.md文件
    """
    if not os.path.exists("README.md"):
        with open("README.md", "w"):
            pass

root_dir = "."
toc = generate_md_toc(root_dir)
create_readme_if_not_exists()
write_to_readme(toc)