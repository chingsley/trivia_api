#!/bin/bash


psql trivia \
    -U postgres \
    -p 5432 \
    -h 127.0.0.1 \
    -c "\copy questions from './seed/questions.csv' with DELIMITER ';' CSV"


psql trivia \
    -U postgres \
    -p 5432 \
    -h 127.0.0.1 \
    -c "\copy categories from './seed/categories.csv' with DELIMITER ',' CSV"

psql trivia \
    -U postgres \
    -p 5432 \
    -h 127.0.0.1 \
    -c "SELECT setval('questions_id_seq', COALESCE((SELECT MAX(id)+1 FROM questions), 1), false)"

psql trivia \
    -U postgres \
    -p 5432 \
    -h 127.0.0.1 \
    -c "SELECT setval('categories_id_seq', COALESCE((SELECT MAX(id)+1 FROM categories), 1), false)"