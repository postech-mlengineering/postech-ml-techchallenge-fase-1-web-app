import logging
import streamlit as st
from scripts.auth_utils import register
from scripts import set_cookies, get_all_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    '''Conteúdo da página de cadastro'''
    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        _, col2, _ = st.columns([.2, .6, .2])
        with col2:
            col1, col2 = st.columns([.22, .78])
            with col1:
                st.image('img/collection.png', width='stretch')
            with col2:
                st.title('BooksToScrape')
        
        st.subheader('Cadastro')
        with st.form('form_cadastro', clear_on_submit=True):
            user = st.text_input('Usuário', placeholder='Digite nome de usuário desejado')
            password = st.text_input('Senha', placeholder='Digite uma senha', type='password')
            _, col2 = st.columns([.7, .3])
            with col2:
                btn_register = st.form_submit_button('Cadastrar', width='stretch')
            if btn_register:
                if not user or not password:
                    st.error('Por favor, preencha todos os campos.')
                else:
                    success, data = register(user, password)
                    if success:
                        set_cookies('page', 'preferences')
                        st.rerun()
                    else:
                        st.error(data)
        if st.button('Já tem uma conta? Faça Login', width='stretch'):
            set_cookies('page', 'login')
            st.rerun()