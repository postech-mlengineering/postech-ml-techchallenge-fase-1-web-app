import logging
from scripts import api_request
from typing import List, Dict, Tuple, Optional, Any


logger = logging.getLogger(__name__)


def get_user_preferences(user_id: int) -> Optional[List[Dict[str, Any]]]:
    '''
    Retorna as recomendações do usuário especificado.

    Args:
        user_id: id do usuário.

    Returns:
        Lista de dicionários com as recomendações com detalhes dos livros
    '''
    try:
        response = api_request('GET', f'/ml/user-preferences/{user_id}')
        
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            logger.warning(f'Nenhum histórico encontrado para o usuário id {user_id}.')
            return []
            
        logger.error(f'error: {response.status_code} - {response.text}')
        return None
    except Exception as e:
        logger.error(f'error: {e}')
        return None


def input_user_preferences(book_id: int) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    '''
    Envia o título do livro favoritado para a API para gerar e salvar recomendações.

    Args:
        book_id: id do livro

    Returns:
        Uma tupla contendo a lista de recomendações geradas e mensagem de erro
    '''
    try:
        from scripts.books_utils import get_book_details
        detalhes = get_book_details(book_id)
        if not detalhes:
            return None, 'Erro na API ao recuperar detalhes do livro'

        book_title = detalhes.get('title')
        payload = {'title': book_title}
        
        response = api_request('GET', '/ml/predictions', data=payload)
        
        if response.status_code == 200:
            return response.json(), None
        try:
            error_msg = response.json().get("error", 'Erro ao processar recomendações.')
        except:
            error_msg = f'Erro no servidor (Status {response.status_code})'
        return None, error_msg
    except Exception as e:
        logger.error(f'error: {e}')
        return None, str(e)