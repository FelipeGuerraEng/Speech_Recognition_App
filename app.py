import streamlit as st
import speech_recognition as sr
import base64

# Función para realizar el reconocimiento de voz
def reconocer_voz(idioma):
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.text("Habla algo...")
        r.adjust_for_ambient_noise(source)  # Añadido para mejorar la calidad de la grabación
        audio = r.listen(source)
        st.text("Grabación completada, reconociendo...")

    try:
        texto = r.recognize_google(audio, language=idioma)
        st.text(f"Has dicho: {texto}")
        return texto

    except sr.UnknownValueError:
        st.warning("No se pudo entender el audio.")
        return None
    except sr.RequestError as e:
        st.error(f"Error al solicitar resultados; {e}")
        return None

# Función para crear un link para descargar la transcripción como un archivo txt
def crear_link_descarga(texto):
    if texto:
        b64 = base64.b64encode(texto.encode()).decode()
        link = f'<a href="data:text/plain;charset=UTF-8;base64,{b64}" download="transcripcion.txt">Descargar transcripción</a>'
        st.markdown(link, unsafe_allow_html=True)
    else:
        st.warning("La transcripción está vacía. No se ha guardado nada.")

st.title("Reconocimiento de voz con SpeechRecognition")
st.write("Presiona el botón para hablar")

idioma = st.selectbox("Selecciona el idioma", ["es-ES", "en-US", "fr-FR", "de-DE"], index=0)

if st.button("Hablar"):
    st.text("Botón presionado, iniciando grabación...")
    texto = reconocer_voz(idioma)

    if texto:
        crear_link_descarga(texto)

