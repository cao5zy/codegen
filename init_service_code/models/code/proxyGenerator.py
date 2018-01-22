from jinja2 import Template

class ProxyGenerator:
    def __init__(self, serviceProject):
        def gen():
            return Template('''

(function (global, factory) {
    module.exports = factory();
}(global, function () {

    function proxy() {}

    proxy.prototype = {
        {% for name in names %}
            {{name}}:function(){
            return null;
        }{% if not loop.last %},{% endif %}

        {% endfor %}
    };

    return new proxy();
}));

 ''').render(names = map(lambda method:method.name, serviceProject.serviceInterface.methods) \
             if serviceProject.serviceInterface and serviceProject.serviceInterface.methods \
             else [])


        self.gen = gen
    
