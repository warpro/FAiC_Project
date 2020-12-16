from flask import Flask, render_template, request
import myFunctions as mF
import ratingSystem as rS

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('start-page.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    elif request.method == 'POST':
        w = request.form['Who'].strip()
        if w == "":
            return render_template('main.html')
        else:
            mF.folderCleaner()
            mF.logSaver(w)
            image_src_URLs = mF.imageSearcher(w)
            result_score, result_img_path = rS.ratingImages(image_src_URLs)
            return render_template('result.html', name=w, max_score=result_score, img_path=result_img_path)

@app.route('/information')
def information():
    return render_template('information.html')

if __name__ == "__main__":
    app.run()