import streamlit as st
from groq import Groq

# Configuración inicial
st.set_page_config(page_title="Chat con Groq", layout="wide")
st.title("Mi primer chat con Streamlit")

# Modelos disponibles
modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
modelo_seleccionado = st.selectbox("Elegí un modelo de Groq", modelos)

# Inicialización del estado de la sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Función para crear cliente Groq con manejo mejorado de errores
def crear_usuario_groq():
    try:
        clave_secreta = st.secrets.get("CLAVE_API")
        if not clave_secreta:
            st.error("🔑 No se encontró la CLAVE_API en los secrets.")
            st.info("Por favor, crea un archivo .streamlit/secrets.toml con tu clave")
            st.stop()
        return Groq(api_key=clave_secreta)
    except Exception as e:
        st.error(f"❌ Error al configurar el cliente: {str(e)}")
        st.stop()

# Función para interactuar con el modelo
def obtener_respuesta_groq(cliente, modelo, historial_chat):
    try:
        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=historial_chat,
            temperature=0.7 
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        st.error(f"⚠️ Error al obtener respuesta del modelo: {str(e)}")
        return None

# Mostrar historial de chat
def mostrar_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

# Área principal del chat
def main():
    # Inicializar cliente
    cliente = crear_usuario_groq()
    
    # Mostrar historial
    mostrar_chat()
    
    # Entrada del usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        # Añadir mensaje del usuario
        st.session_state.mensajes.append({"role": "user", "content": prompt, "avatar": "🧑🏼"})
        
        with st.chat_message("user", avatar="🧑🏼"):
            st.markdown(prompt)
        
        # Obtener respuesta
        with st.spinner("El asistente está pensando..."):
            historial_para_modelo = [{"role": msg["role"], "content": msg["content"]} 
                                    for msg in st.session_state.mensajes]
            
            respuesta = obtener_respuesta_groq(cliente, modelo_seleccionado, historial_para_modelo)
            
            if respuesta:
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta, "avatar": "🤖"})
                
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(respuesta)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()

#py -m streamlit run chatbot_tech.py
#poner ese codigo en la terminal para ejecutarlo localmente