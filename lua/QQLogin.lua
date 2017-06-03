
cmd('pm clear com.tencent.mobileqq')
cmd('am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity')
sleep(5000)
while (exist{textContains='正在更新数据'}) do
    toast('等待数据更新完成')
    sleep(2000)
end


str = repo({type='Account', status='normal', cate_id=args.repo_cate_id, interval=args.time_limit, limit='1'})
local accounts = dkjson.decode (str).result
while (#accounts == 0) do
    toast('帐号库无帐号数据，等待中')
    str = repo({type='Account', status='normal', cate_id=args.repo_cate_id, interval=args.time_limit, limit='1'})
    accounts = dkjson.decode (str).result
    sleep(30000)
end

