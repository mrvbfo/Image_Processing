I.	RENK DAĞILIMI (HİSTOGRAM) ÇIKARMA
Bir görüntüdeki renk dağılımı histogram çıkarma yöntemi ile analiz edilir.  Görüntü grayscale formatta okunur ve piksel değerleri tespit edilir. Fonksiyonda, okunan piksel değerleri histogramda gösterilir. Bu, görselin genel parlaklık ve kontrast özellikleri hakkında bilgi verir. 

II.	RESMİ İKİLİLEŞTİRME (BİNARİZATİON)
İkilileştirme, bir görüntüyü (gri seviyeli veya renkli bir görüntüyü) ikili bir görüntüye dönüştürmek için kullanılan bir görüntü işleme tekniğidir. İkilileştirme sonucu oluşturulan ikili görüntü, yalnızca iki piksel değeri içerir, tipik olarak 0 ve 1, burada 0 arka planı bizim örneğimizde siyah pikselleri ve 1 ön planı bizim örneğimizde beyaz pikselleri temsil eder. 

III.	RESMİ İKİDEN FAZLA BÖLGEYE AYIRMA
Resimleri, üç eşik değeri belirleyerek farklı yoğunluk bölgelerine ayırdım. Her eşik aralığında farklı gri tonları ile bölgeleri belirginleştirdim. Histogram üzerindeki  tepe ve vadi noktalarını analiz ederek eşik değerleri seçtim.

IV.	MORFOLOJİK OPERATÖRLER UYGULAMA
3x3’lük Kernel matrisini aşağıdaki kod ile tanımladım:
kernel = np.ones((3, 3), np.uint8)
	Bu Kernel, Erosion, Dilation Opening, ve Closing işlemlerini uygularken görüntüyü pikseller bazında işleyerek detaylı ve küçük ölçekli olmasını sağlar. Bu operatör şöyle gözükür:
 ![image](https://github.com/user-attachments/assets/822a7808-79d6-4c79-84e5-ceb4020e01ca)

 	Bu matris Kernel olarak adlandırılır. Her bir piksel için bu filtre uygulanır. Erosion (aşındırma), bu alanın tamamındaki değerler düşükse orta noktadaki değeri de dşürür. Dilation (genişletme), alandaki değerler yüksekse orta noktadaki değeri yükseltir. Bunların kombinasyonunu opening ve closing işlemlerinde gerçekleştiririz. 

V.	BÖLGE GENİŞLETME TEKNİĞİ İLE NESNE BULMA (REGİON GROWİNG)
4-Komşuluk kontrolü ile pikselleri (üst,alt,sağ,sol) şeklinde yoğunluk değerlerine göre seed noktalarının yoğunlukları ile karşılaştırdım. Seed noktasına yakın yoğunluktaki pikseller aynı bölgeye dahil edilir. Tüm pikseller taranarak bu bölgeler oluşturulur. Bu belirlenen bölgeler renklendirilerek görsel olarak ayırt edilmesini sağladım.

VI.	HİSTOGRAM EQUALİSATİON
Histogram dengeleme, bir resimdeki renk değerlerinin belli bir yerde kümelenmiş olmasından kaynaklanan dengesizliği gidermek için kullanılan bir yöntemdir.
Bu yöntemi kullanarak her bir görüntü için yeni histogram grafikleri oluşturdum ve bu histogram grafikleri üzerinden renk dağılımı (histogram) çıkarma, resmi ikilileştirme (binarization), resmi ikiden fazla bölgeye ayırma, morfolojik operatörler uygulama, bölge genişletme tekniği ile nesne bulma (region Growing) işlemleri tekrarladım.

