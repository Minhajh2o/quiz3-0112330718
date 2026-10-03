# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app, books

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset():
    books.clear()
    import main
    main.next_id = 1
    yield

def test_create_book():
    response = client.post("/books", json={
        "title":"Clean Code","author":"Robert Martin","price":29.99
    })
    assert response.status_code == 201   # must be 201 Created
    # write one more assert below:
    # Missing assert line
    assert response.json()["title"] == "Clean Code"

def test_delete_book():
    # Step 1: create a book first
    client.post("/books", json={
        "title":"Test","author":"Author","price":9.99})

    # Step 2: delete the book
    response = client.delete("/books/1")
    assert response.status_code == 200


    # Step 3: verify it is gone
    check = client.get("/books")
    assert len(check.json()) == 0

def test_get_all_books():
    # Step 1: create 2 books
    client.post("/books", json={"title": "Book One", "author": "Author A", "price": 10.99})
    client.post("/books", json={"title": "Book Two", "author": "Author B", "price": 15.99})
    
    # Step 2: call GET /books
    response = client.get("/books")
    
    # Step 3: assert the count is 2
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_book():
    # Step 1: create a book
    client.post("/books", json={"title": "Original Title", "author": "Author C", "price": 20.00})
    
    # Step 2: PUT with new price
    response = client.put("/books/1", json={"price": 25.00})
    
    # Step 3: assert price changed and title unchanged
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["price"] == 25.00
    assert updated_data["title"] == "Original Title"