# # #漂流瓶
                    # for i in range(0,6):
                    #     driver.find_element_by_xpath('/html/body/div/section[1]/div/ul/li[4]/a/span[2]/span[1]').click()
                    #     driver.find_element_by_xpath('//*[@id="ct"]/div[2]/a[1]/span[1]').click()
                    #     driver.find_element_by_xpath('//*[@id="bottlelist"]/ul/li[1]/a/div/span').click()
                    #     driver.find_element_by_xpath('//*[@id="multy_select"]').click()
                    #     driver.find_element_by_xpath('//*[@id="multy_select"]').send_keys(Keys.SHIFT, Keys.TAB, Keys.SHIFT,message2)
                    #     driver.find_element_by_xpath( '//*[@id="multy_select"]' ).click( )
                    #     driver.find_element_by_xpath('//*[@id="postform"]/div[2]/div/div[3]/div/div/input').click()
                    #     if "您的漂流瓶已漂向大海！" in driver.page_source.encode("utf-8"):
                    #         continue
                    #     else:
                    #         break
# #PC 贺卡
                # flag = True
                # while flag:
                #     args = self.getArgs( "4" )
                #     repo_material_cateId2 = args["repo_material_cateId2"]
                #     repo_material_cateId = args["repo_material_cateId"]
                #     emailType = args["emailType"]
                #     repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                #     sendNumbers = self.repo.GetNumber( repo_number_cate_id, 0, 1 )
                #     if len( sendNumbers ) == 0:
                #         print u"%s号仓库没有数据" % repo_number_cate_id
                #         break
                #     else:
                #         sendNumber = sendNumbers[0]["number"]
                #     if repo_material_cateId == "" or repo_material_cateId is None:
                #         selectContent1 = ""
                #         print u"4号任务没有选择主题仓库即没有选择贺卡编号"
                #         Material = self.repo.GetMaterial( "441", 0, 1 )
                #         if len( Material ) == 0:
                #             cardIds = [99917, 99918, 99920, 99921, 99922, 99923, 99924, 99925, 99926, 99927, 99928,
                #                        99929]
                #             cardId = cardIds[random.randint( 0, len( cardIds ) - 1 )]
                #         else:
                #             cardId = Material[0]['content']
                #
                #     else:
                #         Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                #         if len( Material ) == 0:
                #             print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                #             # print u'close09'
                #             if len( Material ) == 0:
                #                 cardIds = [99917, 99918, 99920, 99921, 99922, 99923, 99924, 99925, 99926, 99927, 99928,
                #                            99929]
                #                 cardId = cardIds[random.randint( 0, len( cardIds ) - 1 )]
                #         else:
                #             cardId = Material[0]['content']
                #     if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                #         selectContent2 = ""
                #         print u"4号任务没有选择内容仓库即没有选择贺卡内容"
                #         break
                #
                #     else:
                #         Material = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                #         if len( Material ) == 0:
                #             print u"%s  号仓库为空，没有取到消息" % repo_material_cateId2
                #             # print u'close09'
                #             break
                #         else:
                #             message2 = Material[0]['content']
                #
                #     if "@" not in sendNumber:
                #         if emailType == "QQ邮箱":
                #             sendNumber2 = sendNumber + "@qq.com;"
                #         elif emailType == "189邮箱":
                #             sendNumber2 = sendNumber + "@189.cn;"
                #         elif emailType == "139邮箱":
                #             sendNumber2 = sendNumber + "@139.com;"
                #         elif emailType == "163邮箱":
                #             sendNumber2 = sendNumber + "@163.com;"
                #         elif emailType == "wo邮箱":
                #             sendNumber2 = sendNumber + "@wo.cn;"
                #         else:
                #             sendNumber2 = sendNumber + "@qq.com;"
                #     else:
                #         sendNumber2 = sendNumber + ";"
                #     # driver.find_element_by_xpath('/html/body/div/section[1]/div/ul/li[9]/a/span[2]/span').click()
                #     #
                #     # driver.find_element_by_xpath('//*[@id="ct"]/div[3]/div[%s]/div/div[3]/a'%random.randint(1,4)).click()
                #     cardUrl = "https://mail.qq.com/cgi-bin/frame_html?t=newwin_frame&sid="+ sid2 +"&url=/cgi-bin/cardlist?s=%26t=compose_card%26cardid="+cardId+"%26bccsingle=%26ListType=OneCard%26rpycard=%26p=0%26Cate1Idx=hot%26bccs=%26birthCard="
                #     driver.get( cardUrl )
                #     time.sleep(5)
                #     # sendNumber = "2351382894@qq.com"
                #     try:
                #         driver.switch_to_frame('mainFrame')
                #     except:
                #         pass
                #     driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[3]/input' ).send_keys( sendNumber2 )
                #     # driver.find_element_by_xpath( '//*[@id="content"]' ).send_keys( Keys.CONTROL, 'a', Keys.DELETE )
                #     driver.find_element_by_xpath( '//*[@id="content"]' ).send_keys("\n","\n", message2 )
                #     driver.find_element_by_xpath( '//*[@id="frm"]/div[4]/a[1]' ).click( )
                #     time.sleep( 6 )
                #     # try:
                #     #     driver.switch_to_default_content()
                #     #     page_source = driver.page_source.encode( "utf-8" )
                #     # except:
                #     #     page_source = driver.page_source.encode( "utf-8" )
                #
                #     page_source = driver.page_source.encode("utf-8")
                #     if "您的贺卡已发送" in page_source and "验证码" not in page_source:
                #         print u"%s 发送成功 给 %s ," % (QQNumber, sendNumber2)
                #         count = 0
                #     else:
                #         try:
                #             driver.switch_to_default_content( )
                #             page_source = driver.page_source.encode( "utf-8" )
                #         except:
                #             page_source = driver.page_source.encode( "utf-8" )
                #         print u"%s 发送失败 给%s" % (QQNumber, sendNumber2)
                #         if "贺卡" in page_source and "收件人：" in page_source:
                #             print u"还在当前页面"
                #
                #         try:
                #             self.repo.UpdateNumberStauts( sendNumber, repo_number_cate_id, "normal" )
                #             # driver.get(
                #             #     "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                #             #     emailnumber, repo_number_cate_id, "normal"))
                #         except:
                #             pass
                #         flag = False
                #         if "邮件中可能包含不合适的用语或内容" in page_source:
                #             # 需要解锁
                #             print u"%s  邮件中可能包含不合适的用语或内容" % QQNumber
                #             self.repo.BackupInfo( repo_cate_id, 'exception', QQNumber, '', '' )
                #             # driver.get(
                #             #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                #             #         repo_cate_id, "exception", QQNumber, "", ""))
                #             path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                #                 repo_cate_id, "exception", QQNumber, "", "")
                #             conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                #             conn.request( "GET", path )
                #             time.sleep( 3 )
                #             # driver.delete_all_cookies()
                #         elif "<html><head></head><body></body></html>" in page_source:
                #             print "%s  空" % QQNumber
                #             # driver.delete_all_cookies( )
                #             # self.ipChange.ooo()
                #             # self.ipChange.ooo()
                #         elif "验证码" in page_source:
                #             flagFirst = True
                #             flag = True
                #             print u"%s  需要验证码" % QQNumber
                #             count = count + 1
                #             if count >= 3:
                #                 flag = False
                #                 count = 0
                #         elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                #             print u"%s  您发送的邮件已经达到上限，请稍候再发" % QQNumber
                #             # driver.delete_all_cookies()
                #             # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                #             #   repo_cate_id, "exception", QQNumber, "", "")
                #             # conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                #             # conn.request("GET", path)
                #             # time.sleep(3)
                #         elif "垃圾邮件" in page_source:
                #             print u"垃圾邮件"
                #             flag = True
                #             count = count + 1
                #             if count >= 3:
                #                 flag = False
                #                 count = 0
                #         elif "您的域名邮箱账号存在异常行为" in page_source:
                #             # driver.delete_all_cookies( )
                #             print u"您的域名邮箱账号存在异常行为"
                #             self.updateAccountStatus( repo_cate_id, QQNumber, "exception" )
                #             # driver.get("http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                #             #     repo_cate_id, "exception", QQNumber, "", ""))
                #             # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                #             #    repo_cate_id, "exception", QQNumber, "", "")
                #             # conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                #             # conn.request("GET", path)
                #             # time.sleep(3)
                #             self.updateAccountStatus( repo_cate_id, QQNumber, "exception" )
                #         elif "您的帐号存在安全隐患" in page_source:
                #             # driver.delete_all_cookies( )
                #             print u"您的帐号存在安全隐患"
                #             # self.repo.BackupInfo(repo_cate_id, 'exception', QQNumber, '', '')
                #             # driver.get(
                #             #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                #             #         repo_cate_id, "frozen", QQNumber, "", ""))
                #             self.updateAccountStatus( repo_cate_id, QQNumber, "frozen" )
                #         else:
                #             flag = False
                #             driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                #             print u"%s  该情况没判断出来" % QQNumber
                #             # driver.delete_all_cookies( )
                #             # self.ipChange.ooo()
                #             # self.ipChange.ooo()
                #             time.sleep( 5 )