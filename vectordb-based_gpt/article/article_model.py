import os
import time
import uuid
from dotenv import load_dotenv
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

load_dotenv("../.env")


class ArticleModel(Model):
    class Meta:
        region = "ap-northeast-1"
        table_name = "Article"
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    id = UnicodeAttribute(null=False)
    pinecone_id = UnicodeAttribute(null=False)
    summary = UnicodeAttribute(null=False)
    category_id = UnicodeAttribute(range_key=True, null=False)
    deleted = NumberAttribute(hash_key=True, default=0, null=False)
    created_at = NumberAttribute(null=False)
    updated_at = NumberAttribute(null=False)
    created_by = UnicodeAttribute(null=False)
    updated_by = UnicodeAttribute(null=False)

    def __init__(self, *args, **kwargs):
        super(ArticleModel, self).__init__(*args, **kwargs)
        if kwargs.get("id") is None:
            self.id = str(uuid.uuid4())
        self.created_at = int(time.time())

    def save(self, conditional_operator=None, **expected_values):
        self.updated_at = int(time.time())
        super(ArticleModel, self).save(conditional_operator, **expected_values)


class DynamoDBManager:
    def __init__(self, model):
        self.model = model

    def setup(self):
        if not self.model.exists():
            self.model.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


manager = DynamoDBManager(ArticleModel)
manager.setup()
