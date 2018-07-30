# coding:utf-8
from uiautomator import  Device as d
import  unittest ,os ,ddt ,time
from uiautomator import  HTMLTestRunner

data= [{'username': 15964636199, 'password': '111111'}, {'username': 15964636199, 'password': 'liwanlei'},
        {'username': 15964636199, 'password': 'liwanlei123'}]


def assert_i(cm):
    if cm.exists:
        return True
    else:
        return False


@ddt.ddt
class TestaixuetangCase( unittest.TestCase ):
    def setUp(self):
        cmd = 'adb shell am  start   com.aixuetang.teacher/.activities.LoginActivity '
        os.system( cmd )

    def tearDown(self):
        cmd = 'adb shell am force-stop com.aixuetang.teacher'
        os.system( cmd )

    @ddt.data( *data )
    def testlogin(self, data):
        d( resourceId='com.aixuetang.teacher:id/et_username' ).set_text( data['username'] )
        d( resourceId='com.aixuetang.teacher:id/et_password' ).set_text( data['password'] )
        d( resourceId='com.aixuetang.teacher:id/tv_login' ).click( )
        assert_m = assert_i( cm=d( resourceId='com.aixuetang.teacher:id/tv_login' ) )
        self.assertTrue( assert_m )


if __name__ == '__main__':
    suite = unittest.TestSuite( )
    now = time.strftime( '%Y-%m%d', time.localtime( time.time( ) ) )
    report_dir = r'%s.html' % now
    suite.addTests( unittest.TestLoader( ).loadTestsFromTestCase( TestaixuetangCase ) )
    re_open = open( report_dir, 'wb' )
    runner = HTMLTestRunner.HTMLTestRunner( stream=re_open, title='爱学堂demo by uiautomator', description='测试结果' )
    runner.run( suite )
