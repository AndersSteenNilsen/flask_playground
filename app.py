from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    return 'Hello World!'


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/index')
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("all_links.html", links=links)


@app.route('/jennie')
def jennie():
    return render_template('jennie.html')


@app.route('/veivask')
def veivask():
    return render_template('veivask.html')


if __name__ == '__main__':
    app.run()
