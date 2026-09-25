"""
Johnson Algoritması ile Akış Tipi (Flow-Shop) İş Sıralama
===========================================================

Endüstri Mühendisliği - Üretim Planlama ve Çizelgeleme

Problem:
    n adet iş, 2 makineden sırasıyla (M1 -> M2) geçmek zorunda.
    Her işin M1 ve M2 üzerindeki işlem süreleri bilinmektedir.
    Amaç: toplam tamamlanma süresini (makespan / Cmax) minimize
    eden iş sıralamasını bulmak.

Johnson Kuralı (1954):
    1. Tüm işleri iki gruba ayır:
         Grup A: M1 süresi <= M2 süresi olan işler
         Grup B: M1 süresi >  M2 süresi olan işler
    2. Grup A'yı M1 süresine göre KÜÇÜKTEN BÜYÜĞE sırala.
    3. Grup B'yi M2 süresine göre BÜYÜKTEN KÜÇÜĞE sırala.
    4. Sıra = Grup A + Grup B

    Bu sıralama, 2 makineli flow-shop problemi için matematiksel
    olarak KANITLANMIŞ optimum (en iyi) sonucu verir.

Kullanım:
    python johnson_algoritmasi.py
"""

from dataclasses import dataclass
import random


@dataclass
class Is:
    """Bir üretim işini temsil eder."""
    ad: str
    m1_suresi: float   # 1. makinedeki işlem süresi
    m2_suresi: float   # 2. makinedeki işlem süresi


def johnson_sirala(isler: list[Is]) -> list[Is]:
    """
    Johnson algoritmasına göre optimum iş sırasını döndürür.

    Parametreler
    ----------
    isler : list[Is]
        Sıralanacak işlerin listesi.

    Döndürür
    -------
    list[Is]
        Optimum sırayla dizilmiş işler.
    """
    grup_a = [i for i in isler if i.m1_suresi <= i.m2_suresi]
    grup_b = [i for i in isler if i.m1_suresi > i.m2_suresi]

    grup_a.sort(key=lambda i: i.m1_suresi)          # küçükten büyüğe
    grup_b.sort(key=lambda i: i.m2_suresi, reverse=True)  # büyükten küçüğe

    return grup_a + grup_b


def makespan_hesapla(sira: list[Is]) -> tuple[float, list[dict]]:
    """
    Verilen bir iş sırası için toplam tamamlanma süresini (Cmax)
    ve her işin başlangıç/bitiş zamanlarını hesaplar.

    Döndürür
    -------
    (cmax, zaman_cetveli)
        cmax : toplam tamamlanma süresi
        zaman_cetveli : her iş için {ad, m1_baslangic, m1_bitis,
                                       m2_baslangic, m2_bitis}
    """
    m1_bitis_onceki = 0.0
    m2_bitis_onceki = 0.0
    cetvel = []

    for is_ in sira:
        m1_baslangic = m1_bitis_onceki
        m1_bitis = m1_baslangic + is_.m1_suresi

        # M2, hem kendi önceki işini bitirmiş olmalı hem de bu işin
        # M1'den çıkmasını beklemeli
        m2_baslangic = max(m1_bitis, m2_bitis_onceki)
        m2_bitis = m2_baslangic + is_.m2_suresi

        cetvel.append({
            "ad": is_.ad,
            "m1_baslangic": m1_baslangic,
            "m1_bitis": m1_bitis,
            "m2_baslangic": m2_baslangic,
            "m2_bitis": m2_bitis,
        })

        m1_bitis_onceki = m1_bitis
        m2_bitis_onceki = m2_bitis

    cmax = cetvel[-1]["m2_bitis"] if cetvel else 0.0
    return cmax, cetvel


def rastgele_isler_uret(n: int, min_sure=2, max_sure=20, seed=42) -> list[Is]:
    """Test/örnek amaçlı rastgele iş listesi üretir."""
    rnd = random.Random(seed)
    return [
        Is(ad=f"İş-{i+1}",
           m1_suresi=rnd.randint(min_sure, max_sure),
           m2_suresi=rnd.randint(min_sure, max_sure))
        for i in range(n)
    ]


def ozet_yazdir(baslik: str, sira: list[Is], cmax: float):
    print(f"\n{baslik}")
    print("-" * len(baslik))
    print(" -> ".join(i.ad for i in sira))
    print(f"Toplam tamamlanma süresi (Cmax): {cmax}")


if __name__ == "__main__":
    isler = rastgele_isler_uret(n=8)

    print("İş listesi (M1 süresi, M2 süresi):")
    for i in isler:
        print(f"  {i.ad}: M1={i.m1_suresi}  M2={i.m2_suresi}")

    # 1) Johnson algoritması ile optimum sıra
    optimum_sira = johnson_sirala(isler)
    cmax_optimum, cetvel_optimum = makespan_hesapla(optimum_sira)
    ozet_yazdir("JOHNSON ALGORİTMASI (Optimum Sıra)", optimum_sira, cmax_optimum)

    # 2) Karşılaştırma: rastgele / geliş sırası (FCFS)
    cmax_fcfs, _ = makespan_hesapla(isler)
    ozet_yazdir("Geliş Sırası (FCFS - karşılaştırma amaçlı)", isler, cmax_fcfs)

    iyilesme = (cmax_fcfs - cmax_optimum) / cmax_fcfs * 100
    print(f"\nJohnson algoritması ile FCFS'e göre iyileşme: %{iyilesme:.1f}")
