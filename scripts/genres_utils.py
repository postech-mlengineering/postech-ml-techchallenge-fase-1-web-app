import logging
from scripts import api_request
from typing import List, Dict


logger = logging.getLogger(__name__)


def get_all_genres() -> List[Dict[str, str]]:
    '''
    Retorna lista com todos os gêneros de livros cadastrados.

    Returns:
        Uma lista de dicionários contendo os gêneros
    '''
    try:
        response = api_request('GET', '/genres')
        
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []