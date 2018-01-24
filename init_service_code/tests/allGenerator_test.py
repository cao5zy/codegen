from models.ansible.allGenerator import sortByDependency, getDependencies
from assertpy import assert_that

def test_sortByDependency():
    target = [{"project":"a", "dependencies": ["b", "c"]},
              {"project": "b", "dependencies": ["c"]},
              {"project": "c", "dependencies": None}]

    result = sortByDependency([], target)

    assert_that(result).is_equal_to(["c", "b", "a"])

def test_getDependencies():
    target = [{"deployConfig":{"name":"a"}, "dependedServers": [{"name":"b"}, {"name":"c"}]},
              {"deployConfig":{"name":"b"}, "dependedServers": [{"name":"c"}]},
              {"deployConfig":{"name":"c"}}
              
    ]

    result = getDependencies(target)

    assert_that(result).contains({"project": "a", "dependencies": ["b", "c"]})
    assert_that(result).contains({"project": "b", "dependencies": ["c"]})
    assert_that(result).contains({"project": "c", "dependencies": None})    
