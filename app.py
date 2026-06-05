import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Davranışsal Eğilim Dedektifleri",
    page_icon="🕵️",
    layout="centered"
)

ALL_BIASES = [
    "Aşırı Güven Eğilimi",
    "Temsil Etme Eğilimi",
    "Çapalama ve Düzeltme Eğilimi",
    "Bilişsel Çatışma Eğilimi",
    "Ulaşılabilirlik Eğilimi",
    "Kontrol İllüzyonu Eğilimi",
    "Hataları Yanlış Değerlendirme Eğilimi",
    "Sonucu Bildiğini Düşünme Eğilimi",
    "Sonralık Eğilimi",
    "Doğrulama Eğilimi",
    "Zihinsel Muhasebe Eğilimi",
    "Tutuculuk / Muhafazakârlık Eğilimi",
    "Aşırı İyimserlik Eğilimi",
    "Sahiplenme Eğilimi",
    "Belirsizlikten Kaçınma Eğilimi",
    "Kayıptan Kaçınma Eğilimi",
    "Pişmanlıktan Kaçınma Eğilimi",
    "Çerçeveleme Eğilimi",
    "Kendini Kontrol Etme Eksikliği Eğilimi",
    "Sürü Davranışı Eğilimi",
    "Bilgi Çağlayanı Eğilimi",
    "Dönemsel Eğilimler",
]

QUESTIONS = [
    {
        "case": "Selin’e iki farklı danışman aynı yatırım ürününü anlattı. İlk danışman ürünün “%80 olasılıkla kazanç sağlayabileceğini” söylediğinde Selin bu ürüne sıcak baktı. İkinci danışman aynı ürünü “%20 olasılıkla kayıp yaşatabilir” diye anlattığında ise ürünü çok riskli buldu. Oysa iki ifade de aynı olasılığı anlatıyordu.",
        "answer": "Çerçeveleme Eğilimi",
        "clue": "Aynı bilginin sunuluş biçimine göre kararının değişmesi.",
        "advice": "Karar vermeden önce bilgiyi hem kazanç hem kayıp çerçevesinden yeniden ifade etmelidir."
    },
    {
        "case": "Ayşe, geçen yıl yaptığı birkaç işlemden yüksek kazanç elde etmişti. Bu kazançları tamamen kendi analiz yeteneğine bağladı. “Ben doğru şirketleri seçiyorum” diyordu. Bu yıl yaptığı işlemler zarar etmeye başlayınca ise zararları faiz kararlarına, yabancı yatırımcı çıkışına ve piyasanın bozulmasına bağladı. Kendi karar sürecini hiç sorgulamadı.",
        "answer": "Hataları Yanlış Değerlendirme Eğilimi",
        "clue": "Başarıyı kendine, başarısızlığı dış faktörlere bağlaması.",
        "advice": "Performansını piyasa endeksiyle karşılaştırmalı ve her işlem için hata analizi yapmalıdır."
    },
    {
        "case": "Fatma, portföyünü üç ayrı hesap gibi görüyordu: “ana param”, “borsadan kazandığım para” ve “temettü gelirleri”. Ana parasını çok dikkatli kullanıyor, fakat borsadan kazandığı parayla daha riskli işlemler yapıyordu. “Zaten bu para kârdan geldi, kaybedersem çok önemli değil” diyordu.",
        "answer": "Zihinsel Muhasebe Eğilimi",
        "clue": "Parayı farklı zihinsel hesaplara ayırması ve toplam portföy riskini kaçırması.",
        "advice": "Tüm varlıklarını tek portföy görünümüyle değerlendirmeli ve toplam risk limiti belirlemelidir."
    },
    {
        "case": "Selim, yüksek oynaklığa sahip bir kripto varlıkta işlem yapıyordu. Fiyat hareketlerini dakika dakika izliyor, ekranın başında olduğu sürece piyasayı yönetebileceğini düşünüyordu. “Ben sürekli takip edersem zarar etmem; düşüş başlarsa hemen çıkarım” diyordu. Bu yüzden zarar-kes emri koymadı ve pozisyon büyüklüğünü sınırlamadı. Ancak beklenmedik bir haber akışıyla fiyat saniyeler içinde sert düştü. Selim emir verene kadar zarar büyümüştü.",
        "answer": "Kontrol İllüzyonu Eğilimi",
        "clue": "Kontrol edilemeyen piyasa hareketlerini ekrana bakarak kontrol edebileceğini düşünmesi.",
        "advice": "Piyasayı sürekli izlemek kontrol sağladığı anlamına gelmez; önceden zarar-kes, pozisyon limiti ve senaryo planı belirlenmelidir."
    },
    {
        "case": "Ebru, daha önce teknoloji sektöründeki bir hisseden yüksek kazanç elde etmişti. Yeni halka arz edilen başka bir teknoloji şirketini görünce, bu şirketin de aynı şekilde yükseleceğini düşündü. Şirketlerin finansal yapıları ve faaliyet alanları farklıydı; fakat Ebru yalnızca “ikisi de teknoloji şirketi” benzerliğine odaklandı.",
        "answer": "Temsil Etme Eğilimi",
        "clue": "Benzer görünen iki yatırımı aynı kategoriye koyarak genelleme yapması.",
        "advice": "Sektör benzerliği yerine şirketin kendi finansalları ve riskleri analiz edilmelidir."
    },
    {
        "case": "Ahmet, 120 TL’den aldığı hisse 82 TL’ye düştüğü hâlde satmak istemiyordu. “Satarsam zarar kesinleşir” diye düşünüyordu. Aynı dönemde başka bir hissesi %12 kârdaydı; onu ise hemen sattı çünkü “kâr cepte güzeldir” diyordu. Bir süre sonra zarardaki hisse daha da düştü, kârda sattığı hisse ise yükselmeye devam etti.",
        "answer": "Kayıptan Kaçınma Eğilimi",
        "clue": "Zararı realize etmekten kaçınması ve kârı erken satması.",
        "advice": "Önceden çıkış planı belirlemeli; kararı alış fiyatına değil güncel beklentiye göre vermelidir."
    },
    {
        "case": "Mert, yatırım yapacağı varlığı seçerken bilanço, değerleme ya da risk göstergelerine bakmıyordu. Sosyal medyada en çok konuşulan hisseleri takip ediyor, arkadaş grubunda hangi hisse popülerse onu alıyordu. Bir gün herkesin aynı kripto varlıktan bahsettiğini görünce “Bu kadar insan yanılıyor olamaz” diyerek alım yaptı.",
        "answer": "Sürü Davranışı Eğilimi",
        "clue": "Kendi analizini bırakıp kalabalığın davranışına uyması.",
        "advice": "Popülerlik yerine temel veri, risk ve portföy uygunluğu kontrol edilmelidir."
    },
    {
        "case": "Ali, portföyüne yeni bir hisse eklemek istiyordu. Şirketin finansallarını, sektör görünümünü ve olası riskleri incelemeden “Benim piyasa sezgim güçlüdür; çoğu yatırımcıdan daha iyi karar veririm” dedi. Arkadaşının “En azından bilançosuna bakalım” uyarısını “Buna gerek yok, ben bu işleri gözümden anlarım” diye geçiştirdi. Üstelik riskleri sınırlamak yerine portföyünün büyük kısmını tek bir hisseye yatırdı. Ali’nin kararı son fiyat hareketine ya da benzer bir geçmiş örneğe değil, kendi bilgi ve yeteneğine duyduğu aşırı güvene dayanıyordu.",
        "answer": "Aşırı Güven Eğilimi",
        "clue": "Kararın temelinde son dönem performans veya benzerlik değil, kendi sezgi ve yatırım yeteneğini abartması vardır.",
        "advice": "İşlem öncesi kontrol listesi kullanmalı, bağımsız veriyle karar vermeli ve tek varlık için maksimum portföy ağırlığı belirlemelidir."
    },
    {
        "case": "Mehmet, bir hisseyi 100 TL’den almıştı. Hisse 72 TL’ye düştüğünde şirketin kâr marjı gerilemiş, sektörde rekabet artmış ve analist hedef fiyatları aşağı çekilmişti. Buna rağmen Mehmet için 100 TL hâlâ “gerçek değer”di. “Bu hisse en azından aldığım fiyata dönmeden satılmaz” diyordu.",
        "answer": "Çapalama ve Düzeltme Eğilimi",
        "clue": "Alış fiyatını referans noktası yapması ve yeni bilgileri bu çapa etrafında değerlendirmesi.",
        "advice": "Alış fiyatına değil, güncel temel değer aralığına ve risk-getiri dengesine bakmalıdır."
    },
    {
        "case": "Zeynep, bir hisseyi aldıktan hemen sonra bu kararını arkadaşlarına güçlü biçimde savundu. Ertesi hafta şirketin beklenenden zayıf bilanço açıkladığını görünce rahatsız oldu; çünkü bu bilgi kendi kararının hatalı olabileceğini düşündürüyordu. Raporu ayrıntılı okumak yerine “Ben zaten uzun vadeli yatırımcıyım” diyerek kendini rahatlattı. Daha önce önem verdiği kârlılık göstergelerini bu kez önemsiz saydı. Asıl amacı, yeni bilgiyle kendi kararı arasındaki zihinsel rahatsızlığı azaltmaktı.",
        "answer": "Bilişsel Çatışma Eğilimi",
        "clue": "Çelişkili bilgi karşısında kararını objektif biçimde güncellemek yerine rahatsızlığı azaltacak gerekçeler üretmesi.",
        "advice": "Karar sonrası gelen ters bilgileri savunma refleksiyle değil, başlangıçtaki yatırım gerekçeleriyle karşılaştırarak değerlendirmelidir."
    },
]


def restart():
    st.session_state.clear()
    st.rerun()


def calculate_results():
    rows = []
    correct = 0

    for i, q in enumerate(QUESTIONS, start=1):
        user_answer = st.session_state.answers.get(i, "")
        is_correct = user_answer == q["answer"]
        correct += int(is_correct)

        rows.append({
            "Kart": i,
            "Verilen cevap": user_answer,
            "Doğru cevap": q["answer"],
            "Durum": "Doğru" if is_correct else "Yanlış",
            "Puan": 10 if is_correct else 0,
            "İpucu": q["clue"],
            "Öneri": q["advice"],
        })

    return correct, pd.DataFrame(rows)


if "step" not in st.session_state:
    st.session_state.step = "start"

if "current_card" not in st.session_state:
    st.session_state.current_card = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "name" not in st.session_state:
    st.session_state.name = ""


st.title("🕵️ Davranışsal Eğilim Dedektifleri")

with st.sidebar:
    st.write("Her ekranda yalnızca bir kart görünür.")
    st.write("Doğru cevaplar en sonda toplu gösterilir.")
    if st.button("Yeniden başlat"):
        restart()


if st.session_state.step == "start":
    st.snow()

    st.session_state.name = st.text_input(
        "Adınızı giriniz",
        value=st.session_state.name,
        placeholder="Ad Soyad"
    )

    st.info(
        "Bu uygulamada 10 vaka kartı vardır. "
        "Her kart ekrana tek tek gelecektir. "
        "Cevaplarınızı verdikten sonra sonuçlar en sonda toplu gösterilecektir."
    )

    if st.button("Başla", type="primary"):
        if not st.session_state.name.strip():
            st.warning("Lütfen adınızı giriniz.")
        else:
            st.session_state.step = "quiz"
            st.session_state.current_card = 0
            st.session_state.answers = {}
            st.rerun()


elif st.session_state.step == "quiz":
    i = st.session_state.current_card
    q = QUESTIONS[i]
    card_no = i + 1
    total = len(QUESTIONS)

    st.caption(f"Katılımcı: {st.session_state.name}")
    st.progress(card_no / total)

    st.header(f"Kart {card_no} / {total}")
    st.markdown("### Vaka")
    st.write(q["case"])

    selected_answer = st.selectbox(
        "Bu vakadaki ana eğilim nedir?",
        options=["Seçiniz..."] + ALL_BIASES,
        key=f"answer_{card_no}"
    )

    if card_no < total:
        button_label = "Cevabı kaydet ve sonraki karta geç"
    else:
        button_label = "Cevabı kaydet ve sonuçları göster"

    if st.button(button_label, type="primary"):
        if selected_answer == "Seçiniz...":
            st.warning("Lütfen bir cevap seçiniz.")
        else:
            st.session_state.answers[card_no] = selected_answer

            if card_no < total:
                st.session_state.current_card += 1
            else:
                st.session_state.step = "results"

            st.rerun()


elif st.session_state.step == "results":
    correct, result_df = calculate_results()
    score = correct * 10

    st.success(
        f"{st.session_state.name} için sonuç: "
        f"{correct}/10 doğru — {score}/100 puan"
    )

    if score >= 80:
        st.balloons()
        st.success("🎉 Harika! Davranışsal eğilimleri çok iyi teşhis ettiniz.")
    elif score >= 60:
        st.snow()
        st.info("👏 Güzel performans. Bazı eğilimler birbirine yakın olduğu için karışabilir.")
    else:
        st.warning("🔎 Eğilimleri vaka ipuçları üzerinden tekrar gözden geçirmek faydalı olabilir.")

    st.subheader("Toplu Sonuç Tablosu")
    st.dataframe(
        result_df[["Kart", "Verilen cevap", "Doğru cevap", "Durum", "Puan"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Açıklamalar")
    for _, row in result_df.iterrows():
        with st.expander(f"Kart {row['Kart']} — {row['Durum']}"):
            st.write(f"**Verilen cevap:** {row['Verilen cevap']}")
            st.write(f"**Doğru cevap:** {row['Doğru cevap']}")
            st.write(f"**İpucu:** {row['İpucu']}")
            st.write(f"**Öneri:** {row['Öneri']}")

    export_df = result_df.copy()
    export_df.insert(0, "Ad", st.session_state.name)
    export_df.insert(1, "Tarih", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    csv = export_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Sonuçları CSV olarak indir",
        data=csv,
        file_name=f"davranissal_egilim_sonuclari_{st.session_state.name}.csv",
        mime="text/csv"
    )

    if st.button("Yeniden başla"):
        restart()
