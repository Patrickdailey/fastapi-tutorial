from typing import List

import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    r = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, r.json())
    posts_list = list(posts_map)

    assert len(r.json()) == len(test_posts)
    assert r.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    r = client.get("/posts/")
    assert r.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    r = client.get(f"/posts/{test_posts[0].id}")
    assert r.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    r = authorized_client.get(f"/posts/997999")
    assert r.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    r = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostOut(**r.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("Fav pizza", "pizzacontent", False),
        ("fishy title", "awesome fish", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    r = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.Post(**r.json())
    assert r.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    r = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )

    created_post = schemas.Post(**r.json())
    assert r.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    r = client.get(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )
    assert r.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    r = client.delete(f"/posts/{test_posts[0].id}")

    assert r.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    r = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert r.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    r = authorized_client.delete(f"/posts/99989899")

    assert r.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    r = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert r.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    r = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**r.json())

    assert r.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    r = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert r.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    r = client.put(f"/posts/{test_posts[0].id}")

    assert r.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    r = authorized_client.put(f"/posts/99989899", json=data)

    assert r.status_code == 404
