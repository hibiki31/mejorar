
## よく使うコマンド

```bash
# 差分ファイル作成
alembic revision --autogenerate
alembic revision --autogenerate -m "Added columns."
# データベースに適応
alembic upgrade head
# すべて削除
alembic downgrade base
```

lH3-A74D4zjqOkNm


## 参考記事

- FastAPI+SQLAlchemy+Alembic
  - https://zenn.dev/satonopan/articles/4256417e6c629e
  - https://zenn.dev/yusugomori/articles/a3d5dc8baf9e386a58e5

- 命名規則
  - https://qiita.com/genzouw/items/35022fa96c120e67c637
  - https://zenn.dev/chelproc/articles/4f1da698779f67