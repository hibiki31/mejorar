import logging


def setup_logger(name):
    logger = logging.getLogger(name)

    # コンソール出力設定
    ch = logging.StreamHandler()
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    logger.addHandler(ch)

    # 全体のログレベル
    logger.setLevel(logging.DEBUG)

    # コンソール出力のログレベル
    ch.setLevel(logging.INFO)

    return logger