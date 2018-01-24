import os
import npm
import easyrun
from assertpy import assert_that, contents_of
import util

def test_applyTemplate():
    templatefile = "template"
    target = "template.target"
    obj = {"name": "alan"}
    
    easyrun.run('echo "hello {{ name }}" >> %s' % templatefile)
    util.applyTemplate(templatefile, target, obj)

    contents = contents_of(target)
    assert_that(contents).contains("hello alan")
    
    easyrun.run('rm %s' % templatefile)
    easyrun.run('rm %s' % target)
    # targetPath has the content

def test_installpackageByConfig():
    print('test installpackageByConfig')
    
    template = "templates/package.json.template"
    folder = "testfolder"
    target = "%s/package.json" % folder

    easyrun.run('mkdir %s' % folder)
    
    util.applyTemplate(template, target, { "name": "test service" })

    npm.installpackageByConfig('%s/%s' % (os.getcwd(), folder), [{ "name": "seneca", "option":"--save"}])

    assert_that('%s/node_modules' % folder).exists()
    assert_that('%s/node_modules' % folder).is_directory()
    
    easyrun.run('rm %s/ -rf' % folder)

def test_getPackageNames():
    datafile = "datafile"
    easyrun.run('''echo "[{\"name\":\\"seneca\\", \"option\":\\"--save\\"}]" >> %s'''% datafile)
    data = npm.getPackageNames(datafile)
    assert_that(data).is_not_none()
    assert_that(data).is_type_of(list)
    assert_that(data).is_length(1)
    assert_that(data[0]).contains_entry({"name":"seneca"})
    assert_that(data[0]).contains_entry({"option":"--save"})

    easyrun.run("rm %s" % datafile)
