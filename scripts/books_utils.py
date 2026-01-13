import logging
from scripts import api_request
from typing import List, Dict, Optional, Union, Any


logger = logging.getLogger(__name__)


def get_all_book_titles() -> List[Dict[str, str]]:
    '''
    Obtém a lista de todos os títulos de livros disponíveis.

    Returns:
        Uma lista de dicionários contendo os títulos. Ex: [{'title': '...'}].
    '''
    try:
        response = api_request('GET', '/books/titles')
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []


def get_book_details(book_id: Union[int, str]) -> Optional[Dict[str, Any]]:
    '''
    Recupera as informações detalhadas de um livro específico pelo seu ID.

    Args:
        book_id: Identificador único do livro.

    Returns:
        Dicionário com os detalhes do livro ou None se houver falha.
    '''
    try:
        response = api_request('GET', f'/books/details/{book_id}')
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f'error: {e}')
        return None


def get_books_by_search(
    title: Optional[str] = None, 
    genre: Optional[str] = None
) -> Union[List[Dict[str, Any]], Dict[str, str]]:
    '''
    Busca livros filtrando por título e/ou gênero.

    Args:
        title: Parte do título do livro (opcional).
        genre: Gênero/Categoria do livro (opcional).

    Returns:
        Lista de livros encontrados ou dicionário com mensagem de erro da API.
    '''
    params = {}
    if title: params['title'] = title
    if genre: params['genre'] = genre
    
    try:
        response = api_request('GET', '/books/search', params=params)
        if response.status_code == 200:
            return response.json()
        
        if response.status_code in [400, 404]:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []


def get_books_by_price_range(
    min_price: float, 
    max_price: float
) -> List[Dict[str, Any]]:
    '''
    Filtra livros dentro de uma faixa de preço específica.

    Args:
        min_price: Preço mínimo.
        max_price: Preço máximo.

    Returns:
        Lista de livros que atendem aos critérios de preço.
    '''
    params = {'min': min_price, 'max': max_price}
    try:
        response = api_request('GET', '/books/price-range', params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []


def get_top_rated(limit: int = 1000) -> List[Dict[str, Any]]:
    '''
    Retorna os livros com as melhores avaliações.

    Args:
        limit: Quantidade máxima de resultados (padrão: 10).

    Returns:
        Lista de livros mais bem avaliados.
    '''
    params = {'limit': limit}
    try:
        response = api_request('GET', '/books/top-rated', params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []