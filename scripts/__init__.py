import logging
import streamlit as st
import requests
from streamlit_cookies_controller import CookieController
from typing import Tuple, Optional, Any, Dict


logger = logging.getLogger(__name__)


def remove_cookies() -> None:
    '''
    Remove todos os cookies de sessão relacionados à autenticação e navegação.
    '''
    controller.remove('access_token')
    controller.remove('refresh_token')
    controller.remove('user_id')
    controller.remove('username')
    controller.remove('logged_in')
    controller.remove('page')


def get_all_cookies() -> Tuple[Optional[str], Optional[int], Optional[str], Optional[bool], Optional[str]]:
    '''
    Recupera os valores de todos os cookies principais da aplicação.

    Returns:
        Uma tupla contendo as variáveis de sessão.
    '''
    return (
        controller.get('access_token'),
        controller.get('refresh_token'),
        controller.get('user_id'),
        controller.get('username'),
        controller.get('logged_in'),
        controller.get('page')
    )


def get_cookies(key: str) -> Any:
    '''
    Recupera o valor de um cookie específico através da sua chave.

    Args:
        key (str): O nome do cookie que deseja recuperar.

    Returns:
        O valor armazenado no cookie ou None se não existir.
    '''
    return controller.get(key)


def set_all_cookies(access_token: str, refresh_token: str, user_id: int, usuario: str, page: str) -> None:
    '''
    Define simultaneamente todos os cookies necessários para o estado de login.

    Args:
        token (str): Token JWT ou de acesso
        user_id (int): Identificador único do usuário
        usuario (str): Nome de exibição do usuário
        page (str): Nome da página atual para persistência de navegação
    '''
    set_cookies('access_token', access_token)
    set_cookies('refresh_token', refresh_token)
    set_cookies('user_id', user_id)
    set_cookies('username', usuario)
    set_cookies('page', page)
    set_cookies('logged_in', True)


def set_cookies(key: str, value: Any) -> None:
    '''
    Armazena um valor em um cookie específico.

    Args:
        key (str): O nome da chave do cookie.
        value (Any): O valor a ser armazenado.
    '''
    controller.set(key, value)


def api_request(
    method: str, 
    endpoint: str, 
    data: Optional[Dict[str, Any]] = None, 
    params: Optional[Dict[str, Any]] = None
) -> requests.Response:
    '''
    Gerencia a renovação do access token e executa requisições à API.

    Caso a API retorne status 401, utiliza o refresh_token para obter um novo
    access_token, atualiza os cookies e tenta a requisição novamente.

    Args:
        method (str): método HTTP desejado
        endpoint (str): endpoint da API
        data (dict, optional): corpo da requisição
        params (dict, optional): parâmetros de query string

    Returns:
        requests.Response: objeto de resposta da requisição.
    '''
    cookies = get_all_cookies()
    access_token = cookies[0]
    refresh_token = cookies[1]
    
    url = f'{URL_BASE}{endpoint}'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.request(
            method, url, json=data, params=params, headers=headers, timeout=5
        )
        if response.status_code == 401 and refresh_token:
            refresh_response = requests.post(
                f'{URL_BASE}/auth/refresh',
                headers={'Authorization': f'Bearer {refresh_token}'},
                timeout=5
            )
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access_token')
                set_cookies('access_token', new_access_token)
                headers['Authorization'] = f'Bearer {new_access_token}'
                return requests.request(
                    method, url, json=data, params=params, headers=headers, timeout=5
                )
            else:
                remove_cookies()
                st.rerun()
        return response
    except Exception as e:
        logger.error(f'error: {e}')
        raise e
    

controller = CookieController()

URL_BASE = 'http://192.168.15.9:5000/api/v1'