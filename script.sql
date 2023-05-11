drop table if exists phase;
drop table if exists log_acces;

create table phase(
    id int not null primary key,
    name text not null
);

create table log_acces(
    id integer not null primary key autoincrement,
    num_phase int not null references phase(id),
    login text not null,
    num_badge int null,
    commentary text null,
    created_at datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
    successful boolean not null
);


insert into phase values(1, 'identification par login et password');
insert into phase values(2, 'identification par badge');
insert into phase values(3, 'identification par reconnaissance facial');