import logging
import streamlit as st
from scripts.books_utils import get_book_details


logger = logging.getLogger(__name__)


@st.dialog('Detalhes')
def details(book_id: int) -> None:
    '''
    Exibe uma janela de diálogo com as informações detalhadas do livro especificado.

    Args:
        book_id (int): id do livro
    '''
    try:
        details = get_book_details(book_id)
        if details:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(details.get('image_url', ''), width='stretch')
            with col2:
                st.subheader(details.get('title'))
                st.write(f'**Gênero:** {details.get("genre")}')
                st.write(f'**Preço:** £{details.get("price_incl_tax")}')
            st.divider()
            st.write(details.get('description', 'Sem descrição disponível.'))
    except Exception as e:
        logger.exception(f'error: {e}')
        st.error('Erro ao carregar detalhes.')