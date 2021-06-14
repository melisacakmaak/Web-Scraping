
import requests
from flask import Flask, render_template, request  # flask kütüphanemizi projemize import ettik.
import operator
from collections import Counter
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder="./templates")# app değişkenizimizin Flask olduğunu belirttik.


@app.route("/", methods=['POST', 'GET'])#Endpoint imizi tanımladık.
def mainUrl():
    return render_template('base.html')#Sitemizde görmek istediğimiz şeyi return ettik.


@app.route("/tekUrl", methods=['POST', 'GET'])# Endpoint imizi tanımladık.
def tekUrl():
    return render_template('tek_url.html')


# Form Verileri Alma
@app.route('/tekUrlVerileriAl', methods=['POST', 'GET'])
def verilerial():
    if request.method == 'POST':
        firstUrl = request.form.get('first-url')
        allWords = []# butun kelimeler icin dizi ata
        url_is = requests.get(firstUrl)# get fonksiyonu request gonderdi.
        soup = BeautifulSoup(url_is.text, "html.parser")# nesneyi olustururken html.parser oldugunu belirttik.

        for ke_grp in soup.find_all("html"):# html taglerinin icinde ki butun kelimeleri al
            sayfaİcerik = ke_grp.text# text formatında sayfa icerigine ekle
            kelimeleR = sayfaİcerik.lower().split()#split ile kelimeleri ayır

            for Kelime in kelimeleR:#butun kelimelere ekle
                allWords.append(Kelime)
        allWords = sem_cikar(allWords)#butun kelimelerden sembolleri cikart
        index = 0
        while index <= len(allWords):#kelime sayısını bulmak için kelime sıralama fonksiyonunu kullan
            KelSayisi = kel_siralama(allWords)
            return render_template("tek_url_gelen_bilgiler.html", urlBilgisi=firstUrl,
                                   kelSayisi=sorted(KelSayisi.items(), key=operator.itemgetter(0)))#kelimeleri ve frekanslarını gelen bilgiler sayfasına gönder
    else:
        return render_template("tek_url_gelen_bilgiler.html", hata="Formdan veri gelmedi!")#hata varsa hatayı veri gelmedi olarak sayfaya gönder


@app.route("/urlKarsilastirma", methods=['POST', 'GET'])# Endpoint imizi tanımladık.
def urlKarsilastirma():# Bir fonksiyon oluşturduk.
    return render_template('ana_ekran.html')


@app.route("/urlKarsilastirmaVerileri", methods=['POST', 'GET'])# Endpoint imizi tanımladık.
def urlKarsilastirmaVerileriGetir():# Bir fonksiyon oluşturduk.
    if request.method == 'POST':
        firstUrl = request.form.get('first-url')#formdan birinci url i aldık
        secondUrl = request.form.get('second-url')#formdan ikinci  url i aldık
        print(firstUrl)
        print(secondUrl)
        allWords = []# butun kelimeler icin dizi ata
        url_is = requests.get(firstUrl)# get fonksiyonu request gonderdi.
        soup = BeautifulSoup(url_is.text, "html.parser")# nesneyi olustururken html.parser oldugunu belirttik.

        for ke_grp in soup.find_all("html"):# html taglerinin icinde ki butun kelimeleri al
            sayfaİcerik = ke_grp.text# text formatında sayfa icerigine ekle
            kelimeleR = sayfaİcerik.lower().split()#kelimelerin harflerini küçült, split ile ayır

            for Kelime in kelimeleR:# butun kelimelere ekle
                allWords.append(Kelime)

        allWords = sem_cikar(allWords)# butun kelimelerden sembolleri cikart

        index = 0
        while index <= len(allWords):#kelimerin sayısını öğrenmek için kelime sırala fonksiyonunu kullandık
            KelSayisi = kel_siralama(allWords)

            for a_Kel, a_Say in sorted(KelSayisi.items(), key=operator.itemgetter(0)):
                # print((a_Kel, a_Say))  # kelimeyi ve kac defa gectigini yazdir
                index = index + 1

            An_Kel = sorted(KelSayisi, key=KelSayisi.get, reverse=True)  # kelimelerin gectigi sayıları sirala
            aKe = An_Kel[:5]#frekansı en yüksek beş kelimeyi anahtar kelime olarak seç

        allWords2 = []#ikinci url için butun kelimeler icin dizi ata
        url_is2 = requests.get(secondUrl)# get fonksiyonu request gonderdi.
        soup2 = BeautifulSoup(url_is2.text, "html.parser")# nesneyi olustururken html.parser oldugunu belirttik.

        for ke_grp2 in soup2.find_all("html"):# html taglerinin icinde ki butun kelimeleri al
            sayfaİcerik2 = ke_grp2.text#text formatında sayfa icerigine ekle
            kelimeleR2 = sayfaİcerik2.lower().split()#ikinci url için kelimelerin harflerini küçült, split ile ayır

            for Kelime2 in kelimeleR2:# butun kelimelere ekle
                allWords2.append(Kelime2)

        allWords2 = sem_cikar2(allWords2)# butun kelimelerden sembolleri cikart

        index2 = 0
        while index2 <= len(allWords2):# ikinci url için kelime frekanslarını bul
            KelSayisi2 = kel_siralama2(allWords2)
            keltoplam2 = KelSayisi2.values()#ikinci url de ki kelime sayısı

            for a_Kel2, a_Say2 in sorted(KelSayisi2.items(), key=operator.itemgetter(0)):
                # print((a_Kel2, a_Say2))  # kelimeyi ve kac defa gectigini yazdir
                index2 = index2 + 1

            An_Kel2 = sorted(KelSayisi2, key=KelSayisi2.get, reverse=True)  # kelimelerin gectigi sayıları sirala
            aKe2 = An_Kel2[:5]# ikinci url için frekansı en yüksek beş kelimeyi anahtar kelime olarak seç

        indexs = 0
        ayni_anahtarlar = []#aynı anahtar kelimeleri tutmak için dizi oluştur
        frekans_carpim = 1
        d = 0
        benzerlik = 0# iki url benzerligi
        yuzde=0
        while indexs in range(len(aKe2 or aKe)):
            print("1.url", aKe[indexs], "=", KelSayisi[aKe[indexs]])
            print("2.url", aKe2[indexs], "=", KelSayisi2[aKe2[indexs]])
            if aKe[indexs] in aKe2:

                ayni_anahtarlar.append(aKe[indexs])#eger ilk urlde ki anahtar kelime ikincide de anahtarsa diziye ekle

                indexs = indexs + 1
                # print("\n",a,"aynı")
                # print(KelSayisi2[aKe2[indexs]])
                frekans_carpim *= KelSayisi2[aKe2[indexs]]#aynı anahtar kelimelerin frekanslarını alıp çarp
                yuzde += 1
                benzerlik = (yuzde * 100) / 5#yuzde kaç benzediklerini hesapla

            else:
                b = aKe[indexs]
                indexs = indexs + 1

        print("\n", ayni_anahtarlar, "aynı anahtar kelimeler")
        print("frekansların çarpımı: ", frekans_carpim)
        BenzerlikSkoru = frekans_carpim / sum(keltoplam2)
        print("Benzerlik skoru: ", BenzerlikSkoru)
        #verileri url karşılaştırma formunda yazdır
        return render_template("url_karsilastirma_verileri.html", firstUrl=firstUrl, secondUrl=secondUrl,
                               ayni_anahtarlar=ayni_anahtarlar, frekans_carpim=frekans_carpim,
                               BenzerlikSkoru=BenzerlikSkoru, aKe=aKe, aKe2=aKe2, KelSayisi=KelSayisi, KelSayisi2=KelSayisi2,benzerlik=benzerlik)

    else:
        return render_template("url_karsilastirma_verileri.html", hata="Formdan veri gelmedi!")


def kel_siralama(allWords):# sayfada bulunan kelimlerin sayisini bulma fonksiyonu
    kel_Sayisi = {}#kelimeyi ve sayısı için dict
    index = 0

    while index < len(allWords):#kelime varsa sayısını bir arttır yoksa sayısını sabit tut
        #         print(len(allWords))
        #         print(str(allWords[index]))
        #         print("**")
        #         print(kel_Sayisi)
        if str(allWords[index]) in kel_Sayisi:
            kel_Sayisi[allWords[index]] += 1
        else:
            kel_Sayisi[allWords[index]] = 1
        # print(index)
        index += 1

    return kel_Sayisi


def sem_cikar(allWords):# kelimelerde ki sembolleri çikarma fonk.
    cikarilanKelimeler = []#sembollerden arındırılmış kelimeler için dizi
    cikarilacakSembollr = chr(775) + "–!'^+%&/()<>£#$½-*@.,:;→=_↵©️·"
    for Kelime in allWords:
        for sem in cikarilacakSembollr:
            if sem in Kelime:# sembol kelimenin içindeyse sembolu kelimeden cikart
                Kelime = Kelime.replace(sem, "")
        if (len(Kelime) > 0):# son haliyle uzunluğu 0 dan buyukse cikarilan kelimelere ekle
            cikarilanKelimeler.append(Kelime)
    return cikarilanKelimeler


def kel_siralama2(allWords2):# sayfada bulunan kelimlerin sayisini bulma
    kel_Sayisi2 = {}#kelimeyi ve sayısı için dict
    index2 = 0

    while index2 < len(allWords2):#kelime varsa sayısını bir arttır yoksa sayısını sabit tut
        #         print(len(allWords))
        #         print(str(allWords[index]))
        #         print("**")
        #         print(kel_Sayisi)
        if str(allWords2[index2]) in kel_Sayisi2:#kelime varsa sayısını bir arttır yoksa sayısını sabit tut
            kel_Sayisi2[allWords2[index2]] += 1
        else:
            kel_Sayisi2[allWords2[index2]] = 1
        # print(index2)
        index2 += 1

    return kel_Sayisi2  # kelime sayisini dondur


###################################################################################

# kelimelerde yer alan sembolleri cikart
def sem_cikar2(allWords2):  # kelimelerde ki sembolleri çikarma fonk.
    cikarilanKelimeler2 = []
    cikarilacakSembollr2 = chr(775) + "–!'^+%&/()<>£#$½-*@.,:;→=_↵©""️·"
    for Kelime2 in allWords2:
        for sem2 in cikarilacakSembollr2:
            if sem2 in Kelime2:# sembol kelimenin içindeyse sembolu kelimeden cikart
                Kelime2 = Kelime2.replace(sem2, "")
        if (len(Kelime2) > 0):# son haliyle kelimeyse cikarilan kelimelere ekle
            cikarilanKelimeler2.append(Kelime2)
    return cikarilanKelimeler2