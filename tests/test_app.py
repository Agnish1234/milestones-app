from models import Milestone, db


def test_index_empty(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'No milestones yet' in response.data


def test_index_lists_existing_milestones(client, make_milestone):
    make_milestone(title='Visible milestone', description='shown')

    response = client.get('/')

    assert response.status_code == 200
    assert b'Visible milestone' in response.data
    assert b'No milestones yet' not in response.data


def test_add_milestone_creates_record(client):
    response = client.post(
        '/add',
        data={'title': 'New goal', 'description': 'details'},
    )

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')

    milestones = Milestone.query.all()
    assert len(milestones) == 1
    assert milestones[0].title == 'New goal'
    assert milestones[0].description == 'details'


def test_add_milestone_without_title_is_ignored(client):
    response = client.post('/add', data={'description': 'no title'})

    assert response.status_code == 302
    assert Milestone.query.count() == 0


def test_add_milestone_follow_redirect(client):
    response = client.post(
        '/add',
        data={'title': 'Redirected', 'description': ''},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b'Redirected' in response.data


def test_delete_milestone_removes_record(client, make_milestone):
    milestone = make_milestone(title='To delete')

    response = client.post(f'/delete/{milestone.id}')

    assert response.status_code == 302
    assert Milestone.query.count() == 0


def test_delete_missing_milestone_returns_404(client):
    response = client.post('/delete/9999')

    assert response.status_code == 404


def test_update_get_renders_form(client, make_milestone):
    milestone = make_milestone(title='Editable', description='before')

    response = client.get(f'/update/{milestone.id}')

    assert response.status_code == 200
    assert b'Editable' in response.data
    assert b'Update Milestone' in response.data


def test_update_get_missing_returns_404(client):
    response = client.get('/update/9999')

    assert response.status_code == 404


def test_update_post_modifies_record(client, make_milestone):
    milestone = make_milestone(title='Old title', description='old desc')
    original_updated = milestone.date_updated

    response = client.post(
        f'/update/{milestone.id}',
        data={'title': 'New title', 'description': 'new desc'},
    )

    assert response.status_code == 302
    refreshed = db.session.get(Milestone, milestone.id)
    assert refreshed.title == 'New title'
    assert refreshed.description == 'new desc'
    assert refreshed.date_updated >= original_updated


def test_update_post_missing_returns_404(client):
    response = client.post(
        '/update/9999',
        data={'title': 'x', 'description': 'y'},
    )

    assert response.status_code == 404


def test_init_db_cli_command(app):
    runner = app.test_cli_runner()

    result = runner.invoke(args=['init-db'])

    assert result.exit_code == 0
    assert 'Database initialized successfully!' in result.output
