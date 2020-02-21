import fileinput
import os
import shutil
import string
import sys
from datetime import *
import os.path
import csv
from email.mime.text import MIMEText
import smtplib
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

#copia arquivos
def copia(origem,destino):
  for linha in origem:
    valor_linha = linha.rstrip()
    dir_arquivo = os.path.dirname(valor_linha)
    if not os.path.exists(dir_arquivo):
        os.makedirs(dir_arquivo)

    shutil.copy2(valor_linha, destino) 
    
# envia e-mail
def enviaemail(titulo,message):
	msg = MIMEMultipart()
	MIMEMultipart()
	 
	 
	 
	# setup the parameters of the message
	password = "rafa1135"
	msg['From'] = "gaci04.ufpel@gmail.com"
	msg['To'] = "gaci04.ufpel@gmail.com"
	msg['Subject'] = titulo
	 
	# add in the message body
	msg.attach(MIMEText(message, 'plain'))
	 
	#create server
	server = smtplib.SMTP('smtp.gmail.com: 587')
	 
	server.starttls()
	 
	# Login Credentials for sending the mail
	server.login(msg['From'], password)
	 
	 
	# send the message via the server.
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	 
	server.quit()    
# busca arquivos
def buscaArquivos(pasta,extensao):
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arquivos_ext = [arq for arq in arquivos if arq.lower().endswith(extensao)]   
    return arquivos_ext
  
 
 
def replace_word(infile,newfile,old_word,new_word):
    if not os.path.isfile(infile):
        print ("Error on replace_word, not a regular file: "+infile)
        sys.exit(1)

    f1=open(infile,'r').read()
    f2=open(newfile,'w')
    m=f1.replace(old_word,new_word)
    f2.write(m)
    
#localiza linha em arquivos
def localizaLinha(arquivo,palavra):
   with open(arquivo, "r") as arq:
    for linha in arq:
        if linha.find(palavra) > -1:
           return linha
       
        
PATH_RESULT="../resultado/sad/"       
cabecaho_arq="Video,subtrator,impreciso,QP,Bitrate,Y-PSNR,U-PSNR,V-PSNR,YUV-PSNR,Tamanho"

for param in sys.argv :
    print(param)

nome_file ="../config/" + str(param) 
print(nome_file)
input_file = csv.DictReader(open(nome_file))
for row in input_file:
	linha=str(row["linha"])
	sequencia=str(row["sequencia"])
	bit=str(row["bit"])
	framerate=str(row["framerate"])
	SourceWidth=str(row["SourceWidth"])
	SourceHeight=str(row["SourceHeight"])
	qp=str(row["qp"])
	subtrator=str(row["subtrator"])
	linhacomando=str(row["linhacomando"])
	arq_resultado=str(row["resultado"])
	video=str(row["video"])
		
	
	sub = str(subtrator[0])
	imp = str(subtrator[1])

	arq3 = open("impreciso.txt", "w")
	arq3.write((imp) +"\n")
	arq3.close   


	arq2 = open("subtrator.txt", "w")
	arq2.write(str(sub) +"\n")
	arq2.close   

	
	nome_file = PATH_RESULT + video +".csv"
	arq1 = open(nome_file, "w")
	arq1.write(cabecaho_arq +"\n")
	arq1.close

	os.system("cp ../config/sequence.cfg .")	
	os.system("cp ../config/encoder_intra_vtm.cfg .")
	

	os.system("clear")
	print( '---------------------------------------------------------')
	print ("Linha: " + linha)
	print ( "Video: " + video )
	print ("QP: " + qp)
	print ("Subtrator: " + sub)
	print ("Impreciso: " + imp)	
	print ("bit: " + bit)
	print ("framerate: " + framerate)
	print ("SourceWidth: " + SourceWidth)	
	print ("SourceHeight: " + SourceHeight)
	print ("subtrator: " + subtrator)
	print ("linhacomando: " + linhacomando)
	print ("framerate: " + framerate)
	print ("arq_resultado: " + arq_resultado)
	print ('---------------------------------------------------------')
	montaTitulo= 'Linha '+ linha + ' Video ' + video+ ' QP ' + qp+ ' Subtrator ' + sub + ' Impreciso ' + imp
	enviaemail(montaTitulo + 'Begin' ,linhacomando)
	replace_word("sequence.cfg","sequence.cfg","@InputBitDepth@",bit)
	replace_word("sequence.cfg","sequence.cfg","@FrameRate@",framerate)
	replace_word("sequence.cfg","sequence.cfg","@SourceWidth@",SourceWidth)
	replace_word("sequence.cfg","sequence.cfg","@SourceHeight@",SourceHeight)
	replace_word("sequence.cfg","sequence.cfg","@FramesToBeEncoded@","2") 
	
	print (linhacomando)
	os.system(linhacomando)
	#
    
	qualidade = localizaLinha(arq_resultado,"  a  ")  
	qualidade = string.replace(qualidade," ",";")
	qualidade = string.replace(qualidade,";;",";")
	
	

	linha = linha+';'+ video +';'+ (sub) +';' + imp + ';' +qp + ';' + str(qualidade) 
	linha = string.replace(linha,";;;;;",";")
	linha = string.replace(linha,";;",";")	
	linha = string.replace(linha,"sec"," ")
	linha = string.replace(linha,")"," ")
	linha = string.replace(linha,"("," ")
	linha = string.replace(linha,"kbps"," ")
	linha = string.replace(linha,"	","")
	linha = string.replace(linha,";;",";")
	linha = string.replace(linha," ","")
	linha = string.replace(linha,";;",";")
	linha = string.replace(linha,";;",";")
	linha = string.replace(linha,";;",";")
	linha = string.replace(linha,";60;a;",";")	
	linha = string.replace(linha,";6;a;",";")		
	linha = string.replace(linha,'\n',"")
	linha = string.replace(linha,';',",")
	
	

	arq1 = open(nome_file , "a")
	arq1.write(linha + '\n')                                  
	arq1.close
	#sys.exit(1)
	
	os.system("cp -Rvfp "+ arq_resultado  + "  "+      PATH_RESULT+arq_resultado+".out" )
	os.system("cp -Rvfp valores.txt" + "  "+   PATH_RESULT + 'SSE_' + arq_resultado+".csv" )
	#os.system("cp -Rvfp rec.yuv " + "  "+   PATH_RESULT + "rec"+ arq_resultado+(oper)+ ".yuv")
	#os.system("cp -Rvfp str.bin " + "  "+   PATH_RESULT + "bin"+ arq_resultado +(oper)+ ".bin")
	enviaemail(montaTitulo +'End: ' ,linhacomando)
	#sys.exit(1)


