import time
from flask import Flask, Response, render_template_string
from flask import stream_with_context

app = Flask(__name__)

@app.route("/")
def server_1():
    def generate_output():
        age = 0
        template = '<p>{{ name }} is {{ age }} seconds old.</p>'
        context = {'name': 'bob'}
        while True:
            context['age'] = age
            yield render_template_string(template, **context)
            time.sleep(5)
            age += 5
    return Response(stream_with_context(generate_output()))

app.run()

"""
def g():
    for i, c in enumerate("hello" * 10):
        print i
        print c
        time.sleep(.1)  # an artificial delay
        yield i, c


for i, c in enumerate("hello" * 10):
    print i
    print c
"""
