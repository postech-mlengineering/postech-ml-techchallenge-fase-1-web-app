import logging
import streamlit as st
from scripts.auth_utils import register
from scripts import set_cookies, get_all_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    '''Conteúdo da página de cadastro'''
    _, _, _, _, logged_in, _ = get_all_cookies()
    if not logged_in:
        st.session_state.page = 'login'
        st.rerun()
    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        _, col_img, _ = st.columns([.2, .6, .2])
        with col_img:
            col1, col2_title = st.columns([.22, .78])
            with col1:
                st.image('img/collection.png', width='stretch')
            with col2_title:
                st.title('BooksToScrape')
        
        st.subheader('Cadastro')
        with st.form('form_cadastro', clear_on_submit=True):
            new_user = st.text_input('Usuário', placeholder='Digite nome de usuário desejado')
            new_password = st.text_input('Senha', placeholder='Digite uma senha', type='password')
            _, col2 = st.columns([.7, .3])
            with col2:
                cadastrar = st.form_submit_button('Cadastrar', width='stretch')
            if cadastrar:
                if not new_user or not new_password:
                    st.error('Por favor, preencha todos os campos.')
                else:
                    success, data = register(new_user, new_password)
                    if success:
                        set_cookies('page', 'preferences')
                        st.session_state.page = 'preferences'
                        st.rerun()
                    else:
                        st.error(data)