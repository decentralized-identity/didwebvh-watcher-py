from did_webvh.core.resolver import DidResolver, HistoryVerifier
from did_webvh.resolver import resolve_did
from did_webvh.history import did_base_url

import requests


class WebVhProcessor:
    def __init__(self):
        self.resolver = DidResolver(HistoryVerifier())

    async def resolve(self, did: str) -> None | dict:
        results = await resolve_did(did)
        return results.document

    def get_log_file(self, did: str) -> str:
        r = requests.get(f"{did_base_url(did)}did.jsonl")
        return r.text if r.status_code == 200 else ""

    def get_witness_file(self, did: str) -> list | dict:
        r = requests.get(f"{did_base_url(did)}did-witness.json")
        return r.json() if r.status_code == 200 else []

    def get_resource(self, did: str, resource_path: str) -> tuple:
        resource_path = resource_path.lstrip("/")
        r = requests.get(f"{did_base_url(did)}{resource_path}")
        return (
            (r.text, r.headers.get("content-type", "text/plain"))
            if r.status_code == 200
            else (None, None)
        )
