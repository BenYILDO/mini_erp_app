import streamlit as st
import pandas as pd

# Başlangıç verileri
# Stok bilgileri DataFrame olarak saklanacak
if 'stok_df' not in st.session_state:
    st.session_state.stok_df = pd.DataFrame(columns=["Ürün Kodu", "Ürün Adı", "Stok Miktarı", "Yeniden Sipariş Sınırı"])

# Sipariş bilgileri için ayrı bir DataFrame
if 'sipariş_df' not in st.session_state:
    st.session_state.sipariş_df = pd.DataFrame(columns=["Ürün Kodu", "Ürün Adı", "Sipariş Miktarı", "Durum"])

# Stok güncelleme ve kontrol fonksiyonu
def stok_guncelle(urun_kodu, urun_adi, miktar, yeniden_siparis_siniri):
    if urun_kodu in st.session_state.stok_df['Ürün Kodu'].values:
        st.session_state.stok_df.loc[st.session_state.stok_df['Ürün Kodu'] == urun_kodu, 'Stok Miktarı'] += miktar
    else:
        # Yeni ürün ekle
        yeni_veri = pd.DataFrame([[urun_kodu, urun_adi, miktar, yeniden_siparis_siniri]],
                                 columns=["Ürün Kodu", "Ürün Adı", "Stok Miktarı", "Yeniden Sipariş Sınırı"])
        st.session_state.stok_df = pd.concat([st.session_state.stok_df, yeni_veri], ignore_index=True)

# Sipariş kontrol fonksiyonu
def siparis_ver(urun_kodu, urun_adi, siparis_miktari):
    stok_verisi = st.session_state.stok_df.loc[st.session_state.stok_df['Ürün Kodu'] == urun_kodu]
    if not stok_verisi.empty:
        mevcut_stok = stok_verisi['Stok Miktarı'].values[0]
        if mevcut_stok >= siparis_miktari:
            # Stoktan düş
            st.session_state.stok_df.loc[st.session_state.stok_df['Ürün Kodu'] == urun_kodu, 'Stok Miktarı'] -= siparis_miktari
            durum = "Tamamlandı"
        else:
            durum = "Eksik Stok"
    else:
        durum = "Ürün Bulunamadı"
    
    # Sipariş kaydını ekle
    yeni_siparis = pd.DataFrame([[urun_kodu, urun_adi, siparis_miktari, durum]],
                                columns=["Ürün Kodu", "Ürün Adı", "Sipariş Miktarı", "Durum"])
    st.session_state.sipariş_df = pd.concat([st.session_state.sipariş_df, yeni_siparis], ignore_index=True)

# Uygulama başlığı
st.title("Mini ERP Stok ve Sipariş Yönetimi")

# Sekmeler
tab1, tab2, tab3 = st.tabs(["Stok Yönetimi", "Sipariş Yönetimi", "Stok ve Sipariş Takip"])

# Stok Yönetimi Sekmesi
with tab1:
    st.header("Stok Ekleme ve Güncelleme")
    
    # Ürün bilgilerini eklemek/güncellemek için form
    urun_adi = st.text_input("Ürün Adı")
    urun_kodu = st.text_input("Ürün Kodu")
    miktar = st.number_input("Stok Miktarı", min_value=0)
    yeniden_siparis_siniri = st.number_input("Yeniden Sipariş Sınırı", min_value=0)
    
    if st.button("Stok Ekle/Güncelle"):
        stok_guncelle(urun_kodu, urun_adi, miktar, yeniden_siparis_siniri)
        st.success(f"{urun_adi} ({urun_kodu}) başarıyla eklendi/güncellendi.")
    
    # Stokları göster
    st.subheader("Güncel Stok Durumu")
    st.write(st.session_state.stok_df)

# Sipariş Yönetimi Sekmesi
with tab2:
    st.header("Sipariş Yönetimi")
    
    # Sipariş formu
    siparis_urun_kodu = st.text_input("Sipariş Ürün Kodu")
    siparis_urun_adi = st.text_input("Sipariş Ürün Adı")
    siparis_miktari = st.number_input("Sipariş Miktarı", min_value=1)
    
    if st.button("Sipariş Ver"):
        siparis_ver(siparis_urun_kodu, siparis_urun_adi, siparis_miktari)
        st.success(f"{siparis_urun_adi} için sipariş başarıyla oluşturuldu.")
    
    # Verilen siparişleri göster
    st.subheader("Sipariş Durumları")
    st.write(st.session_state.sipariş_df)

# Stok ve Sipariş Takip Sekmesi
with tab3:
    st.header("Stok ve Sipariş Takip")
    
    # Eksik stoklar
    st.subheader("Düşük Stok Uyarıları")
    eksik_stok_df = st.session_state.stok_df[st.session_state.stok_df['Stok Miktarı'] < st.session_state.stok_df['Yeniden Sipariş Sınırı']]
    if not eksik_stok_df.empty:
        st.warning("Düşük stok seviyesine sahip ürünler:")
        st.write(eksik_stok_df)
    else:
        st.success("Tüm stoklar yeterli seviyede.")
    
    # Tüm stokları ve siparişleri göster
    st.subheader("Tüm Stoklar ve Siparişler")
    st.write("Stok Listesi:")
    st.write(st.session_state.stok_df)
    st.write("Sipariş Listesi:")
    st.write(st.session_state.sipariş_df)
