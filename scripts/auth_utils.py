import logging
import requests
from scripts import set_all_cookies, URL_BASE
from typing import Tuple, Optional, Union, Dict, Any


logger = logging.getLogger(__name__)


def login(usuario: str, senha: str) -> Tuple[Optional[str], Optional[str]]:
    '''
    Realiza a autenticação do usuário e retorna tokens autenticação e id do usuário.

    Returns:
        Uma tupla contendo os tokens, id do usuário e mensagem de erro
    '''
    try:
        response = requests.post(
            f'{URL_BASE}/auth/login', 
            json={'username': usuario, 'password': senha}, 
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            user_id = data.get('user_id')
            
            set_all_cookies(access_token, refresh_token, user_id, usuario, 'menu')
            
            return access_token, None
        try:
            data = response.json()
            error_msg = data.get('error', 'Credenciais inválidas.')
        except Exception:
            error_msg = f'Erro no servidor (Status {response.status_code})'
        return None, error_msg
    except requests.exceptions.ConnectionError:
        logger.error(f'Falha de conexão: {URL_BASE}')
        return None, 'Não foi possível conectar ao servidor.'
    except Exception as e:
        logger.error(f'error: {e}')
        return None, f'error: {str(e)}'


def register(usuario: str, senha: str) -> Tuple[bool, Union[str, Dict[str, Any]]]:
    '''
    Cria uma nova conta de usuário no sistema e retorna tokens de autenticação.

    Args:
        usuario: nome de usuário desejado
        senha: senha para a nova conta

    Returns:
        Uma tupla contendo (True/False, retorno da API)
    '''
    try:
        response = requests.post(
            f'{URL_BASE}/auth/register', 
            json={'username': usuario, 'password': senha}, 
            timeout=5
        )
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            return False, f'Resposta inválida do servidor (Status: {response.status_code}).'

        if response.status_code == 201:
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            user_id = data.get('user_id')
            
            if access_token:
                set_all_cookies(access_token, refresh_token, user_id, usuario, 'menu')
                
            return True, data
        return False, data.get('error', 'Falha ao realizar o registro.')
    except requests.exceptions.ConnectionError:
        logger.error(f'Falha de conexão em register: {URL_BASE}')
        return False, 'Erro de conexão: servidor offline.'
    except Exception as e:
        logger.error(f'Erro inesperado no registro: {e}')
        return False, f'Erro inesperado: {str(e)}'