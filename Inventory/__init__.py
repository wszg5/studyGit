# coding:utf-8
import urllib2
import json


class Inventory:

    def __init__(self):

        self.headers = {'Content-Type': 'application/json'}

        self.field = set(['phone', 'qq', 'sex', 'email', 'qq_nickname', 'province', 'city', 'district', 'real_name', 'birth', 'school', 'gmt_created', 'gmt_modified',
                          'is_deleted', 'x_01', 'x_02', 'x_03', 'x_04', 'x_05', 'x_06', 'x_07', 'x_08', 'x_09', 'x_10', 'x_11','x_12', 'x_13', 'x_14','x_15', 'x_16',
                          'x_17', 'x_18', 'x_19', 'x_20', 'x_21', 'x_22', 'x_23', 'x_24', 'x_25', 'x_26', 'x_27', 'x_28', 'x_29', 'x_30', 'x_31', 'x_32', 'x_33', 'x_34',
                          'x_35', 'x_36', 'x_37' , 'x_38', 'x_39', 'x_40', 'x_41', 'x_42', 'x_43', 'x_44', 'x_45', 'x_46', 'x_47', 'x_48', 'x_49', 'x_50', 'x_51', 'x_52',
                          'x_53', 'x_54', 'x_55', 'x_56', 'x_57', 'x_58', 'x_59', 'x_60', 'x_61', 'x_62', 'x_63', 'x_64', 'x_65', 'x_66', 'x_67', 'x_68', 'x_69', 'x_70',
                          'x_71', 'x_72', 'x_73', 'x_74', 'x_75', 'x_76', 'x_77', 'x_78', 'x_79', 'x_80', 'x_81', 'x_82', 'x_83', 'x_84', 'x_85', 'x_86', 'x_87', 'x_88',
                          'x_89', 'x_90', 'x_91', 'x_92', 'x_93', 'x_94', 'x_95', 'x_96', 'x_97', 'x_98', 'x_99'])


    def postData(self,para):

        keys = para.keys()
        for i in range(0,len(keys)):
            if keys[i] not in self.field :
                return keys[i]

        url = 'http://1.210.zunyun.net/api.php?ac=put'

        request = urllib2.Request(url=url, headers=self.headers, data=json.dumps(para))

        response = urllib2.urlopen(request)
        data = response.read()
        data = json.loads(data)

        return data['success']



if __name__ == '__main__':
    inventory = Inventory()

    para = {"sex":"1","x_01":"a66669ea","qq_nickname":"qq_nickname","x_03":"3333a66669ea", "phone":13234104557}

    con = inventory.postData(para)

    print (con)

