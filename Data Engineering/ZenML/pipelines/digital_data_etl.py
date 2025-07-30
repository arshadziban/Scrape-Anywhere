from zenml import pipeline
from steps.etl import get_or_create_user, crawl_links

@pipeline
def digital_data_etl(user_full_name: str, links: list[str]):
    user = get_or_create_user(user_full_name)
    crawl_links(user=user, links=links)
