sequencias= ['/data/videos/4k/Beauty_3840x2160_120fps_420_10bit_YUV.yuv'
,'/data/videos/1080p/BasketballDrive_1920x1080_50.yuv'
,'/data/videos/1600p/NebutaFestival_2560x1600_60_10bit_crop.yuv'
,'/data/videos/720p/FourPeople_1280x720_60.yuv'
,'/data/videos/4k/Bosphorus_3840x2160_120fps_420_10bit_YUV.yuv'
,'/data/videos/1080p/BQTerrace_1920x1080_60.yuv'
,'/data/videos/1600p/PeopleOnStreet_2560x1600_30.yuv'
,'/data/videos/720p/Johnny_1280x720_60.yuv'
,'/data/videos/4k/Cactus_3840x2160_60fps.yuv'
,'/data/videos/1080p/Cactus_1920x1080_50.yuv'
,'/data/videos/1600p/SteamLocomotiveTrain_2560x1600_60_10bit_crop.yuv'
,'/data/videos/720p/KristenAndSara_1280x720_60.yuv'
,'/data/videos/4k/Coastguard_3840x2160_60fps.yuv'
,'/data/videos/1080p/CrowdRun_1920x1080_25.yuv'
,'/data/videos/1600p/Traffic_2560x1600_30.yuv'
,'/data/videos/720p/SlideEditing_1280x720_30.yuv'
,'/data/videos/4k/Foreman_3840x2160_60fps.yuv'
,'/data/videos/1080p/Kimono1_1920x1080_24.yuv'
,'/data/videos/720p/SlideShow_1280x720_20.yuv'
,'/data/videos/4k/HoneyBee_3840x2160_120fps_420_10bit_YUV.yuv'
,'/data/videos/1080p/ParkScene_1920x1080_24.yuv'
,'/data/videos/1080p/Tennis_1920x1080_24.yuv'
,'/data/videos/4k/Jockey_3840x2160_120fps_420_10bit_YUV.yuv'
,'/data/videos/4k/Mobile_3840x2160_60fps.yuv'
,'/data/videos/4k/News_3840x2160_60fps.yuv'
,'/data/videos/4k/RadySetGo_3840x2160_120fps_420_10bit_YUV.yuv'
,'/data/videos/4k/RollerCoaster_4096x2160_60fps_10bit_420_jvet.yuv'
,'/data/videos/4k/ShakeNDry_3840x2160_120fps_420_10bit_YUV.yuv'
,'/data/videos/4k/Suzie_3840x2160_120fps.yuv'
,'/data/videos/4k/Suzie_3840x2160_60fps.yuv'
,'/data/videos/4k/ToddlerFountain_4096x2160_60fps_10bit_420_jvet.yuv'
,'/data/videos/4k/YachtRide_3840x2160_120fps_420_10bit_YUV.yuv']

saidaResult = ['Beauty','BasketballDrive','NebutaFestival60_crop','FourPeople'
,'Bosphorus120fps','BQTerrace','PeopleOnStreet','Johnny','Cactus60','Cactus50'
,'SteamLocomotiveTrain','KristenAndSara','Coastguard','CrowdRun','Traffic'
,'SlideEditing','Foreman','Kimono','SlideShow','HoneyBee','ParkScene','Tennis'
,'Jockey','Mobile','News','RadySetGo','RollerCoaster','ShakeNDry','Suzie120fps'
,'Suzie60fps','ToddlerFountain','YachtRide120fps']

bit= ['10','8','10','8','10','8','8','8','8','8','10','8','8'
,'8','8','8','8','8','8','10','8','8','10','8','8','10'
,'10','10','8','8','10','10']

FrameRate = ['120','50','60','60','120','60','30','60'
,'30','50','60','60','60','25','30','30','60','24'
,'20','120','24','24','120','60','60','120','60','120'
,'120','60','60','120']

SourceWidth=['3840','1920','2560','1280','3840'
,'1920','2560','1280','3840','1920','2560','1280'
,'3840','1920','2560','1280','3840','1920','1280'
,'3840','1920','1920','3840','3840','3840','3840'
,'4096','3840','3840','3840','4096','3840']

SourceHeight=['2160','1080','1600','720','2160','1080','1600'
,'720','2160','1080','1600','720','2160','1080','1600','720'
,'2160','1080','720','2160','1080','1080','2160','2160','2160'
,'2160','2160','2160','2160','2160','2160','2160']

QP_list = [22,27,32,37]
subtrator= ['011','021','031','041','051','061','071','081','091','101','111','121'
            '012','022','032','042','052','062','072','082','093','102','112','122',
            '013','023','033','043','053','063','073','083','094','103','113','123',
            '014','024','034','044','054','064','074','084','095','104','114','124']

cabecalho ='linha,sequencia,bit,framerate,SourceWidth,SourceHeight,qp,subtrator,linhacomando,resultado,video'
intLinha =0

nome_file ="arquivos.csv"
arq1 = open(nome_file, "w")
arq1.write(cabecalho +"\n")
arq1.close 
  
for seq in range(0,len(sequencias)):
    arq1 = open(saidaResult[seq]+'.csv', "w")
    arq1.write(cabecalho +"\n")
    arq1.close
    for qp in range(0,len(QP_list)):
        for sub in range(0,len(subtrator)):
            intLinha = intLinha + 1
            arq_resultado = str(saidaResult[seq]) +'_'+ str(QP_list[qp]) +'_'+ str(subtrator[sub])            
            #print arq_resultado
            #linhaComando = "teste"
            linhaComando = "./EncoderAppStaticd -c encoder_intra_vtm.cfg"  " --QP="  + str(QP_list[qp]) + " -c sequence.cfg " + ' -i ' +  str(sequencias[seq]) +  " --FramesToBeEncoded=60 > " +  arq_resultado
            linhaSalva = str(intLinha)+','+ str(sequencias[seq])+','+ str(bit[seq])+','+ str(FrameRate[seq])+','+ str(SourceWidth[seq])+','+ str(SourceHeight[seq])+','+ str(QP_list[qp])+','+ str(subtrator[sub])+','+linhaComando+','+arq_resultado +','+ str(saidaResult[seq]) + '\n' 
            print (linhaSalva)
            arq1 = open(saidaResult[seq]+'.csv', "a")
            arq1.write(linhaSalva)                                  
            arq1.close

           
          
         
       
   
