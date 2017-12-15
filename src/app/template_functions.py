from jinja2 import Template
import time


def render_index():
    template = Template('index.html')
    template.add_template_global(time.time(), name='t')
    return render_template(template)
