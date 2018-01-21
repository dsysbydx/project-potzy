drop table if exists financial_statement;
create table financial_statement (
  id integer primary key autoincrement,
  ticker text not null,
  date text not null,

  ## list all items
  revenue real,
  net_income real,
  cashflow_operation real
);