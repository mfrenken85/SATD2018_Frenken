drop table if exists processed_comment;
CREATE TABLE processed_comment (
    id serial primary key,
    commentClassId integer,
    startLine integer,
    endLine integer,
    commentText text,
    commentType text,
    location text,
    description text,
    dictionary_hit text,
    jdeodorant_hit text,
    refactoring_list_name text,
    textual_similarity numeric,
    treated_commenttext text,
    classification text


);

drop table if exists comment_class;
create table comment_class (
    id serial primary key,
    projectName text,
    fileName text,
    className text,
    access text,
    isAbstract text,
    isEnum text,
    isInterface text,
    startline integer,
    endline integer,
    analyzed integer
);