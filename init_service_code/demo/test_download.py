from codegen import Download

def test_download():
    url="http://http://130.175.64.9:9008/_api/interface_service"
    download = Download()
    download.getUserName()
    download.getPwd()
    download.getJson(url)
