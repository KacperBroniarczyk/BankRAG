import streamlit as st

try:
    # certyfikaty z systemu (Windows), bez tego połączenie z API kończy się CERTIFICATE_VERIFY_FAILED
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

from asystent import K, ODMOWA, PROG, odpowiedz, wczytaj_indeks

st.set_page_config(page_title="BankRAG", page_icon="🏦")


@st.cache_resource
def indeks():
    return wczytaj_indeks()


st.title("🏦 BankRAG")
st.caption(
    "Asystent pracownika banku: odpowiada na pytania o regulamin kont "
    "dla klientów indywidualnych, zawsze z numerem strony źródłowej."
)

try:
    fragmenty, macierz = indeks()
except (FileNotFoundError, ValueError) as e:
    st.error(f"Nie udało się wczytać indeksu: {e}")
    st.info("Uruchom najpierw `python podziel_fragmenty.py` i `python embedding.py`.")
    st.stop()

with st.sidebar:
    st.header("Ustawienia")
    prog = st.slider("Próg podobieństwa", 0.0, 1.0, PROG, 0.01,
                     help="Poniżej progu asystent odmawia bez wywoływania modelu.")
    k = st.slider("Liczba fragmentów (top-k)", 1, 10, K)
    pokaz_fragmenty = st.checkbox("Pokaż znalezione fragmenty", value=True)
    st.divider()
    st.write(f"Fragmentów w indeksie: **{len(fragmenty)}**")
    if st.button("Wyczyść rozmowę"):
        st.session_state.historia = []
    st.warning("Nie wpisuj danych osobowych klientów: pytania trafiają do zewnętrznego API.")

if "historia" not in st.session_state:
    st.session_state.historia = []


def pokaz_wynik(wynik):
    st.markdown(wynik["odpowiedz"])
    if wynik["zrodla"]:
        st.caption("Źródła: strony " + ", ".join(str(s) for s in wynik["zrodla"]))
    if pokaz_fragmenty and wynik["trafienia"]:
        with st.expander("Znalezione fragmenty"):
            for indeks_fragmentu, podobienstwo in wynik["trafienia"]:
                fragment = fragmenty[indeks_fragmentu]
                znak = "✅" if podobienstwo >= wynik["prog"] else "⛔"
                st.markdown(f"{znak} **strona {fragment['strona']}** · podobieństwo `{podobienstwo:.3f}`")
                st.text(fragment["tekst"])


for wpis in st.session_state.historia:
    with st.chat_message("user"):
        st.markdown(wpis["pytanie"])
    with st.chat_message("assistant"):
        pokaz_wynik(wpis["wynik"])

pytanie = st.chat_input("Zadaj pytanie o regulamin, np. Kto może dysponować pieniędzmi na koncie?")

if pytanie:
    with st.chat_message("user"):
        st.markdown(pytanie)
    with st.chat_message("assistant"):
        with st.spinner("Szukam w regulaminie..."):
            try:
                wynik = odpowiedz(pytanie, fragmenty, macierz, prog=prog, k=k)
            except Exception as e:
                st.error(f"Błąd API: {e}")
                st.stop()
        wynik["prog"] = prog
        if wynik["odpowiedz"] == ODMOWA and not wynik["zrodla"]:
            wynik["odpowiedz"] = f"🤷 {ODMOWA}"
        pokaz_wynik(wynik)
    st.session_state.historia.append({"pytanie": pytanie, "wynik": wynik})
