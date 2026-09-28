import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"federation"/"release_contract.py"
s=importlib.util.spec_from_file_location("r",P);r=importlib.util.module_from_spec(s);assert s and s.loader;s.loader.exec_module(r)
def test_store_source_evidence_is_source_only():
    p=r.store_source_evidence_payload()
    assert p["source_verified"] is True
    assert p["artifact_built"] is False
    assert p["store_published"] is False
    assert p["deployment_authority"] is False
