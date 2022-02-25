from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def main_page():
    return app.send_static_file('page.html')


@app.route('/<post_title>')
def post(post_title):
    post_titles_file = open('text_files/post_titles.txt', 'r', encoding = 'utf-8')
    post_titles = post_titles_file.readlines()
    post_titles_file.close()

    for element in post_titles:
        if element[:-1] == post_title:
            return app.send_static_file(element[:-1] + '.html')
    if post_title != 'form-page':
        return '404 NOT FOUND', 404


@app.route('/form-page', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return app.send_static_file('form-page.html')

    elif request.method == 'POST':
        posts_file = open('text_files/posts.txt', 'r', encoding = 'utf-8')
        posts = posts_file.read()
        posts_file.close()

        posts_file = open('text_files/posts.txt', 'w', encoding = 'utf-8')
        posts_file.write(str(int(posts) + 1))
        posts_file.close()

        post_titles_file = open('text_files/post_titles.txt', 'a', encoding = 'utf-8')
        post_titles_file.write('page' + str(int(posts) + 1) + '\n')
        post_titles_file.close()

        post_titles_file = open('text_files/post_titles.txt', 'r', encoding = 'utf-8')
        post_titles = post_titles_file.readlines()
        post_titles_file.close()

        page_file = open('static/page.html', 'r', encoding = 'utf-8')
        page = page_file.readlines()
        page_file.close()

        new_page_title = post_titles[-1][:-1]
        page_file = open('static/page.html', 'w', encoding = 'utf-8')
        for line in page:
            page_file.write(line)
            if line == '                <h3>آخرین مطالب</h3>\n':
                page_file.write('                <li><a href="' + new_page_title + '">' + request.form[
                    'Title'] + '</a></li>\n')
        page_file.close()

        page_file = open('static/page.html', 'r', encoding = 'utf-8')
        page = page_file.readlines()
        page_file.close()

        new_page = open('static/' + new_page_title + '.html', 'w', encoding = 'utf-8')
        for line in page:
            if line == '    <a class="active" href="/">صفحه اصلی</a>\n':
                new_page.write('    <a href="/">صفحه اصلی</a>')
            elif line == '                <li><a href="' + new_page_title + '">' + request.form[
                    'Title'] + '</a></li>\n':
                new_page.write('                <li><a class="active" href="' + new_page_title + '">' + request.form[
                    'Title'] + '</a></li>\n')
            else:
                new_page.write(line)
                if line == '    <div class="leftcolumn">\n':
                    new_page.write('        <div class="post">\n')
                    new_page.write('            <h3>' + request.form["Title"] + '</h3>\n')

                    new_page.write('            ')
                    for char in request.form['Content']:
                        new_page.write(char)
                        if char == '\n':
                            new_page.write('            ')
                    new_page.write('        </div>\n')
        new_page.close()

        for element in post_titles[:-1]:
            old_page_file = open('static/' + element[:-1] + '.html', 'r', encoding = 'utf-8')
            old_page = old_page_file.readlines()
            old_page_file.close()

            old_page_file = open('static/' + element[:-1] + '.html', 'w', encoding = 'utf-8')
            for line in old_page:
                old_page_file.write(line)
                if line == '                <h3>آخرین مطالب</h3>\n':
                    old_page_file.write('                <li><a href="' + new_page_title + '">'
                                        + request.form['Title'] + '</a></li>\n')
            old_page_file.close()

        return '<p>مطلب جدید با موفقیت اضافه شد.</p><a href="/">بازگشت به صفحه اصلی</a>'


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 1004, debug = True)
