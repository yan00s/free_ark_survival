import json
import time
import steam.webauth as wa
from steampy.guard import generate_one_time_code
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def main():
    with open(r'accounts.txt', 'r') as f:
        accounts = f.read().split('\n')
    mafiles_on = int(input('ACC WITH MAFILES? (0 || 1): '))
    for index, account in enumerate(accounts):
        try:
            if len(account) < 5 or not ':' in account: continue
            username = account.split(":")[0]
            password = account.split(":")[1]
            mafilees = (f"mafiles\{username}.maFile")
            user = wa.WebAuth(username)
            one_time_authentication_code = None
            if mafiles_on == 1:
                with open(mafilees,'r',encoding='UTF-8') as f:
                    content:dict = json.load(f)
                    shared_secret = content.get('shared_secret')
                    identity_secret = content.get('identity_secret')
                steamid = str(content.get('Session')['SteamID'])
                one_time_authentication_code = generate_one_time_code(shared_secret)
            try:
                user.login(password,twofactor_code=one_time_authentication_code)
            except Exception as exp:
                if isinstance(exp, wa.LoginIncorrect):
                    logging.warning(f"[ {username} ] акк не валид")
                    continue
                if isinstance(exp, wa.CaptchaRequired):
                    input(f"[ {username} ] требует капчу, меняй айпи")
                time.sleep(5)
                continue
            su = user.logged_on
            if su == True:
                try:
                    data = {
                                'snr': '1_5_9__403',
                                'originating_snr': '1_store-navigation__',
                                'action': 'add_to_cart',
                                'sessionid': user.session.cookies.get('sessionid', domain='store.steampowered.com'),
                                'subid': '734115',
                            }
                    resp = user.session.post('https://store.steampowered.com/checkout/addfreelicense/', data=data)
                    logging.info(f'[ {username} ][{index+1}/{len(accounts)}] ARK ADD TO ACCOUNT = {resp.status_code}')
                    time.sleep(1)
                except Exception as e:
                    err = f'[{username}] ERROR {e}'
                    logging.warning(err)
                    time.sleep(4)
            else:
                logging.warning(f"[ {username} ] всё плохо с данным акком спасаай")
                time.sleep(4)
        except Exception as e:
            logging.warning(f'Произошла неизвестная ошибка {e}')
            time.sleep(4)
    for _ in range(5):
        logging.info('FINISH')
        input()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.warning(e)
        input()