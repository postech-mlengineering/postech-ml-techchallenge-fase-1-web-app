import logging
import streamlit as st
from scripts.auth_utils import login
from scripts import get_all_cookies, set_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    '''Conteúdo da página de login'''
    _, _, _, _, logged_in, _ = get_all_cookies()
    if logged_in and st.session_state.get('page') != 'register':
        st.session_state.logged_in = True
        set_cookies('page', 'menu')
        st.rerun()

    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        _, col_img, _ = st.columns([.2, .6, .2])
        with col_img:
            col1, col2_title = st.columns([.22, .78])
            with col1:
                st.image('img/logo.png', width='stretch')
            with col2_title:
                st.title('BooksToScrape')
        st.subheader('Entrar')
        with st.form('form_login'):
            user = st.text_input('Usuário')
            password = st.text_input('Senha', type='password')
            _, col2 = st.columns([.7, .3])
            with col2:
                btn_login = st.form_submit_button('Entrar', width='stretch')
            if btn_login:
                success, error_msg = login(user, password)
                if success:
                    st.rerun()
                else:
                    st.error(error_msg)
        st.write('Não possui uma conta?')
        if st.button('Cadastre-se', width='stretch'):
            set_cookies('page', 'register') 
            st.rerun()