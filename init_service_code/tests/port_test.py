from models.port import Port
import demjson
from assertpy import assert_that

def test_port():
    port = Port(demjson.decode('''{
      host: 8322,
      container: 8323
    }'''))

    assert_that(port.host).is_equal_to(8322)
    assert_that(port.container).is_equal_to(8323)
