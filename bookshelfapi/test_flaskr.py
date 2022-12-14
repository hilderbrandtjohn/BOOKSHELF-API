import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book

#This class represents the trivia test case
class BookTestCase(unittest.TestCase):
    
    #define test variables and initialize the app
    def setUp(self):
        self.app= create_app()
        self.client= self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            "postgres","0723368444","localhost:5432",self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title":"Anansi Boys", "author":"Neil Gaiman","rating":"5" }

        #binds the app to the current context
        with self.app.app_context():
            self.db =SQLAlchemy()
            self.db.init_app(self.app)
            #create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass
    
    def test_get_paginated_books(self):
        #set up response by client getting that endpoint.
        res =self.client().get("/books")
        data =json.loads(res.data) #load the data using json.loads

        #use assert to check the response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        #requested a get to /books for page 1,000
        res=self.client().get("/books?page=1000", json={"rating": 1} )
        data=json.loads(res.data)

        #use assert to check the response
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resourse not found")

    def test_get_book_search_with_results(self):
        #Setup response||Looking at the entire collection||endpoint we expect /books||JSON body that contains search argument with a value
        res=self.client().post("/books", json={"search":"Novel"}) #get response data
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["total_books"])
        self.assertEqual(len(data["books"]), 4)

    def test_get_book_search_without_results(self):
        #JSON body that contains search argument with a value we know is not in the database
        res=self.client().post("/books", json={"search":"caucasian"})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_books"], 0)
        self.assertEqual(len(data["books"]), 0)


    def test_update_book_rating(self):
        res = self.client().patch("/books/5", json={"rating":1})
        data = json.loads(res.data)
        book= Book.query.filter(Book.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertEqual(book.format()["rating"], 1)

    def test_400_for_failed_update(self):
        res =self.client().patch("/books/5")
        data =json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_create_new_book(self):
        res = self.client().post("/books", json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["books"]))

    def test_405_if_book_creation_not_allowed(self):
        res = self.client().post("/books/45", json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    #Delete a different book in each attempt
    def test_delete_book(self):
        res = self.client().delete("/books/3")
        data = json.loads(res.data) #include JSON body created in setup

        book = Book.query.filter(Book.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 3)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))
        self.assertEqual(book, None)

    def test_422_if_book_does_not_exist(self):
        res = self.client().delete("/books/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")



if __name__ == "__main__":
    unittest.main()