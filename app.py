from flask import Flask, render_template
app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    return 'Hello World!'

@app.route('/jennie')
def jennie():
    return render_template('jennie.html')

@app.route('/veivask')
def veivask():
    return render_template('veivask.html')

if __name__ == '__main__':
    app.run()
