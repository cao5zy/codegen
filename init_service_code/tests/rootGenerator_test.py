from models.ansible.rootGenerator import getEntriesFromFile, getIncludes
from assertpy import assert_that
from Runner import Run

def test_getEntriesFromFile():
    easyrun.run('mkdir test_folder')
    easyrun.run('echo "hello {{ name1 }}{{ name2 }}" >> test_folder/test.yml')

    result = getEntriesFromFile("test_folder/test.yml")
    print(result)
    assert_that(result).contains("name1")
    assert_that(result).contains("name2")

    easyrun.run("rm test_folder -rf")
    

def test_getIncludes():
    Run.command('mkdir test_folder')
    Run.command('echo "hello {{ name1 }}" >> test_folder/test.yml')
    Run.command('touch test_folder/test.txt')

    result = getIncludes("test_folder")
    print(result)
    assert_that(result).is_length(1).contains("test.yml")
    
    Run.command("rm test_folder -rf")


    
