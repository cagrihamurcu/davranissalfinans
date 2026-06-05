import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Davranışsal Eğilim Dedektifleri",
    page_icon="🕵️",
    layout="wide"
)

# ============================================================
# Davranışsal Eğilim Dedektifleri
# Streamlit sınıf içi yarışma uygulaması
# Her katılımcıya/gruba aynı 10 vaka aynı sırayla gelir.
# ============================================================

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

# Karışık ama sabit sıra: her katılımcı/grup aynı sırayı görür.
QUESTIONS = [
    {
        "card_no": 1,
        "case": """Ayşe, geçen yıl yaptığı birkaç işlemden yüksek kazanç elde etmişti. 
Bu kazançları tamamen kendi analiz yeteneğine bağladı. “Ben doğru şirketleri seçiyorum” diyordu. 
Bu yıl yaptığı işlemler zarar etmeye başlayınca ise zararları faiz kararlarına, yabancı yatırımcı çıkışına 
ve piyasanın bozulmasına bağladı. Kendi karar sürecini hiç sorgulamadı.""",
        "answer": "Hataları Yanlış Değerlendirme Eğilimi",
        "clue": "Başarıyı kendine, başarısızlığı dış faktörlere bağlaması.",
        "advice": "Performansını piyasa endeksiyle karşılaştırmalı ve her işlem için hata analizi yapmalıdır."
    },
    {
        "card_no": 2,
        "case": """Mert, yatırım yapacağı varlığı seçerken bilanço, değerleme ya da risk göstergelerine bakmıyordu. 
Sosyal medyada en çok konuşulan hisseleri takip ediyor, arkadaş grubunda hangi hisse popülerse onu alıyordu. 
Bir gün herkesin aynı kripto varlıktan bahsettiğini görünce “Bu kadar insan yanılıyor olamaz” diyerek alım yaptı.""",
        "answer": "Sürü Davranışı Eğilimi",
        "clue": "Kendi analizini bırakıp kalabalığın davranışına uyması.",
        "advice": "Popülerlik yerine temel veri, risk ve portföy uygunluğu kontrol edilmelidir."
    },
    {
        "card_no": 3,
        "case": """Mehmet, bir hisseyi 100 TL’den almıştı. Hisse 72 TL’ye düştüğünde şirketin kâr marjı gerilemiş, 
sektörde rekabet artmış ve analist hedef fiyatları aşağı çekilmişti. Buna rağmen Mehmet için 100 TL hâlâ 
“gerçek değer”di. “Bu hisse en azından aldığım fiyata dönmeden satılmaz” diyordu.""",
        "answer": "Çapalama ve Düzeltme Eğilimi",
        "clue": "Alış fiyatını referans noktası yapması ve yeni bilgileri bu çapa etrafında değerlendirmesi.",
        "advice": "Alış fiyatına değil, güncel temel değer aralığına ve risk-getiri dengesine bakmalıdır."
    },
    {
        "card_no": 4,
        "case": """Selin’e iki farklı danışman aynı yatırım ürününü anlattı. İlk danışman ürünün 
“%80 olasılıkla kazanç sağlayabileceğini” söylediğinde Selin bu ürüne sıcak baktı. İkinci danışman aynı ürünü 
“%20 olasılıkla kayıp yaşatabilir” diye anlattığında ise ürünü çok riskli buldu. Oysa iki ifade de aynı olasılığı anlatıyordu.""",
        "answer": "Çerçeveleme Eğilimi",
        "clue": "Aynı bilginin sunuluş biçimine göre kararının değişmesi.",
        "advice": "Karar vermeden önce bilgiyi hem kazanç hem kayıp çerçevesinden yeniden ifade etmelidir."
    },
    {
        "card_no": 5,
        "case": """Selim, yüksek oynaklığa sahip bir kripto varlıkta işlem yapıyordu. 
Fiyat hareketlerini dakika dakika izliyor, ekranın başında olduğu sürece piyasayı yönetebileceğini düşünüyordu. 
“Ben sürekli takip edersem zarar etmem; düşüş başlarsa hemen çıkarım” diyordu. Bu yüzden zarar-kes emri koymadı ve pozisyon büyüklüğünü sınırlamadı. 
Ancak beklenmedik bir haber akışıyla fiyat saniyeler içinde sert düştü. Selim emir verene kadar zarar büyümüştü.""",
        "answer": "Kontrol İllüzyonu Eğilimi",
        "clue": "Kontrol edilemeyen piyasa hareketlerini ekrana bakarak kontrol edebileceğini düşünmesi.",
        "advice": "Piyasayı sürekli izlemek kontrol sağladığı anlamına gelmez; önceden zarar-kes, pozisyon limiti ve senaryo planı belirlenmelidir."
    },
    {
        "card_no": 6,
        "case": """Fatma, portföyünü üç ayrı hesap gibi görüyordu: “ana param”, “borsadan kazandığım para” ve 
“temettü gelirleri”. Ana parasını çok dikkatli kullanıyor, fakat borsadan kazandığı parayla daha riskli işlemler yapıyordu. 
“Zaten bu para kârdan geldi, kaybedersem çok önemli değil” diyordu.""",
        "answer": "Zihinsel Muhasebe Eğilimi",
        "clue": "Parayı farklı zihinsel hesaplara ayırması ve toplam portföy riskini kaçırması.",
        "advice": "Tüm varlıklarını tek portföy görünümüyle değerlendirmeli ve toplam risk limiti belirlemelidir."
    },
    {
        "card_no": 7,
        "case": """Ebru, daha önce teknoloji sektöründeki bir hisseden yüksek kazanç elde etmişti. 
Yeni halka arz edilen başka bir teknoloji şirketini görünce, bu şirketin de aynı şekilde yükseleceğini düşündü. 
Şirketlerin finansal yapıları ve faaliyet alanları farklıydı; fakat Ebru yalnızca “ikisi de teknoloji şirketi” benzerliğine odaklandı.""",
        "answer": "Temsil Etme Eğilimi",
        "clue": "Benzer görünen iki yatırımı aynı kategoriye koyarak genelleme yapması.",
        "advice": "Sektör benzerliği yerine şirketin kendi finansalları ve riskleri analiz edilmelidir."
    },
    {
        "card_no": 8,
        "case": """Ahmet, 120 TL’den aldığı hisse 82 TL’ye düştüğü hâlde satmak istemiyordu. 
“Satarsam zarar kesinleşir” diye düşünüyordu. Aynı dönemde başka bir hissesi %12 kârdaydı; onu ise hemen sattı çünkü 
“kâr cepte güzeldir” diyordu. Bir süre sonra zarardaki hisse daha da düştü, kârda sattığı hisse ise yükselmeye devam etti.""",
        "answer": "Kayıptan Kaçınma Eğilimi",
        "clue": "Zararı realize etmekten kaçınması ve kârı erken satması.",
        "advice": "Önceden çıkış planı belirlemeli; kararı alış fiyatına değil güncel beklentiye göre vermelidir."
    },
    {
        "card_no": 9,
        "case": """Zeynep, bir hisseyi aldıktan hemen sonra bu kararını arkadaşlarına güçlü biçimde savundu. 
Ertesi hafta şirketin beklenenden zayıf bilanço açıkladığını görünce rahatsız oldu; çünkü bu bilgi kendi kararının hatalı 
olabileceğini düşündürüyordu. Raporu ayrıntılı okumak yerine “Ben zaten uzun vadeli yatırımcıyım” diyerek kendini rahatlattı. 
Daha önce önem verdiği kârlılık göstergelerini bu kez önemsiz saydı. Asıl amacı, yeni bilgiyle kendi kararı arasındaki 
zihinsel rahatsızlığı azaltmaktı.""",
        "answer": "Bilişsel Çatışma Eğilimi",
        "clue": "Çelişkili bilgi karşısında kararını objektif biçimde güncellemek yerine rahatsızlığı azaltacak gerekçeler üretmesi.",
        "advice": "Karar sonrası gelen ters bilgileri savunma refleksiyle değil, başlangıçtaki yatırım gerekçeleriyle karşılaştırarak değerlendirmelidir."
    },
    {
        "card_no": 10,
        "case": """Ali, portföyüne yeni bir hisse eklemek istiyordu. Şirketin finansallarını, sektör görünümünü ve olası riskleri incelemeden 
“Benim piyasa sezgim güçlüdür; çoğu yatırımcıdan daha iyi karar veririm” dedi. Arkadaşının “En azından bilançosuna bakalım” uyarısını 
“Buna gerek yok, ben bu işleri gözümden anlarım” diye geçiştirdi. Üstelik riskleri sınırlamak yerine portföyünün büyük kısmını tek bir hisseye yatırdı. 
Ali’nin kararı son fiyat hareketine ya da benzer bir geçmiş örneğe değil, kendi bilgi ve yeteneğine duyduğu aşırı güvene dayanıyordu.""",
        "answer": "Aşırı Güven Eğilimi",
        "clue": "Kararın temelinde son dönem performans veya benzerlik değil, kendi sezgi ve yatırım yeteneğini abartması vardır.",
        "advice": "İşlem öncesi kontrol listesi kullanmalı, bağımsız veriyle karar vermeli ve tek varlık için maksimum portföy ağırlığı belirlemelidir."
    },
]


def init_state():
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "answers" not in st.session_state:
        st.session_state.answers = {}


def reset_game():
    st.session_state.submitted = False
    st.session_state.answers = {}
    st.rerun()


def score_answers(answers):
    correct = 0
    rows = []
    for i, q in enumerate(QUESTIONS, start=1):
        user_answer = answers.get(f"q{i}", "")
        is_correct = user_answer == q["answer"]
        correct += int(is_correct)
        rows.append({
            "Kart": i,
            "Verilen cevap": user_answer,
            "Doğru cevap": q["answer"],
            "Durum": "Doğru" if is_correct else "Yanlış",
            "İpucu": q["clue"],
            "Öneri": q["advice"],
        })
    return correct, pd.DataFrame(rows)


init_state()

st.title("🕵️ Davranışsal Eğilim Dedektifleri")
st.caption("Sınıf içi grup yarışması | 10 vaka kartı | Her katılımcı için aynı sıra")

with st.sidebar:
    st.header("Uygulama Bilgisi")
    st.write("Her kartta bir yatırımcı davranışı var.")
    st.write("Görev: Vakadaki ana davranışsal eğilimi teşhis etmek.")
    st.markdown("---")
    st.write("Puanlama: Her doğru cevap 10 puan.")
    st.write("Toplam: 100 puan.")
    st.markdown("---")
    if st.button("Oyunu sıfırla"):
        reset_game()

participant = st.text_input("Grup / katılımcı adı", placeholder="Örn. Grup 1")

st.info(
    "Her kartı okuyunuz ve vakadaki **ana davranışsal eğilimi** seçiniz. "
    "Cevaplarınızı gönderdikten sonra doğru cevaplar ve kısa açıklamalar görünecektir."
)

if not st.session_state.submitted:
    with st.form("quiz_form"):
        for i, q in enumerate(QUESTIONS, start=1):
            st.markdown(f"### Kart {i}")
            st.write(q["case"])
            selected = st.selectbox(
                "Bu vakadaki ana eğilim nedir?",
                options=["Seçiniz..."] + ALL_BIASES,
                key=f"q{i}",
            )
            st.markdown("---")

        submitted = st.form_submit_button("Cevapları gönder")

        if submitted:
            missing = [i for i in range(1, len(QUESTIONS) + 1) if st.session_state.get(f"q{i}") == "Seçiniz..."]
            if missing:
                st.warning(f"Lütfen tüm kartlar için cevap seçiniz. Eksik kartlar: {missing}")
            else:
                st.session_state.answers = {f"q{i}": st.session_state.get(f"q{i}") for i in range(1, len(QUESTIONS) + 1)}
                st.session_state.submitted = True
                st.rerun()

else:
    correct, results_df = score_answers(st.session_state.answers)
    score = correct * 10

    st.success(f"{participant or 'Katılımcı'} için sonuç: {correct}/10 doğru — {score}/100 puan")

    if score >= 80:
        st.balloons()
        st.write("🎉 Güçlü teşhis performansı.")
    elif score >= 50:
        st.write("👍 Temel eğilimler yakalanmış; karıştırılan kavramlar birlikte tartışılabilir.")
    else:
        st.write("🔎 Eğilimleri vaka ipuçları üzerinden tekrar gözden geçirmek yararlı olabilir.")

    st.subheader("Cevap Anahtarı ve Açıklamalar")

    for _, row in results_df.iterrows():
        status_icon = "✅" if row["Durum"] == "Doğru" else "❌"
        with st.expander(f"{status_icon} Kart {row['Kart']} — {row['Durum']}"):
            st.write(f"**Verilen cevap:** {row['Verilen cevap']}")
            st.write(f"**Doğru cevap:** {row['Doğru cevap']}")
            st.write(f"**İpucu:** {row['İpucu']}")
            st.write(f"**Yatırımcıya öneri:** {row['Öneri']}")

    export_df = results_df.copy()
    export_df.insert(0, "Katılımcı / Grup", participant or "Belirtilmedi")
    export_df.insert(1, "Tarih", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    export_df["Puan"] = export_df["Durum"].map({"Doğru": 10, "Yanlış": 0})

    csv = export_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Sonuçları CSV olarak indir",
        data=csv,
        file_name=f"davranissal_egilim_sonuclari_{participant or 'katilimci'}.csv",
        mime="text/csv",
    )

    st.button("Yeniden başla", on_click=reset_game)
