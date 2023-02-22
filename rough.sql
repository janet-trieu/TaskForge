create table TaskMaskers (
    primary key tm_id int,
    name text,
    email text,
    mobile_number varchar(10),
    is_admin boolean, 
)

create table Tasks (
    primary key task_id int,
    foreign key (creator_id) references TaskMaskers(tm_id),
    task_title text,
    task_description text,
    task_deadline date,
    task_workload decimal,
    update_status enum('Not Started', 'In Progress', 'Blocked', 'Completed')
)

create table Task_assignees (
    foreign key (task) references Tasks(task_id),
    foreign key (assignee) references TaskMaskers(tm_id)
)

