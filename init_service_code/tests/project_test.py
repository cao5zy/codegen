import shellrun
from assertpy import assert_that, contents_of

def test_generateProxy():
    from project import generateProxy
    from models.ansible.yamlgen import YamlGenModel

    root = "./test_proxy_gen"
    shellrun.run("mkdir %s" % root)
    model = YamlGenModel(deployRootPath = root, proxyName = "nginx_proxy", \
                         services = [YamlGenModel.Service(name = "service1", type = "microService", ports = ["8080:8080"])])

    try:
        generateProxy(model)
        assert_that("%s/nginx_proxy/logs" % root).exists().is_directory()
        assert_that("%s/nginx_proxy/conf.d" % root).exists().is_directory()
        assert_that("%s/nginx_proxy/conf.d/app.conf" % root).exists()
        content = contents_of("%s/nginx_proxy/conf.d/app.conf" % root)
        assert_that(content).contains("upstream service1 {")
        assert_that(content).contains("server service1:8080")
        assert_that(content).contains("location /_api/service1/")
        assert_that(content).contains("proxy_pass http://service1/")
    finally:
        shellrun.run("rm %s -rf" % root)

    
