import logging
import streamlit as st
from scripts.auth_utils import register
from scripts import set_cookies


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
                        #gerenciando sessao
                        set_cookies('access_token', data.get('access_token'))
                        set_cookies('user_id', str(data.get('user_id')))
                        set_cookies('username', new_user)
                        set_cookies('logged_in', True)
                        set_cookies('page', 'preferences') 
                        st.rerun()
                    else:
                        st.error(data)
        if st.button('Já tem uma conta? Faça Login', width='stretch'):
            set_cookies('page', 'login') 
            st.rerun()