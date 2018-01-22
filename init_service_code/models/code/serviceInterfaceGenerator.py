from jinja2 import Template

class ServiceInterfaceGenerator:
    def __init__(self, serviceInterface):
        def getServiceName():
            return serviceInterface.name
        
        def getTestCode():
            return Template('''
                this.add({test:"hello-world"}, (msg, respond)=>{
                    respond("hello world from {{serviceName}}", null);
                });

 ''').render(serviceName = getServiceName())

        
        def gen():


            template = '''
    (function (global, factory) {
        module.exports = factory(require('./proxy'));
    }(global, function (proxy) {

        function {{serviceName}}() { 
            {% for method in service.methods %}
                this.add({ {% for p in method.params if p.isUrlFilter %}{{p.name}}:"{{p.defaultVal}}" {%if not loop.last %},{%endif%}{% endfor %} }, (msg, respond)=>{
                    proxy.{{ method.name }}(msg, res=>{
                        respond(null, res);
                    });
                });
            {% endfor %}
            {{ testcode }}
         } 

        return {{ serviceName }};
    }));

    '''

            return Template(template).render(service = serviceInterface, \
                                             serviceName = getServiceName(),\
                                             testcode = getTestCode())    

        self.gen = gen
