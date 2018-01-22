from jinja2 import Template

class LogModuleGenerator:
    def __init__(self, serviceProject):
        self.__serviceProject = serviceProject

    def gen(self):
        return Template('''(function(global, factory){
    module.exports = factory(require('log4js'));
}(global, function(log4js){
    global.mylogger = global.mylogger || {
	configure:()=>{
	    //asume that the log configuration is stored at /config/logconfig.json
	    log4js.configure( './config/logconfig.json', {reloadSecs:3000});
	    this.logger = log4js.getLogger("{{ name }}");
	},
	info:(val)=>{
	    this.logger.info(val);
	},
	debug:(val)=>{
	    this.logger.debug(val);
	},
	error:(val)=>{
	    this.logger.error(val);
	}
    };

    return global.mylogger;
})
);
 ''').render(name = self.__serviceProject.name)
