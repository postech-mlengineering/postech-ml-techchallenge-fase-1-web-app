import logging
from scripts import api_request
from typing import List, Dict, Optional, Any


logger = logging.getLogger(__name__)


def get_stats_overview() -> Optional[Dict[str, Any]]:
    '''
    Retorna indicadores gerais e a distribuição de avaliações do acervo.

    Returns:
        Um dicionário contendo:
            - avg_price (float): média de preço de todos os livros
            - total (int): quantidade total de registros
            - rating_distribution (list): Lista de dicts com 'rating' e 'count'
    '''
    try:
        response = api_request('GET', '/stats/overview')
        
        if response.status_code == 200:
            return response.json()
        
        logger.warning(f'Falha ao obter overview. Status: {response.status_code}')
        return None
    except Exception as e:
        logger.error(f'Erro ao buscar overview de stats: {e}')
        return None


def get_stats_by_genre() -> List[Dict[str, Any]]:
    '''
    Retorna métricas detalhadas agrupadas por gênero.

    Returns:
        Uma lista de dicionários, onde cada item contém:
            - genre (str): Nome do gênero
            - avg_price (float): Média de preço naquela categoria
    '''
    try:
        response = api_request('GET', '/stats/genres')
        
        if response.status_code == 200:
            return response.json()
        
        logger.warning(f'Falha ao obter estatísticas por gênero. Status: {response.status_code}')
        return []
    except Exception as e:
        logger.error(f'Erro ao buscar estatísticas por gênero: {e}')
        return []