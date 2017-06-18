function QQLogin()
  cmd('pm clear com.tencent.mobileqq')
  cmd('am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity')
  str = repo({type='Account', status='normal', cate_id=args.repo_cate_id, interval=args.time_limit, limit='1'})
  local accounts = dkjson.decode (str).result
  while (#accounts == 0) do
      toast('帐号库无帐号数据，等待中')
      str = repo({type='Account', status='normal', cate_id=args.repo_cate_id, interval=args.time_limit, limit='1'})
      accounts = dkjson.decode (str).result
      sleep(30000)
  end
  local account = accounts[1]
  sleep(5000)

  while (exist{textContains='正在更新数据'}) do
      toast('等待数据更新完成')
      sleep(2000)
  end

  click({resourceId='com.tencent.mobileqq:id/btn_login'})
  sleep(2000)
  set_text(account.number, {className='android.widget.EditText', index='0'})
  set_text(account.password, {resourceId='com.tencent.mobileqq:id/password'})

  click({resourceId='com.tencent.mobileqq:id/login'})
  while (exist{text='登录中'}) do
      sleep(2000)
  end

  if (exist{text='QQ'})  then
      click({text='QQ'})
      if (exist{text='仅此一次'})  then
          click({text='仅此一次'})
      end
  end
  --此处需要验证码
  code = {}
  for i=1, 10 , 1 do
    if (exist({resourceId='com.tencent.mobileqq:id/name', index='2',className="android.widget.EditText"})) then
        toast('第'..i..'次打码，最多尝试10次')
        verify_error(code.id)
        code = verify_code({resourceId='com.tencent.mobileqq:id/name', className='android.widget.ImageView'})
        set_text(code.code, {resourceId='com.tencent.mobileqq:id/name', index='2',className="android.widget.EditText"})
        click({text='完成', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText'})
        sleep(6000)
        while exist({className='android.widget.ProgressBar',index='0'}) do --网速不给力时，点击完成后仍然在加载时的状态
            sleep(2000)
        end
        sleep(2000)
        if not exist({text='输入验证码',resourceId='com.tencent.mobileqq:id/ivTitleName'}) then
           break
        end
    end
  end

  if (exist({text='搜索', resourceId='com.tencent.mobileqq:id/name'})) then
    return true
  end
  if (exist({text='帐号无法登录'}) or exist({text='登录失败'}) or exist({textContains='密码错误'}) ) then
    return false
  end
  return true
end

for i=1, 10 , 1 do
  toast('第'..i..'次QQ登录，最多尝试10次')
  if (QQLogin()) then
    break
  end
end


