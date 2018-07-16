var page = require('webpage').create();
var address = 'https://w.mail.qq.com/';//填写需要打印的文件位置
var output = './screen.png';//存储文件路径和名称
page.viewportSize = { width: 1280, height: 800 };//设置长宽
var x = document.getElementsByClassName("ke-content");
var byId = document.getElementById("ds");
document.getElementsByTagName()
byId.value();
var y =  setMailEditorContentHtml("<h1>Hello</h1>Hello");
var flag = phantom.addCookie({
        "domain": "w.mail.qq.com",
        "expires": "Fri, 01 Jan 2038 00:00:00 GMT",
        "expiry": 2145916800,
        "httponly": false,
        "name": "mpwd",
        "path": "/",
        "secure": false,
        "value": "'E9EF906C2F3E8FFCFAC4E531E46321F026B972A3838BE7E6FB534CEA71F467AA@2156209417@4'" //这里省略了，输入自己的value即可
});



console.log(flag);

if(flag){
    page.open(address, function (status) {
        if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit();
        } else {
        window.setTimeout(function () {
            page.render(output);
            phantom.exit();
        }, 500);
        }
    });
}else{
        console.log('error!!!');
}
// "Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)"
// import win32clipboard as w
// import win32con

// #获取剪切板内容
// def gettext():
//     w.OpenClipboard()
//     t = w.GetClipboardData(win32con.CF_TEXT)
//     w.CloseClipboard()
//     return t
//
// #写入剪切板内容
// def settext(aString):
//     w.OpenClipboard()
//     w.EmptyClipboard()
//     w.SetClipboardData(win32con.CF_TEXT, aString)
//     w.CloseClipboard()