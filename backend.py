# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request,render_template, redirect, url_for
from flask_cors import CORS
from fuzzywuzzy import process
import pymysql


app = Flask(__name__,  static_url_path='',
            static_folder='../web/static',
            template_folder='../web/templates')
CORS(app)


shop_list = ['灵海店', '联华超市(新河二店)', '昆山店', '行健店', '紫云店', '华联超市(中兴店) ', '双喜店', '东北店', '联华超市(淞良店)', '飞跃店', '联华超市(惠南店)', '蒋松店', '墅新店', '联华超市(康茂店)', '联华超市(真武店)', '泗建店', '德利店', '清涧店', '外马路店', '博福店', '联华超市(桃浦店)', '东华店', '联华超市(普庆店)', '共芷店', '联华超市(施湾店)', '禺秀店', '联华超市(周浦店)', '联华超市(漕东店)', '联华超市(锦顺店)', '景星店', '青云店', '联华超市(文化店)', '联华超市(川环店)', '淞裕店', '武胜店', '浦光店', '林群店', '联华超市(古北新城店)', '真如店', '洛有店', '宁强店', '长凯店', '新龙店', '邻居店', '文河店', '高台店', '申长店', '联华超市(金月店)', '溧阳店', '联华超市(红亮店)', '康兴店', '盘阳店', '联华超市(唐镇店)', '联华超市(呈汇店)', '申友店', '浦南二店', '海星店', '联华超市(新港二店)', '立立店', '北苑店', '联华超市(永清店)', '军清店', '康沈店', '姚虹店', '外滩店', '临青二店', '青安店', '建工店', '联华超市(联明店)', '联华超市(标树店)', '宜军店', '浦华店', '联华超市(奉浦店)', '正旺店', '联华超市(顾高店)', '翔军店', '国京店', '联华超市(环桥店)', '傅家店', '联华超市(环镇店)', '联华超市(亦园店)', '卓越店', '保德店', '上祁店', '得隆店', '陆铮店', '新客三店', '华联超市(三星店)', '联华超市(芦潮港店)', '联华超市(南亭公路店)', '联华超市(莱阳路)', '联华超市(盛足店)', '浦坊店', '联华超市(操场街店)', '联华超市(中佳店)', '联华超市(西渡店)', '紫荆店', '黄山店', '沈巷店', '辉辉店', '新澳店', '联华超市(航头店)', '加团店', '安俊店', '胜贤店', '联华超市(铁峰店)', '万镇店', '物贸店', '联华超市(奎照路店)', '广楠店', '制造店', '高行店', '俊俊店', '旺鲜店', '向华店', '美香店', '泗泾店', '联华超市(新源店)', '静铁二店', '联华超市(卫清店)', '吾悦店', '桂菁店', '长虎店', '联华超市(古浪店)', '牡兰店', '中华店', '凌空店', '华联超市(崇明供销向化店) ', '联华超市(学前店)', '晨光店', '壹丰店', '兴发店', '联华超市(高桥店)', '丰明店', '联华超市(德祥店)', '联华超市(梅园店)', '华联超市(崇明供销新建店)', '联华超市(真新店)', '联华超市(今辉店)', '和珍店', '联华超市(拱乐店)', '嘉宝店', '南都店', '联华超市(沈巷店)', '联华超市(云汉店)', '唐安店', '天雄店', '仙霞一店', '嘉春店', '联华超市(吴兴店)', '顾唐二店', '联华超市(继业店)', '联华超市(泥城店)', '宜达店', '施湾店', '敏敏店', '功明店', '华联超市(崇明供销竖河店)', '嘉文店', '学府店', '联华超市(西康店)', '联华超市(庙镇店)', '联华超市(菊园店)', '临港店', '灵浦店', '西康店', '江桥店', '联华超市(黄楼店)', '金乐店', '双峰店', '习勤店', '联华超市(松兰路)', '华萍店', '亚一店', '儿科店', '位育店', '莘潭店', '泽丰一店', '浦津店', '亿丰店', '运光店', '联华超市(建中店)', '兄弟店', '联华超市(曹路店)', '历城店', '联华超市(俱进店)', '联华超市(庚诚店)', '静中店', '凉丰店', '双庆店', '方浜店', '联华超市(市台路店)', '联华超市(奕民店)', '延武店', '联华超市(干巷店)', '丰新店', '威海店', '麦家店', '叶榭店', '华联超市(崇明供销合作店)', '虹源店', '联华超市(增惠店)', '瑞丽店', '联华超市(云皓店)', '陈昱店', '联华超市(福海店)', '悦风店', '澳圣店', '潍浦店', '自忠店', '虹嘉店', '联华超市(三林新村店)', '清新店', '联华超市(丰康店)', '联华超市(铜川店)', '联华超市(远洋店)', '行华店', '牡丹店', '新金桥店', '联华超市(南明店)', '万荣店', '联华超市(报春店)', '凇良店', '银貂店', '联华超市(嘉华店)', '东方一店', '联华超市(静安店)', '杨帆店', '和龙店', '龙馨店', '联华超市(罗阳店)', '联华超市(赋欣店)', '联华超市(松辉店)', '联华超市(虹颂店)', '联华超市(果园店)', '航天店', '联华超市(绿杨店)', '肇平店', '联华超市(来发店)', '朱梅店', '联华超市(中科店)', '联华超市(华阴店)', '中通店', '泰迪店', '博德店', '联华超市(丰庄路店)', '万里店', '场镇店', '联华超市(建德店)', '共服店', '联华超市(锦秋新天地店)', '联华超市(川南奉公路)', '汇峰店', '联华超市(客盈店)', '联华超市(荣乐西路店)', '周铁店', '凌河店', '联华超市(松汇店)', '上南一店', '昌盛店', '联华超市(良华店)', '联华超市(宾阳店)', '联华超市(宝馨店)', '联华超市(新育店)', '上实店', '东昌店', '卢胜店', '星漕店', '博渊店', '联华超市(亦诺店)', '联华超市(海潮店)', '华新店', '绿明店', '联华超市(新锦绣店)', '疏影店', '通州店', '泓和店', '行知店', '红松一店', '珠湖路店', '联华超市(瑞金医院店)', '联华超市(巨野店)', '联华超市(特惠店)', '竹柏店', '东绣店', '栖友店', '泽海店', '联华超市(升扬店)', '仙威店', '可由店', '浦泰路店', '联华超市(黄渡店)', '宝豪店', '联华超市(老沪闵路店)', '祯元店', '优诗店', '华联超市(西门二店)', '联华超市(真金店)', '金储店', '彰武店', '联华超市(君庭店)', '好购店', '胜幸店', '金台店', '联华超市(灵泉店)', '南新店', '文盛店', '燕斌店', '浦桃店', '芷通店', '重北店', '联华超市(临江店)', '联华超市(北艾店)', '海英店', '联华超市(水电路二店)', '锦楠店', '联华超市(新浦航店)', '都会店', '如飞店', '青松店', '联华超市(沪泰店)', '联华超市(黄路店)', '联华超市(沈家弄店)', '联华超市(钦州南路店)', '长逸店', '联华超市(坦直店)', '向荣店', '平华店', '鲁周店', '联华超市(宝山路店)', '掌安店', '联华超市(辉平店)', '联华超市(金葵店)', '联华超市(茶陵店)', '大同店', '联华超市(梅陇店)', '连铁店', '联华超市(城中园酒店东南)', '龙南店', '新红店', '轩轩店', '享友店', '联华超市(虹梅南路店)', '联华超市(淞南店)', '联华超市(丁香店)', '联华超市(虹中店)', '联华超市(高迪店)', '长屿店', '大发店', '联华超市(长江店)', '联华超市(汇成店)', '长南店', '比伦店', '慧创店', '联华超市(保屯店)', '连城店', '万顺店', '联华超市(仙霞店)', '联华超市(昆冈店)', '联华超市(雅轩店)', '双城店', '澳门店', '共阳店', '泰州店', '联华超市(航梅店)', '联华超市(云风店)', '联华超市(南丹店)', '真知店', '洁彤店', '联华超市(顺发店)', '联华超市(盐仓店)', '共中店', '林兴店', '岭南店', '政兴店', '联华超市(志丹店)', '联华超市(安亭店)', '联华超市(瓦屑店)', '花山店', '利伟店', '联华超市(平安店)', '伟铭店', '桂林店', '联华超市(竹园店)', '江云店', '联华超市(隽苑店)', '徐泾店', '联华超市(浦益店)', '联华超市(浦东南路店)', '崂山店', '华兰店', '联华超市(新凌桥店)', '联华超市(传梅店)', '艾南店', '伊豪店', '黄渡店', '天道店', '联华超市(万航店)', '超越店', '方红店', '联华超市(百中店)', '尚善店', '联华超市(申浦店)', '联华超市(情谊店)', '联华超市(马陆店)', '联华超市(公利医院店)', '联华超市(御山店)', '联华超市(大华店)', '仁德店', '佳旭店', '天泽店', '延长店', '荣轩店', '金吉店', '新二店', '联华超市(野桥店)', '联华超市(航北路店)', '联华超市(洞宁店)', '沪柳店', '翔贵店', '联华超市(水丰店)', '陶盟店', '华联超市(富民店)', '华佳店', '奇奇店', '联华超市(德园店)', '联华超市(欣跃店)', '联华超市(万川店)', '宏浩店', '中凯店', '培花店', '洛东店', '联华超市(体育馆店)', '福海店', '百联店', '联华超市(盛大花园)', '久华店', '联华超市(文月店)', '博兴店', '闻曲店', '联华超市(三林店)', '福良店', '联华超市(启帆店)', '联华超市(塔城店)', '吉昌店', '联华超市(新凯店)', '宁阳店', '车站店', '南山店', '联华超市(青湖店)', '联华超市(妙栏店)', '瑞丰店', '联华超市(张虹路店)', '上聚店', '王鹰店', '逸香店', '尚泰店', '联华超市(隆安店)', '和宁店', '延吉一店', '平度店', '金塔店', '新凤店', '联华超市(东门店)', '联华超市(柏树店)', '联华超市(新闸路店)', '联华超市(新镇店)', '南方店', '海雁店', '联华超市(千山店)', '永清店', '林嘉店', '联华超市(龙汇店)', '联华超市(翔殷店)', '昆明店', '联华超市(三林远迎店)', '联华超市(莲溪店)', '斜峰店', '玉波店', '阿斌店', '枫梅店', '联华超市(鑫龙店)', '金联店', '联华超市(昌里店)', '联华超市(连波店)', '同铁店', '马当一店', '联华超市(欧阳店)', '联华超市(欣明店)', '肇瑞店', '浦靖店', '成意店', '浦铁店', '联华超市(新国顺店)', '联华超市(甘泉店)', '盛石店', '联华超市(赵中店)', '联华超市(玉麦店)', '俊琦店', '东台一店', '联华超市(东宝店)', '联华超市(锦宁店)', '新市店', '联华超市(余姚路二店)', '武长店', '鲁城店', '联华超市(楼圆店)', '沪栊店', '联华超市(禹州店)', '乐谷店', '联华超市(中港店)', '腾飞店', '联华超市(吴杨东店)', '祥红店', '西村店', '莘都店', '申滨店', '联华超市(共富店)', '惠岭店', '联华超市(新建设店)', '钦北店', '宇辰店', '绿树店', '联华超市(铭诚店)', '晋元店', '景鸿店', '联华超市(雄发店)', '联华超市(洞泾店)', '天顺店', '桂康店', '联华超市(赵屯店)', '联华超市(封浜店)', '阳城店', '新余店', '达东店', '联华超市(施新店)', '联华超市(吕巷店)', '海大店', '南祁店', '兆邦店', '京江店', '宛南店', '襄阳店', '联华超市(崇明崇安店) ', '交暨店', '文杰店', '亭轩店', '联华超市(新沪店)', '联华超市(巍广店)', '中铁店', '联华超市(友谊店)', '隆德店', '吴梅店', '田州店', '景东店', '联华超市(杨园店)', '福元店', '联华超市(闵行店)', '枫丹店', '联华超市(西凌店)', '联华超市(杨光店)', '联华超市(梅川店)', '云雅店', '林佑店', '联华超市(眉州路店)', '联华超市(瞿溪路店)', '柳闵店', '联华超市(富泉店)', '安澜店', '联华超市(上虹东兰店)', '伟莱店', '谭行店', '联华超市(明杰店)', '联华超市(田林五、六、七村北)', '联华超市(海伦店)', '奔达店', '晨蔚店', '怒北店', '联华超市(仓丰店)', '九亭店', '桃浦店', '联华超市(怒江路店)', '百色路店', '公兴店', '联华超市(六团店)', '福利店', '联华超市(凉城店)', '联华超市(柳城店)', '河源店', '联华超市(旭祥店)', '兰陵店', '立升店', '联华超市(芳华店)', '中环一店', '吉安店', '友益店', '联华超市(九亭店)', '联华超市(江浦路店)', '联华超市(联东店)', '联华超市(栖山店)', '联华超市(华高店)', '长隆店', '南中店', '经典店', '唐保店', '联华超市(妙境店)', '联华超市(裕安店)', '煜轩店', '漕庆店', '丽萍店', '联华超市(真大店)', '联华超市(茸盛店)', '联华超市(洪山店)', '联华超市(罗香店)', '联华超市(芦潮店)', '槎溪店', '联华超市(香苑店)', '联华超市(宛南店)', '天虹店', '明祥店', '联华超市(博山店)', '联华超市(百花店)', '同嘉店', '四海店', '漕源店', '联华超市(喜达店)', '金林店', '交真店', '三门店', '天丰店', '联华超市(龙茗店)', '欧银店', '联华超市(北青店)', '新客二店', '平青店', '名都店', '华联超市(崇明供销堡南店) ', '联华超市(陈镇店)', '书平店', '古九店', '联华超市(下南路店)', '卢高店', '国庠店', '联华超市(濠峰店)', '广川店', '联华超市(花山店)', '联华超市(仓汇路)', '大华店', '馨宁店', '泓铭店', '闽缘店', '莘沥店', '瑞宁店', '江文店', '锦江二店', '联华超市(菊盛路店)', '卓凡店', '诚远店', '罗阳店', '运颉店', '方泰店', '顾唐一店', '康西店', '真祁店', '联华超市(延平店)', '马当店', '建韵店', '联华超市(琪惠店)', '仓川店', '世博村店', '伊敏店', '杨行店', '联华超市(航兴店)', '睿濠店', '联华超市(恒大店)', '联华超市(新二店)', '罗星店', '鲁公店', '东泉店', '联华超市(港西店)', '联华超市(上海御桥店)', '金栖店', '宝丰店', '龙凤店', '华联超市(崇明供销大新店)', '博悦店', '商学院店', '侃韵店', '洋磊店', '曲阳店', '同欢店', '联华超市(香花店)', '安波路店', '联华超市(宏启店)', '联华超市(福州店)', '联华超市(松江人民店)', '石龙店', '罗秀店', '捷佳店', '联华超市(南门店)', '宝平店', '嘉汇店', '海鸥店', '金沙店', '华强店', '泉源店', '联华超市(青安店)', '联华超市(华骥店)', '柳营一店', '联华超市(张江店)', '梁波店', '联华超市(张桥店)', '新港店', '联华超市(安顺路)', '联华超市(海盈店)', '中卫店', '快捷店', '天美店', '扶港店', '愚园一店', '上钞店', '华顺店', '沪华店', '复兴店', '联华超市(万荣小区东南)', '平原店', '南祝店', '霍定店', '喜泰店', '联华超市(大宁店)', '嘉苑店', '联华超市(中山桥店)', '鹤闵店', '联华超市(景谷店)', '联华超市(田园店)', '联华超市(交通路)', '西江店', '龙睦店', '医学院店', '台庄店', '浦恒店', '瞿溪店', '淡水店', '凯慧店', '明红店', '长江店', '浦杨店', '加隆店', '联华超市(芝园店)', '四平店', '联华超市(永年店)', '康士店', '贵顺店', '宁欣店', '志成店', '金桂店', '洛场店', '联华超市(北园店)', '口福店', '沧源店', '联华超市(张杨店)', '浦南一店', '联华超市(正阳店)', '联华超市(岭南店)', '联华超市(金杨店)', '欧阳路店', '联华超市(电台店)', '延长一店', '联华超市(文翔店)', '阳保店', '密山店', '阿香店', '长远店', '联华超市(上川店)', '维尼店', '联华超市(芷江店)', '虹铁一店', '娄山店', '佳佳店', '国济店', '罗川店', '永德店', '联学店', '静静店', '谨守店', '天北店', '联华超市(建国西店)', '南方国际店', '联华超市(千星店)', '联华超市(万源店)', '联华超市(虹桥店)', '联华超市(沪杭店)', '联华超市(桂林店)', '联华超市(商榻店)', '延荣店', '联华超市(羽山路)', '井延店', '联华超市(爱博店)', '奇正店', '太原店', '许杨店', '城银店', '联华超市(兴国店)', '联华超市(曙建店)', '西乡店', '华容店', '联华超市(园洲店)', '长泉店', '金闸店', '联华超市(宝峰店)', '联华超市(曹行店)', '共富路店', '淞济店', '联华超市(高设店)(装修中)', '德羽店', '联华超市(平凉店)', '联华超市(长海店)', '四达店', '大连店', '界华店', '大沽店', '发稳店', '联华超市(长阳新苑店)', '场凉店', '联华超市(包头店)', '联华超市(彭浦店)', '滴水湖店', '联华超市(东辉店)', '联华超市(香贵店)', '联华超市(东余杭店)(装修中)', '市东店', '碧泉店', '奎照店', '陕西店', '秀庭店', '联华超市(唐行店)', '莘西店', '沪康店', '陆翔店', '赵兴店', '大康店', '联华超市(曹八店)', '如家店', '梓怡店', '丹徒店', '清源店', '联华超市(花木店)', '联华超市(富民店)', '城基店', '徐虹店', '町畹店', '课植店', '华联超市(崇明供销长江店)', '吉隆店', '联华超市(奉城店)', '维多店', '联华超市(共江店)', '联华超市(峨嵋店)', '宿铁店', '联华超市(百林店)', '政法学院店', '联华超市(万邦店)', '巨杨店', '联华超市(虹古店)', '陈春店', '花花店', '联华超市(永吉路店)', '联华超市(叶红店)', '车纪店', '杨园店', '樱花店', '博辉店', '秣陵店', '逸辉店', '联华超市(裕林店)', '新沪店', '华友店', '少平店', '联华超市(莲花店)', '联华超市(川环南路店)', '联华超市(栖霞店)', '联华超市(漕宝店)', '石屏店', '联华超市(桥梅店)', '黄松店', '联华超市(西郊枫林苑南)', '联华超市(剑龙店)', '联华超市(白鹤店)', '联华超市(鑫宝店)', '旭辉店', '联华超市(原平店)', '漕东店', '联华超市(青赵店)', '联华超市(泾南店)', '联华超市(铭申店)', '联华超市(汇港店)', '联华超市(余庆店)', '安桥店', '海龙店', '联华超市(陆家嘴软件园店)', '浦江店', '金剑店', '广灵店', '民鑫店', '广中店', '物华店', '联华超市(富锦店)', '联华超市(成山店)', '联华超市(菊联店)', '天怡店', '联华超市(长城店)', '俊园店', '广一店', '新胶店', '顾唐三店', '联华超市(张建店)', '联华超市(江桥店)', '卢斜店', '苏州店', '联华超市(沪广店)', '华辉店', '联华超市(临二店)', '联华超市(见面缘店)', '新客一店', '嘉瑞店', '联华超市(华盈店)', '华联超市(崇明供销新河店)', '世博三店', '虬江店', '彬吉店', '星华店', '联华超市(崧雅店)', '大地店', '乳山店', '中姚店', '联华超市(宜君店)', '联华超市(盘古路)', '黄兴店', '金旋店', '凤凤店', '联华超市(名城店)', '凯安店', '联华超市(紫欣店)', '联华超市(浦秀店)', '伟庆店', '国清店', '联华超市(图们店)', '联华超市(百平店)', '联华超市(祥仁店)', '联华超市(翔川店)', '联华超市(华亭店)', '联华超市(堡镇店)', '联华超市(碧海店)', '联华超市(白玉店)', '联华超市(东明路店)', '联华超市(虎山店)', '畹町店', '逸龙店', '鑫超店', '长临店', '华丰店', '兰溪店', '联华超市(晶平店)', '华张店', '联华超市(陆家嘴店)', '联华超市(江农店)', '平福店', '包头路店', '璀璨店', '江川店', '盘古店', '虹漕店', '日晖店', '田田店', '新梅店', '向城店', '联华超市(西门店)', '万秀店', '联华超市(秀沿店)', '生全店', '广福店', '昌南店', '铜阳店', '联华超市(裕丰店)', '联华超市(益江店)', '称乐店', '联华超市(博居店)', '联华超市(广福店)', '江秀店', '南仓店', '华宾店', '联华超市(盛桥店)', '建峰店', '德都店', '联华超市(金山店)', '李晓店', '创顺店', '瓯可店', '联华超市(纪旺店)', '联华超市(铁力店)', '繁霖店', '华鹤店', '联华超市(宝良店)', '佳龙店', '联华超市(安宁路店)', '同盛店', '联华超市(祖冲之路店)', '聿酷店', '向东店', '英华店', '临潼店', '联华超市(新宣桥店)', '七莘店', '联华超市(鹤庆店)', '福城店', '联华超市(曹杨店)', '莘庄店', '黄河店', '忠平店', '方舟店', '美艾店', '师大店', '联华超市(武西店)', '联华超市(天马店)', '吴安店', '民德店', '广东店', '丰祥店', '和田店', '江宁店', '东名店', '联华超市(杰欣店)', '铖量店', '联华超市(国和店)', '联华超市(沧源店)', '广同店', '大统店', '好迪店', '天苑店', '联华超市(府永店)', '长清一店', '上浦店', '联华超市(昌化店)', '场江店', '昊欣店', '华富店', '联华超市(枫泾店)', '广华店', '联华超市(云雅店)', '联华超市(长岛路店)', '繁茂店', '联华超市(四平店)', '联华超市(潼港四村东兴苑北)', '三佳店', '武威店', '七莘路店', '联华超市(碧江路店)']
attr_list = ['地址','区域','电话']

db = pymysql.connect(host="10.141.209.224", user="root", password="sdzh521", db="guns", charset='utf8')
cursor = db.cursor()


@app.route('/search/', methods=['GET'])
def delivey_view():
    question = str(request.args.get('question'))
    print(question)
    ShopRatios = process.extractOne(question, shop_list)
    print(ShopRatios)
    if ShopRatios is not None:
        print(ShopRatios[0])
        shop = ShopRatios[0]
        AttrRatios = process.extractOne(question,attr_list)
        print(AttrRatios)
        if AttrRatios is not None:
            print(AttrRatios[0])
            cursor.execute("SELECT market_tel,market_district,market_address FROM `info_market` where market_name = %s",shop)
            res = cursor.fetchone()
            tel = res[0]
            district = res[1]
            address = res[2]
            print(res)
            if AttrRatios[0]=='地址':
                answer = address
                address = '上海市'+district+address
                src = 'http://localhost:3333/map?address='+address
                return render_template('article2.html',shop=shop,address=address,question=question,district=district,src=src)
            elif AttrRatios[0]=='电话':
                answer = tel
            else:
                answer = district
    return render_template('article5.html',question=question,district=district,tel=tel,address=address,answer=answer,shop=shop)



    # if question.find('全方新桥配送中心的详细地址')!=-1:
    #     return redirect('/article2')
    # elif question.find('联华超市张江店的电话')!=-1:
    #     return render_template('article.html')
    # elif question.find('快客便利店(顾北东路)的订单')!=-1:
    #    return render_template('article3.html')
    # elif question.find('快客便利店(世博源店)距离')!=-1:
    #    return render_template('article4.html')
    # return redirect('/index')


@app.route('/intro', methods=['GET'])
def delivey_intro():
    return render_template('intro.html')


@app.route('/article', methods=['GET'])
def delivey_article():
    return render_template('article.html')


@app.route('/article2', methods=['GET'])
def delivey_article2():
    return render_template('article2.html')


@app.route('/article3', methods=['GET'])
def delivey_article3():
    return render_template('article3.html')


@app.route('/article4', methods=['GET'])
def delivey_article4():
    return render_template('article4.html')


@app.route('/category', methods=['GET'])
def delivey_category():
    return render_template('category.html')


@app.route('/user', methods=['GET'])
def delivey_user():
    return render_template('user.html')


@app.route('/index', methods=['GET'])
def delivey_index():
    return render_template('index.html')


@app.route('/contact', methods=['GET'])
def delivey_contact():
    return render_template('contact.html')


@app.route('/changelog', methods=['GET'])
def delivey_changelog():
    return render_template('changelog.html')


@app.route('/map', methods=['GET'])
def delivey_map():
    address = str(request.args.get('address'))
    return render_template('map.html',address=address)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3333)