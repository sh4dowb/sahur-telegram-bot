from telethon import TelegramClient, events, sync
import traceback
import requests
import json
from datetime import datetime
from threading import Lock
from unidecode import unidecode
import random

api_id =  CHANGE_ME
api_hash = 'CHANGE_ME'

client = TelegramClient('sahur_bot', api_id, api_hash)
client.start(bot_token="CHANGE_ME")


sahursoz = open("sahur_sahursoz.txt").read().splitlines()
iftarsoz = open("sahur_iftarsoz.txt").read().splitlines()

# parsed from diyanet.gov.tr
ilceMap = {'akcakale': '9824', 'birecik': '9825', 'bozova': '9826', 'ceylanpinar': '9827', 'halfeti': '9828', 'harran': '9829', 'hilvan': '9830', 'sanliurfa': '9831', 'siverek': '9832', 'suruc': '9833', 'viransehir': '9834', 'cayirova': '9648', 'darica': '9649', 'dilovasi': '9650', 'gebze': '9651', 'kandira': '9652', 'karamursel': '9653', 'kartepe': '17902', 'kocaeli': '9654', 'korfez': '9655', 'baykan': '9835', 'eruh': '9836', 'kurtalan': '9837', 'pervari': '9838', 'siirt': '9839', 'sirvan': '17888', 'araban': '9478', 'gaziantep': '9479', 'islahiye': '9480', 'karkamis': '9481', 'nizip': '9482', 'nurdagi': '9483', 'oguzeli': '9484', 'yavuzeli': '9485', 'ardesen': '9791', 'camlihemsin': '9792', 'cayeli': '9793', 'findikli': '9794', 'hemsin': '9795', 'ikizdere': '9796', 'iyidere': '9797', 'rize': '9799', 'adakli': '17889', 'bingol': '9303', 'karliova': '9304', 'kigi': '9305', 'solhan': '9306', 'yayladere': '9307', 'yedisu': '9308', 'akcakent': '20039', 'akpinar': '9643', 'cicekdagi': '9644', 'kaman': '9645', 'kirsehir': '9646', 'mucur': '9647', 'bahce': '9784', 'duzici': '9785', 'hasanbeyli': '9786', 'kadirli': '9787', 'osmaniye': '9788', 'sumbas': '9789', 'toprakkale': '9790', 'agacoren': '9192', 'aksaray': '9193', 'eskil': '9194', 'gulagac': '9195', 'guzelyurt': '9196', 'sariyahsi': '9197', 'sultanhani': '20069', 'aglasun': '9324', 'bucak': '9326', 'burdur': '9327', 'cavdir': '9328', 'celtikci': '9329', 'golhisar': '9330', 'karamanli': '9331', 'tefenni': '9333', 'yesilova': '9334', 'anamur': '9731', 'bozyazi': '9733', 'camliyayla': '9734', 'erdemli': '9735', 'gulnar': '9736', 'mersin': '9737', 'mut': '9738', 'silifke': '9739', 'tarsus': '9740', 'akseki': '9222', 'alanya': '9224', 'antalya': '9225', 'demre': '9226', 'elmali': '9227', 'finike': '9228', 'gazipasa': '9229', 'gundogmus': '9230', 'ibradi': '9231', 'kas': '9232', 'kemer (burdur)': '3', 'kemer (antalya)': '9233', 'korkuteli': '9234', 'kumluca': '9235', 'manavgat': '9236', 'serik': '9237', 'adana': '9146', 'aladag': '9147', 'ceyhan': '9148', 'feke': '9149', 'imamoglu': '9150', 'karaisali': '9151', 'karatas': '9152', 'kozan': '9153', 'pozanti': '9154', 'saimbeyli': '9155', 'tufanbeyli': '9156', 'yumurtalik': '9157', 'atkaracalar': '9357', 'bayramoren': '9358', 'cankiri': '9359', 'cerkes': '9360', 'ilgaz': '9361', 'kizilirmak': '9362', 'kursunlu': '9363', 'orta': '9364', 'sabanozu': '9365', 'yaprakli': '9366', 'adiyaman': '9158', 'besni': '9159', 'celikhan': '9160', 'gerger': '9161', 'golbasi': '9162', 'kahta': '9163', 'samsat': '9164', 'sincik': '9165', 'tut': '9166', 'cerkezkoy': '9872', 'corlu': '9873', 'ergene': '17904', 'hayrabolu': '9874', 'kapakli': '17905', 'm.ereglisi': '9875', 'malkara': '9876', 'sarkoy': '9878', 'tekirdag': '9879', 'akyaka': '9590', 'arpacay': '9591', 'digor': '9592', 'kagizman': '9593', 'kars': '9594', 'sarikamis': '9595', 'selim': '9596', 'susuz': '17880', 'akcaabat': '9891', 'arakli': '9892', 'arsin': '9893', 'besikduzu': '9894', 'carsibasi': '9895', 'caykara': '9896', 'dernekpazari': '9897', 'duzkoy': '9898', 'hayrat': '9899', 'of': '9901', 'salpazari': '9902', 'surmene': '9903', 'tonya': '9904', 'trabzon': '9905', 'vakfikebir': '9906', 'yomra': '9907', 'abana': '9597', 'agli': '9598', 'arac': '9599', 'azdavay': '9600', 'catalzeytin': '9602', 'cide': '9603', 'daday': '9604', 'devrekani': '17885', 'doganyurt': '9605', 'hanonu': '9606', 'ihsangazi': '9607', 'inebolu': '9608', 'kastamonu': '9609', 'kure': '9610', 'senpazar': '9612', 'seydiler': '17886', 'taskopru': '9613', 'tosya': '9614', 'dargecit': '9723', 'derik': '9724', 'kiziltepe': '9725', 'mardin': '9726', 'mazidagi': '9727', 'midyat': '9728', 'nusaybin': '9729', 'omerli': '9730', 'savur': '17901', 'ahirli': '9656', 'akoren': '9657', 'aksehir': '9658', 'altinekin': '9659', 'beysehir': '9660', 'bozkir': '9661', 'celtik': '9662', 'cihanbeyli': '9663', 'cumra': '9664', 'derbent': '9665', 'derebucak': '9666', 'doganhisar': '9667', 'emirgazi': '9668', 'eregli': '9669', 'guneysinir': '9670', 'hadim': '16704', 'halkapinar': '9671', 'huyuk': '9672', 'ilgin': '9673', 'kadinhani': '9674', 'karapinar': '9675', 'karatay': '17872', 'konya': '9676', 'kulu': '9677', 'meram': '17870', 'sarayonu': '17874', 'selcuklu': '17871', 'seydisehir': '9678', 'taskent': '17873', 'tuzlukcu': '9679', 'yalihuyuk': '9680', 'yunak': '9681', 'akcakoca': '9411', 'cilimli': '9412', 'cumayeri': '9413', 'duzce': '9414', 'golyaka': '9415', 'gumusova': '9416', 'kaynasli': '9417', 'yigilca': '9418', 'akcadag': '9694', 'arapgir': '9695', 'arguvan': '9696', 'darende': '9697', 'dogansehir': '9698', 'doganyol': '9699', 'hekimhan': '9700', 'kuluncak': '9702', 'malatya': '9703', 'puturge': '9704', 'yazihan': '9705', 'agin': '9428', 'alacakaya': '9429', 'aricak': '9430', 'baskil': '9431', 'elazig': '9432', 'karakocan': '9433', 'keban': '9434', 'kovancilar': '9435', 'maden': '9436', 'palu': '9437', 'sivrice': '9438', 'amasya': '9198', 'goynucek': '9199', 'gumushacikoy': '9200', 'hamamozu': '9201', 'merzifon': '9202', 'suluova': '9203', 'tasova': '9204', 'ayancik': '9840', 'boyabat': '9841', 'dikmen': '9842', 'duragan': '9843', 'erfelek': '9844', 'gerze': '9845', 'sarayduzu': '9846', 'sinop': '9847', 'turkeli': '9848', 'alucra': '9486', 'bulancak': '9487', 'camoluk': '9488', 'canakci': '9489', 'dereli': '9490', 'dogankent': '9491', 'espiye': '9492', 'eynesil': '9493', 'giresun': '9494', 'gorele': '9495', 'guce': '9496', 'kesap': '9497', 'piraziz': '9498', 'sebinkarahisar': '16706', 'tirebolu': '9499', 'yaglidere': '9500', 'bursa': '9335', 'buyuk orhan': '9336', 'gemlik': '9337', 'harmancik': '9338', 'inegol': '9339', 'iznik': '9340', 'karacabey': '9341', 'keles': '9342', 'kestel': '17893', 'mudanya': '9343', 'mustafa kemalpasa': '9344', 'orhaneli': '17894', 'orhangazi': '9345', 'yenisehir': '9346', 'askale': '9448', 'aziziye': '9449', 'cat': '9450', 'erzurum': '9451', 'hinis': '9452', 'horasan': '9453', 'ispir': '9454', 'karacoban': '9455', 'karayazi': '9456', 'koprukoy': '9457', 'narman': '9458', 'oltu': '9459', 'olur': '9460', 'pasinler': '9461', 'pazaryolu': '9462', 'senkaya': '9463', 'tekman': '9464', 'tortum': '9465', 'uzundere': '9466', 'aksu (antalya)': '2', 'aksu (isparta)': '9525', 'atabey': '17891', 'egirdir': '9526', 'gelendost': '9527', 'isparta': '9528', 'keciborlu': '9529', 'sarki karaagac': '9530', 'senirkent': '17816', 'sutculer': '9531', 'uluborlu': '9532', 'yalvac': '9533', 'yenisar bademli': '9534', 'cayirli': '9439', 'erzincan': '9440', 'ilic': '9441', 'kemah': '9442', 'kemaliye': '9443', 'otlukbeli': '9444', 'refahiye': '9445', 'tercan': '9446', 'uzumlu': '9447', 'alaca': '9367', 'bogazkale': '9369', 'corum': '9370', 'dodurga': '9371', 'iskilip': '9372', 'kargi': '9373', 'lacin': '9374', 'mecitozu': '9375', 'oguzlar': '9376', 'ortakoy (aksaray)': '7', 'ortakoy (corum)': '9377', 'osmancik': '9378', 'sungurlu': '9379', 'ugurludag': '9380', 'baliseyh': '9631', 'celebi': '9632', 'delice': '9633', 'karakecili': '9634', 'keskin': '17897', 'kirikkale': '9635', 'sulakyurt': '9636', 'ahmetli': '9707', 'akhisar': '9708', 'alasehir': '9709', 'demirci': '9710', 'golmarmara': '9711', 'gordes': '9712', 'kirkagac': '9713', 'koprubasi (trabzon)': '9', 'koprubasi (manisa)': '9714', 'kula': '9715', 'manisa': '9716', 'salihli': '9717', 'sarigol': '9718', 'saruhanli': '9719', 'selendi': '9720', 'soma': '9721', 'turgutlu': '9722', 'akincilar': '9856', 'altinyayla (burdur)': '3', 'altinyayla (sivas)': '9857', 'divrigi': '9858', 'dogansar': '9859', 'gemerek': '9860', 'golova': '9861', 'gurun': '9862', 'hafik': '9863', 'imranli': '9864', 'kangal': '9865', 'koyulhisar': '9866', 'sarkisla': '9867', 'sivas': '9868', 'susehri': '9869', 'ulas': '17920', 'yildizeli': '9870', 'zara': '9871', 'cemisgezek': '9908', 'hozat': '9909', 'nazimiye': '9910', 'pertek': '9912', 'pulumur': '9913', 'tunceli': '9914', 'bolu': '9315', 'dortdivan': '9316', 'gerede': '9317', 'goynuk': '9318', 'kibriscik': '9319', 'mengen': '9320', 'mudurnu': '9321', 'seben': '9322', 'yenicaga': '9323', 'adilcevaz': '9309', 'ahlat': '9310', 'bitlis': '9311', 'guroymak': '17887', 'hizan': '9312', 'mutki': '9313', 'tatvan': '9314', 'afsin': '9571', 'andirin': '9572', 'caglayancerit': '9573', 'ekinozu': '9574', 'elbistan': '9575', 'goksun': '9576', 'kahramanmaras': '9577', 'nurhak': '9578', 'pazarcik': '9579', 'turkoglu': '17908', 'akyazi': '9800', 'geyve': '9801', 'hendek': '9802', 'karasu': '9803', 'kaynarca': '9804', 'kocaali': '9805', 'pamukova': '9806', 'sakarya': '9807', 'tarakli': '9808', 'gumushane': '9501', 'kelkit': '16746', 'kose': '9502', 'kurtun': '9503', 'siran': '9504', 'torul': '9505', 'bartin': '9285', 'kurucasile': '9286', 'ulus': '9287', 'bulanik': '9751', 'haskoy': '9752', 'korkut': '9753', 'malazgirt': '9754', 'mus': '9755', 'varto': '9756', 'banaz': '9915', 'esme': '9916', 'karahalli': '9917', 'sivasli': '9918', 'ulubey': '17909', 'usak': '9919', 'babaeski': '17903', 'demirkoy': '9637', 'kirklareli': '9638', 'luleburgaz': '9639', 'pehlivankoy': '9640', 'pinarhisar': '9641', 'vize': '9642', 'ardahan': '9238', 'cildir': '9239', 'damal': '9240', 'gole': '9241', 'hanak': '9242', 'posof': '9243', 'alapli': '9950', 'caycuma': '9951', 'devrek': '9952', 'gokcebey': '9953', 'karadeniz eregli': '9954', 'zonguldak': '9955', 'ayvalik': '9269', 'balikesir': '9270', 'balya': '9271', 'bandirma': '17917', 'bigadic': '9272', 'burhaniye': '9273', 'dursunbey': '9274', 'erdek': '17881', 'gomec': '9276', 'gonen (ısparta)': '7', 'gonen (balikesir)': '9277', 'havran': '9278', 'ivrindi': '9279', 'kepsut': '9280', 'manyas': '17918', 'marmara': '9281', 'savastepe': '9282', 'sindirgi': '9283', 'susurluk': '9284', 'ayranci': '9584', 'basyayla': '9585', 'ermenek': '9586', 'karaman': '9587', 'kazimkarabekir': '9588', 'sariveliler': '9589', 'altinozu': '9510', 'arsuz': '9515', 'belen': '9511', 'dortyol': '9512', 'erzin': '9513', 'hassa': '9514', 'hatay': '20089', 'iskenderun': '9516', 'kirikhan': '9517', 'kumlu': '9518', 'payas': '17810', 'reyhanli': '9519', 'samandag': '9520', 'yayladag': '16730', 'afyonkarahisar': '9167', 'basmakci': '9168', 'bayat (çorum)': '3', 'bayat (afyonkarahisar)': '9169', 'bolvadin': '9170', 'cay': '9171', 'cobanlar': '9172', 'dazkiri': '9173', 'dinar': '9174', 'emirdag': '9175', 'evciler': '9176', 'hocalar': '9177', 'ihsaniye': '9178', 'iscehisar': '9179', 'kiziloren': '9180', 'sandikli': '9181', 'sinanpasa': '9182', 'suhut': '9183', 'sultandagi': '9184', 'akkus': '9768', 'aybasti': '9769', 'camas': '9770', 'catalpinar': '9771', 'caybasi': '9772', 'fatsa': '9773', 'golkoy': '9774', 'gulyali': '9775', 'gurgentepe': '9776', 'ikizce': '9777', 'kabatas': '9778', 'korgan': '9779', 'kumru': '9780', 'mesudiye': '9781', 'ordu': '9782', 'unye': '9783', 'bilecik': '9297', 'bozuyuk': '9298', 'golpazari': '9299', 'inhisar': '9300', 'osmaneli': '17895', 'pazaryeri': '17896', 'sogut': '9301', 'elbeyli': '9628', 'kilis': '9629', 'musabeyli': '9630', 'polateli': '17907', 'aydintepe': '9294', 'bayburt': '9295', 'demirozu': '9296', 'bismil': '9397', 'cermik': '9398', 'cinar': '9399', 'cungus': '9400', 'dicle': '9401', 'diyarbakir': '9402', 'egil': '9403', 'ergani': '9404', 'hani': '9405', 'hazro': '9406', 'kocakoy': '9407', 'kulp': '9408', 'lice': '9409', 'silvan': '9410', 'aydin': '9252', 'bozdogan': '9253', 'buharkent': '9254', 'cine': '9255', 'didim': '9256', 'germencik': '9257', 'incirliova': '9258', 'karacasu': '9259', 'karpuzlu': '9260', 'kocarli': '9261', 'kosk': '9262', 'kusadasi': '9263', 'kuyucak': '9264', 'nazilli': '9265', 'soke': '9266', 'sultanhisar': '9267', 'yenipazar (bilecik)': '3', 'yenipazar (aydin)': '9268', 'agri': '9185', 'diyadin': '9186', 'dogubeyazit': '9187', 'eleskirt': '9188', 'patnos': '9189', 'taslicay': '9190', 'tutak': '9191', 'akdagmadeni': '9936', 'aydincik (mersin)': '7', 'aydincik (yozgat)': '9937', 'bogazliyan': '9938', 'candir': '9939', 'cayiralan': '9940', 'cekerek': '9941', 'kadisehri': '9942', 'saraykent': '9943', 'sarikaya': '9944', 'sefaatli': '17879', 'sorgun': '9946', 'yenifakili': '9947', 'yerkoy': '9948', 'yozgat': '9949', 'aliaga': '9552', 'bayindir': '9553', 'bergama': '9554', 'beydag': '9555', 'cesme': '9556', 'dikili': '9557', 'foca': '9558', 'guzelbahce': '9559', 'izmir': '9560', 'karaburun': '9561', 'kinik': '9563', 'kiraz': '9564', 'menderes': '17868', 'menemen': '17869', 'odemis': '9565', 'seferihisar': '9566', 'selcuk': '9567', 'tire': '9568', 'torbali': '9569', 'urla': '9570', 'altintas': '9682', 'aslanapa': '9683', 'cavdarhisar': '9684', 'domanic': '9685', 'dumlupinar': '17906', 'emet': '9686', 'gediz': '9687', 'hisarcik': '9688', 'kutahya': '9689', 'pazarlar': '9690', 'saphane': '9691', 'simav': '9692', 'tavsanli': '9693', 'ardanuc': '9244', 'arhavi': '9245', 'artvin': '9246', 'borcka': '9247', 'hopa': '9248', 'kemalpasa (izmir)': '5', 'kemalpasa (artvin)': '20070', 'murgul': '9249', 'savsat': '9250', 'yusufeli': '9251', 'bahcesaray': '9920', 'baskale': '9921', 'caldiran': '9922', 'catak': '9923', 'edremit (balıkesir)': '2', 'edremit (van)': '9924', 'ercis': '9925', 'gevas': '9926', 'gurpinar': '17912', 'muradiye': '9927', 'ozalp': '9928', 'saray (tekirdağ)': '8', 'saray (van)': '9929', 'van': '9930', 'eflani': '9580', 'eskipazar': '17890', 'karabuk': '9581', 'ovacik (tunceli)': '9', 'ovacik (karabuk)': '9582', 'acigol': '9757', 'avanos': '17878', 'hacibektas': '9758', 'kozakli': '9759', 'nevsehir': '9760', 'urgup': '9761', 'altunhisar': '9762', 'bor': '9763', 'camardi': '9764', 'ciftlik': '9765', 'nigde': '9766', 'ulukisla': '9767', 'bodrum': '9741', 'dalaman': '9742', 'datca': '9743', 'fethiye': '9744', 'koycegiz': '9745', 'marmaris': '17883', 'milas': '9746', 'mugla': '9747', 'ortaca': '9748', 'seydikemer': '17884', 'ula': '9749', 'yatagan': '9750', 'bayramic': '9348', 'biga': '9349', 'bozcaada': '9350', 'can': '9351', 'canakkale': '9352', 'ezine': '17882', 'gelibolu': '9353', 'gokceada': '9354', 'lapseki': '9355', 'yenice (karabük)': '5', 'yenice (canakkale)': '9356', 'arnavutkoy': '9535', 'avcilar': '17865', 'basaksehir': '17866', 'beylikduzu': '9536', 'buyukcekmece': '9537', 'catalca': '9538', 'cekmekoy': '9539', 'esenyurt': '9540', 'istanbul': '9541', 'kartal': '9542', 'kucukcekmece': '9543', 'maltepe': '9544', 'pendik': '9545', 'sancaktepe': '9546', 'sile': '9547', 'silivri': '9548', 'sultanbeyli': '9549', 'sultangazi': '9550', 'tuzla': '9551', '19 mayis': '9809', 'alacam': '9810', 'asarcik': '9811', 'atakum': '17911', 'ayvacik (çanakkale)': '3', 'ayvacik (samsun)': '9812', 'bafra': '9813', 'carsamba': '9814', 'havza': '9815', 'kavak': '9816', 'ladik': '9817', 'salipazari': '9818', 'samsun': '9819', 'tekkekoy': '9820', 'terme': '9821', 'vezirkopru': '9822', 'yakakent': '9823', 'akyurt': '9205', 'ankara': '9206', 'ayas': '9207', 'bala': '9208', 'beypazari': '9209', 'camlidere': '9210', 'cubuk': '9211', 'elmadag': '9212', 'evren': '9213', 'gudul': '9214', 'haymana': '9215', 'kahramankazan': '9217', 'kalecik': '9216', 'kizilcahamam': '9218', 'nallihan': '9219', 'polatli': '9220', 'sereflikochisar': '9221', 'beytussebap': '9849', 'cizre': '9850', 'guclukonak': '9851', 'idil': '9852', 'silopi': '9853', 'sirnak': '9854', 'uludere': '9855', 'cukurca': '9506', 'derecik': '20067', 'hakkari': '9507', 'semdinli': '9508', 'yuksekova': '9509', 'alpu': '9467', 'beylikova': '9468', 'cifteler': '9469', 'eskisehir': '9470', 'gunyuzu': '9471', 'han': '9472', 'inonu': '9473', 'mahmudiye': '9474', 'mihaliccik': '9475', 'saricakaya': '17919', 'seyitgazi': '9476', 'sivrihisar': '9477', 'almus': '9880', 'artova': '9881', 'basciftlik': '9882', 'erbaa': '17910', 'niksar': '9883', 'pazar (rize)': '7', 'pazar (tokat)': '9884', 'resadiye': '9885', 'sulusaray': '9886', 'tokat': '9887', 'turhal': '9888', 'yesilyurt (malatya)': '7', 'yesilyurt (tokat)': '9889', 'zile': '9890', 'altinova': '9931', 'armutlu': '9932', 'cinarcik': '9933', 'termal': '9934', 'yalova': '9935', 'akkisla': '9615', 'bunyan': '9616', 'develi': '9617', 'felahiye': '9618', 'incesu': '9619', 'kayseri': '9620', 'ozvatan': '9621', 'pinarbasi (kastamonu)': '6', 'pinarbasi (kayseri)': '9622', 'sarioglan': '9623', 'sariz': '9624', 'tomarza': '9625', 'yahyali': '9626', 'yesilhisar': '9627', 'aralik': '9521', 'igdir': '9522', 'karakoyunlu': '9523', 'tuzluca': '9524', 'edirne': '9419', 'enez': '9420', 'havsa': '9421', 'ipsala': '9422', 'kesan': '9423', 'lalapasa': '9424', 'meric': '9425', 'suloglu': '9426', 'uzunkopru': '9427', 'batman': '9288', 'besiri': '9289', 'gercus': '9290', 'hasankeyf': '9291', 'kozluk': '9292', 'sason': '9293', 'acipayam': '19020', 'babadag': '9382', 'baklan': '9383', 'bekilli': '9384', 'beyagac': '9385', 'bozkurt (kastamonu)': '6', 'bozkurt (denizli)': '9386', 'buldan': '9387', 'cal': '9388', 'cameli': '9389', 'cardak': '9390', 'civril': '9391', 'denizli': '9392', 'guney': '9381', 'honaz': '9393', 'kale (malatya)': '7', 'kale (denizli)': '17899', 'saraykoy': '9395', 'serinhisar': '9396', 'tavas': '17900'}
lower_map = {ord(u'I'): u'ı',ord(u'İ'): u'i'}

cacheLock = Lock()
usercacheLock = Lock()
try:
	cache = json.load(open("sahur_cache.json"))
	usercache = json.load(open("sahur_usercache.json"))
except:
	cache = {}
	usercache = {}


def getvakit(ilceid):
	global cache
	today = str(datetime.now().day)
	try:
		result = cache[ilceid][today]
		return result
	except KeyError:
		cache[ilceid] = {} # invalidate cache since we might be in a new month

	resp = requests.get("https://namazvakitleri.diyanet.gov.tr/tr-TR/"+ilceid+"/ilce-icin-namaz-vakti").text
	days = resp.split('<tbody>')[1].split('</tbody>')[0].split('<tr>')[1:]
	for day in days:
		cols = [x.split('</td>')[0] for x in day.split('<td>')[1:]]
		dom = cols[0].split(' ')[0]
		imsak = cols[1]
		aksam = cols[5]
		if ilceid not in cache:
			cache[ilceid] = {}

		cache[ilceid][dom] = (imsak, aksam)
		with cacheLock:
			cachefn = open("sahur_cache.json","w")
			cachefn.write(json.dumps(cache))
			cachefn.close()

	return cache[ilceid][today]


@client.on(events.NewMessage)
async def handler(event):
	try:
		if not any(event.message.message.startswith(x) for x in ["/sahur","/ezan","/iftar"]):
			return

		try:
			uid = str(event.message.peer_id.user_id)
		except:
			uid = str(event.message.from_id.user_id)


		ilce = ' '.join(event.message.message.split(' ')[1:])
		if ilce == "" and uid not in usercache:
			return await event.respond('İlk kullanım: ```/ezan <sehir veya ilce>```\nŞehiri bir kez girdikten sonra seçiminiz kaydedilir. Sahur ve iftar hatırlatıcısı yakında!')
		elif ilce == "":
			ilce = usercache[uid]

		ilce = unidecode(ilce.translate(lower_map).lower())

		cevaplar = []
		cekhata = False
		for alt in [x for x in ilceMap.keys() if x.startswith(ilce+" (") or x == ilce]:
			try:
				cevaplar.append((alt, getvakit(ilceMap[alt])))
			except:
				cekhata = True

		if len(cevaplar) != 0:
			usercache[uid] = ilce
			with usercacheLock:
				cachefn = open("sahur_usercache.json","w")
				cachefn.write(json.dumps(usercache))
				cachefn.close()

		resp = ""
		for ilce, zamanlar in cevaplar:
			ilceresp = "{}\n".format(ilce.title())
			iftarokunuyor, sahurokunuyor, messageSet = False, False, False
			for i, zaman in enumerate(zamanlar):
				eventtime = datetime.strptime(zaman, "%H:%M")
				eventdt = datetime.combine(datetime.today(), eventtime.time())
				remaining = (eventdt - datetime.now()).total_seconds()

				if i == 0:
					timeresp = f"🌙 Sahur: {zaman} - "
					if remaining < -3600 * (24- 6): # son x saat içindeyse göstermeye ayarla
						remaining += 86400
				else:
					timeresp = f"🍴 İftar: {zaman} - "
					if remaining > 3600 * 13: # son x saat içindeyse göstermeye ayarla
						remaining = -999999

				if remaining > 3600 * 3:
					timeresp += "{:.0f} saat içinde".format(remaining / 3600)
				elif remaining > 3600 * 2:
					timeresp += "{:.1f} saat içinde".format(remaining / 3600)
				elif remaining > 3600:
					timeresp += "{:.0f} saat {:.0f} dk içinde".format(remaining / 3600, remaining % 3600 / 60)
				elif remaining > 180:
					timeresp += "{:.0f} dk içinde".format(remaining / 60)
				elif remaining > 0:
					timeresp += "{:.0f} dk {:.0f} sn içinde".format(remaining / 60, remaining % 60)
				elif remaining > -120:
					timeresp += "OKUNUYOR".format(remaining / 60, remaining % 60)
					if i == 0:
						sahurokunuyor = True
					else:
						iftarokunuyor = True
				elif remaining > -600:
					timeresp += "az önce okundu"
				else:
					continue # son X saate kadar gösterme

				ilceresp += timeresp+"\n"
				messageSet = True

			if not messageSet:
				continue

			resp += ilceresp+"\n"

		if len(cevaplar) == 0 and cekhata:
			resp = "vakitleri alırken bir hata oluştu.."
		elif len(cevaplar) == 0:
			resp = "bu il veya ilçeyi bulamadım"
		elif resp == "":
			resp = "daha yeni yedik..\nyaklaşan bir sahur veya iftar vakti bulunmuyor"
		elif iftarokunuyor:
			resp += "\n\n"+random.choice(iftarsoz)
		elif sahurokunuyor:
			resp += "\n\n"+random.choice(sahursoz)

		await event.reply(resp)
	except:
		traceback.print_exc()

client.loop.run_forever()
