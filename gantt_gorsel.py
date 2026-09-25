"""
Gantt Şeması Görselleştirmesi
==============================
Johnson algoritması sonucunu ve FCFS (geliş sırası) karşılaştırmasını
Gantt şeması olarak çizer, PNG olarak kaydeder.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from johnson_algoritmasi import (
    rastgele_isler_uret,
    johnson_sirala,
    makespan_hesapla,
)


def gantt_ciz(ax, cetvel: list[dict], baslik: str):
    renkler = plt.cm.tab20.colors
    for idx, kayit in enumerate(cetvel):
        renk = renkler[idx % len(renkler)]

        ax.barh(
            y=1, left=kayit["m1_baslangic"],
            width=kayit["m1_bitis"] - kayit["m1_baslangic"],
            height=0.8, color=renk, edgecolor="black"
        )
        ax.barh(
            y=0, left=kayit["m2_baslangic"],
            width=kayit["m2_bitis"] - kayit["m2_baslangic"],
            height=0.8, color=renk, edgecolor="black"
        )

        ax.text(
            (kayit["m1_baslangic"] + kayit["m1_bitis"]) / 2, 1,
            kayit["ad"].replace("İş-", ""), ha="center", va="center", fontsize=8
        )
        ax.text(
            (kayit["m2_baslangic"] + kayit["m2_bitis"]) / 2, 0,
            kayit["ad"].replace("İş-", ""), ha="center", va="center", fontsize=8
        )

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Makine 2", "Makine 1"])
    ax.set_xlabel("Zaman")
    ax.set_title(baslik)
    ax.grid(axis="x", linestyle="--", alpha=0.4)


def main():
    isler = rastgele_isler_uret(n=8)

    optimum_sira = johnson_sirala(isler)
    cmax_optimum, cetvel_optimum = makespan_hesapla(optimum_sira)

    cmax_fcfs, cetvel_fcfs = makespan_hesapla(isler)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6.5))

    gantt_ciz(ax1, cetvel_optimum, f"Johnson Algoritması - Optimum Sıra (Cmax = {cmax_optimum:g})")
    gantt_ciz(ax2, cetvel_fcfs, f"Geliş Sırası / FCFS - Karşılaştırma (Cmax = {cmax_fcfs:g})")

    iyilesme = (cmax_fcfs - cmax_optimum) / cmax_fcfs * 100
    fig.suptitle(f"Flow-Shop Çizelgeleme Karşılaştırması  (İyileşme: %{iyilesme:.1f})",
                 fontsize=13, fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("gantt_karsilastirma.png", dpi=150)
    print("Gantt şeması 'gantt_karsilastirma.png' olarak kaydedildi.")
    print(f"Johnson Cmax = {cmax_optimum} | FCFS Cmax = {cmax_fcfs} | İyileşme = %{iyilesme:.1f}")


if __name__ == "__main__":
    main()
