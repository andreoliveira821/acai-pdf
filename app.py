import streamlit as st
import os
import tempfile
from docx2pdf import convert as docx_to_pdf
from pdf2docx import Converter as PDFToDocx
from pdf2image import convert_from_path

# Configuração da página do navegador
st.set_page_config(page_title="Açaí PDF - Conversor Inteligente", page_icon="Açaí PDF.png", layout="centered")

# Cabeçalho do aplicativo
# Criamos duas colunas: Primeira Estreita (1) para a imagem, Segunda Larga (5) para o título e subtítulo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("Açaí PDF.png", width=100)
with col2:
    st.title("Açaí PDF")
    st.subheader("O conversor de arquivos mais forte e rápido da região!")
    st.caption("⚡ Desenvolvido por *André Oliveira*")
# Menu lateral de ferramentas
st.sidebar.title("🛠️ Ferramentas")
opcao = st.sidebar.radio(
    "Escolha o que deseja fazer:",
    ["Word para PDF", "PDF para Word", "PDF para Imagem (JPG)"]
)

# Criar um diretório temporário seguro para processar os arquivos
with tempfile.TemporaryDirectory() as pasta_temp:

    if opcao == "Word para PDF":
        st.header("🗂️ Converter Word para PDF")
        arquivo_enviado = st.file_uploader("Arraste seu arquivo .docx aqui", type=["docx"])

        if arquivo_enviado is not None:
            caminho_docx = os.path.join(pasta_temp, arquivo_enviado.name)
            caminho_pdf = os.path.join(pasta_temp, os.path.splitext(arquivo_enviado.name)[0] + ".pdf")
            
            # Salva o arquivo enviado temporariamente
            with open(caminho_docx, "wb") as f:
                f.write(arquivo_enviado.getbuffer())

            if st.button("Converter para PDF"):
                with st.spinner("Processando... O Word abrirá em segundo plano."):
                    try:
                        docx_to_pdf(caminho_docx, caminho_pdf)
                        st.success("Convertido com sucesso!")
                        
                        # Botão para o usuário baixar o resultado
                        with open(caminho_pdf, "rb") as pdf_file:
                            st.download_button(
                                label="📥 Baixar PDF Convertido",
                                data=pdf_file,
                                file_name=os.path.basename(caminho_pdf),
                                mime="application/pdf"
                            )
                    except Exception as e:
                        st.error(f"Erro na conversão: {e}")

    elif opcao == "PDF para Word":
        st.header("📝 Converter PDF para Word")
        arquivo_enviado = st.file_uploader("Arraste seu arquivo .pdf aqui", type=["pdf"])

        if arquivo_enviado is not None:
            caminho_pdf = os.path.join(pasta_temp, arquivo_enviado.name)
            caminho_docx = os.path.join(pasta_temp, os.path.splitext(arquivo_enviado.name)[0] + ".docx")
            
            with open(caminho_pdf, "wb") as f:
                f.write(arquivo_enviado.getbuffer())

            if st.button("Converter para Word (.docx)"):
                with st.spinner("Extraindo textos e formatação..."):
                    try:
                        cv = PDFToDocx(caminho_pdf)
                        cv.convert(caminho_docx, start=0, end=None)
                        cv.close()
                        st.success("Convertido com sucesso!")
                        
                        with open(caminho_docx, "rb") as docx_file:
                            st.download_button(
                                label="📥 Baixar Arquivo Word",
                                data=docx_file,
                                file_name=os.path.basename(caminho_docx),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    except Exception as e:
                        st.error(f"Erro na conversão: {e}")

    elif opcao == "PDF para Imagem (JPG)":
        st.header("🖼️ Converter PDF para Imagem")
        arquivo_enviado = st.file_uploader("Arraste seu arquivo .pdf aqui", type=["pdf"])

        if arquivo_enviado is not None:
            caminho_pdf = os.path.join(pasta_temp, arquivo_enviado.name)
            
            with open(caminho_pdf, "wb") as f:
                f.write(arquivo_enviado.getbuffer())

            if st.button("Renderizar Páginas em JPG"):
                with st.spinner("Gerando imagens..."):
                    try:
                        paginas = convert_from_path(caminho_pdf, poppler_path=r"C:\poppler-24.02.0\Library\bin")  # Certifique-se de que o Poppler está configurado corretamente
                        st.success(f"Sucesso! {len(paginas)} página(s) convertida(s).")
                        
                        # Exibe as imagens na tela e oferece o download de cada uma
                        for i, pagina in enumerate(paginas):
                            nome_img = f"pagina_{i+1}.jpg"
                            caminho_img = os.path.join(pasta_temp, nome_img)
                            pagina.save(caminho_img, "JPEG")
                            
                            st.image(caminho_img, caption=f"Página {i+1}", use_container_width=True)
                            
                            with open(caminho_img, "rb") as img_file:
                                st.download_button(
                                    label=f"📥 Baixar Página {i+1}",
                                    data=img_file,
                                    file_name=nome_img,
                                    mime="image/jpeg",
                                    key=f"btn_{i}"
                                )
                    except Exception as e:
                        st.error(f"Erro na conversão: {e}. Certifique-se de que o Poppler está configurado.")