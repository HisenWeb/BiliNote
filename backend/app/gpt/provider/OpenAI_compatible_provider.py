from typing import Optional, Union

from openai import OpenAI

from app.utils.logger import get_logger

logging= get_logger(__name__)
class OpenAICompatibleProvider:
    def __init__(self, api_key: str, base_url: str, model: Union[str, None]=None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    @property
    def get_client(self):
        return self.client

    @staticmethod
    def test_connection(api_key: str, base_url: str) -> bool:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            # 优先用 models.list()，不支持的供应商会失败
            try:
                client.models.list()
                logging.info("连通性测试成功 (models.list)")
                return True
            except Exception:
                # models.list() 不支持的供应商（如 MiniMax），用 chat.completions 测试
                try:
                    client.chat.completions.create(
                        model="*",  # 用通配符让服务器选择可用模型
                        messages=[{"role": "user", "content": "hi"}],
                        max_tokens=1,
                    )
                    logging.info("连通性测试成功 (chat.completions)")
                    return True
                except Exception as e:
                    error_str = str(e)
                    # 5xx = 服务端问题（模型权限、额度等），不代表地址/密钥错误
                    if any(code in error_str for code in ['500', '502', '503', '504']):
                        logging.info("连通性测试成功 (服务器返回5xx，API可通)")
                        return True
                    # 400 + unknown model / invalid model = API可达，只是模型名问题
                    if 'unknown model' in error_str.lower() or 'invalid model' in error_str.lower():
                        logging.info("连通性测试成功 (API可达，模型名需指定)")
                        return True
                    # 401/403 = 认证失败，才是真正的密钥错误
                    if any(code in error_str for code in ['401', '403']):
                        logging.info(f"连通性测试失败：认证错误 {e}")
                        return False
                    raise  # 其他错误继续向上抛出
        except Exception as e:
            logging.info(f"连通性测试失败：{e}")
            return False