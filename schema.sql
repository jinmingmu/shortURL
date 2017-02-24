drop table if exists URLTable;
create table URLTable (
  id integer primary key autoincrement,
  longURL text not null,
  counter int
);
CREATE INDEX longurl
ON URLTable (longURL)