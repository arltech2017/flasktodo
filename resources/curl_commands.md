# Interacting with Flask via Curl

## To test the GET functions:

    curl -i http://localhost:8080/todo/api/v1.0/tasks
    curl -i http://localhost:8080/todo/api/v1.0/tasks/1
    curl -i http://localhost:8080/todo/api/v1.0/tasks/2
    curl -i http://localhost:8080/todo/api/v1.0/tasks/3

## To test the POST function:

    curl -i -H "Content-Type: application/json"  \
            -X POST                              \
            -d '{"title":"Read a book"}'         \
            http://localhost:8080/todo/api/v1.0/tasks
    curl -i http://localhost:8080/todo/api/v1.0/tasks

## To test the DELETE function:

    curl -i -H "Content-Type: application/json"  \
            -X DELETE                            \
            http://localhost:5000/todo/api/v1.0/tasks/3
    curl -i http://localhost:8080/todo/api/v1.0/tasks

## To test the PUT function:

    curl -i -H "Content-Type: application/json"  \
            -X PUT                               \
            -d '{"done":true}'                   \
            http://localhost:5000/todo/api/v1.0/tasks/2
    curl -i http://localhost:8080/todo/api/v1.0/tasks
