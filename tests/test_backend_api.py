import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / 'backend'))
os.environ['DATABASE_URL'] = f"sqlite:///{ROOT / 'tests' / 'test.db'}"

from app.database.base import Base  # noqa: E402
from app.database.session import engine  # noqa: E402
from app.main import app  # noqa: E402

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def _auth_headers(email='user@example.com', password='secret123'):
    client.post('/api/v1/auth/signup', json={'name': 'User', 'email': email, 'password': password})
    res = client.post('/api/v1/auth/login', json={'email': email, 'password': password})
    token = res.json()['data']['access_token']
    return {'X-Auth-Token': token}


def test_health_route():
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json()['success'] is True


def test_auth_and_protected_dashboard_flow():
    headers = _auth_headers('dashboard@example.com')
    response = client.get('/api/v1/dashboard/summary', headers=headers)
    assert response.status_code == 200
    payload = response.json()
    assert payload['success'] is True
    assert 'cards' in payload['data']


def test_resume_analyzer_and_job_tracker():
    headers = _auth_headers('feature@example.com')

    resume_payload = {
        'resume_text': 'Software engineer with 3 years of Python and React experience. Improved API latency by 42 percent.'
    }
    resume_response = client.post('/api/v1/resume/analyze', headers=headers, json=resume_payload)
    assert resume_response.status_code == 200
    assert 'overall_score' in resume_response.json()['data']

    create_job = client.post('/api/v1/jobs', headers=headers, json={'company': 'Acme', 'role': 'Backend Engineer', 'status': 'Wishlist'})
    assert create_job.status_code == 200
    job_id = create_job.json()['data']['id']

    update_job = client.patch(f'/api/v1/jobs/{job_id}', headers=headers, json={'status': 'Applied'})
    assert update_job.status_code == 200
    assert update_job.json()['data']['status'] == 'Applied'
