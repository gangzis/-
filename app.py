import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 定义笔记文件的路径
NOTES_FILE = 'notes.json'


# 初始化笔记数据
def load_notes():
    try:
        with open(NOTES_FILE, 'r') as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            else:
                return {}
    except FileNotFoundError:
        return {}


# 保存笔记到文件
def save_notes(notes):
    with open(NOTES_FILE, 'w') as file:
        json.dump(notes, file)


# 加载已有笔记（按学科分类）
notes = load_notes()

# 设置默认的学科列表
subjects = ["Math", "Science", "History", "Literature"]


@app.route('/')
def home():
    return "Hello, welcome to your categorized study website!"


# 显示特定学科的笔记和上传表单
@app.route('/notes', methods=['GET', 'POST'])
def notes_page():
    if request.method == 'POST':
        # 获取表单中的学科和笔记内容
        subject = request.form['subject']
        note_content = request.form['content']

        # 如果该学科不存在，则创建一个空列表
        if subject not in notes:
            notes[subject] = []

        # 将笔记添加到对应学科的列表中
        notes[subject].append(note_content)
        # 保存到文件
        save_notes(notes)
        return redirect(url_for('notes_page'))

    return render_template('notes.html', notes=notes, subjects=subjects)


if __name__ == '__main__':
    app.run(debug=True)
