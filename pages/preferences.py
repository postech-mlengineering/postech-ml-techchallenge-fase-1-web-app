import logging
import streamlit as st
from scripts.books_utils import get_top_rated
from scripts.ml_utils import input_user_preferences
from scripts import get_all_cookies, set_cookies
from . import details
import time


logger = logging.getLogger(__name__)


def show() -> None:
    '''Conteúdo da página de personalização'''
    #gerenciando sessao
    _, _, _, _, logged_in, _ = get_all_cookies()
    if not logged_in:
        set_cookies('page', 'login')
        st.rerun()

    #inicializa o estado do gênero
    if 'selected_genre' not in st.session_state:
        st.session_state.selected_genre = None
        
    #título
    col1, col2 = st.columns([.05, .95])
    with col1:
        st.image('img/collection.png', width='stretch')
    with col2:
        st.title('BooksToScrape | Preferências')
    _, col2 = st.columns([0.9, 0.1])
    st.markdown('#### Favorite um título para receber recomendações incríveis! ✨')
    st.markdown('---')

    #inicializa o acervo completo
    if 'books_collection' not in st.session_state:
        st.session_state.books_collection = get_top_rated()
    
    all_books = st.session_state.books_collection

    #gêneros
    if st.session_state.selected_genre is None:
        st.markdown('#### Gêneros')
        st.markdown('')
        if all_books and isinstance(all_books, list):
            genres = sorted(list(set(book.get('genre') for book in all_books if book.get('genre'))))
            
            n_cols = 5
            for i in range(0, len(genres), n_cols):
                row_genres = genres[i : i + n_cols]
                cols = st.columns(n_cols)
                for j, g_name in enumerate(row_genres):
                    with cols[j]:
                        if st.button(g_name, key=f'btn_gen_{g_name}', width='stretch'):
                            st.session_state.selected_genre = g_name
                            st.rerun()
        else:
            st.warning('Nenhum dado disponível para listar gêneros.')

    #acervo
    else:
        _, col2 = st.columns([0.9, 0.1])
        with col2:
            if st.button('←', help='Voltar aos Gêneros', width='stretch'):
                st.session_state.selected_genre = None
                st.rerun()
        st.markdown(f'#### Gênero: {st.session_state.selected_genre}')
        books = [b for b in all_books if b.get('genre') == st.session_state.selected_genre]
        if not books:
            st.warning('Nenhum livro encontrado para este gênero.')
            if st.button('Voltar'):
                st.session_state.selected_genre = None
                st.rerun()
        else:
            st.write(f'**{len(books)}** resultado(s)')
            for i in range(0, len(books), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(books):
                        book = books[i + j]
                        book_id = book.get('id') 
                        with cols[j]:
                            with st.container(border=True):
                                url_img = book.get('image_url') or 'https://via.placeholder.com/150x200?text=Sem+Capa'
                                st.markdown(
                                    f'''
                                        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                                            <img src="{url_img}" style="height: 200px; object-fit: contain; border-radius: 4px;">
                                        </div>
                                    ''', 
                                    unsafe_allow_html=True
                                )
                                book_title = book.get('title', 'Sem título')
                                st.markdown(f'**{book_title[:35]}...**' if len(book_title) > 35 else f'**{book_title}**')
                                st.write(f'£{book.get("price")}')
                                if book.get('rating'):
                                    st.caption(f'⭐ {book.get("rating")}')
                                
                                if st.button('Detalhes', key=f'btn_{book_id}_{i+j}', width='stretch'):
                                    details(book_id)
                                if st.button('Favoritar', key=f'ml_{book_id}_{i+j}', width='stretch', type='primary'):
                                    try:
                                        _, error_msg = input_user_preferences(book_id)
                                        if error_msg:
                                            st.error(f'Erro: {error_msg}')
                                        else:
                                            st.toast('Experiência personalizada! ✨')
                                            keys_to_clear = ['user_prefs', 'pref_index', 'books_collection', 'selected_genre']
                                            for key in keys_to_clear:
                                                if key in st.session_state:
                                                    del st.session_state[key]
                                            time.sleep(2)
                                            set_cookies('page', 'menu') 
                                            st.session_state.page = 'menu' # Sincronização necessária
                                            st.rerun()
                                    except Exception as e:
                                        logger.error(f'Erro ao salvar preferência: {e}')
                                        st.error('Erro ao processar sua escolha.')