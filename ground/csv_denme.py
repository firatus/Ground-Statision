import csv

s = "a,b,123,32.0"
new = s.split(",")

with open('deneme.csv', 'w') as f:
    writer =  csv.writer(f)
    writer.writerow(['TAKIM NO','PAKET NUMARASI','GONDERME SAATI','BASINC1','BASINC2','YUKSEKLIK1','YUKSEKLIK2','IRTIFA FARKI','INIS HIZI','SICAKLIK','PIL GERILIMI','GPS1 LATITUDE','GPS1 LONGTITUDE','GPS1 ALTITUDE','GPS2 LATITUDE','GPS2 LONGTITUDE','GPS2 ALTITUDE','UYDU STATUSU','PITCH','ROLL','YAW','DONUS SAYISI','VIDEO AKTARIM BILGISI'])
    writer.writerow(new)