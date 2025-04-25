CREATE SCHEMA IF NOT EXISTS "public";

CREATE TYPE notification_type_enum AS ENUM ('teams','email','both');

CREATE TYPE ticket_status AS ENUM ('new','in_progress','completed','queued');

CREATE  TABLE "public".departments ( 
	id                   uuid  NOT NULL  ,
	name                 varchar(255)  NOT NULL  ,
	CONSTRAINT departments_pkey PRIMARY KEY ( id ),
	CONSTRAINT departments_name_key UNIQUE ( name ) 
 );

CREATE  TABLE "public".users ( 
	id                   uuid  NOT NULL  ,
	display_name         varchar(255)  NOT NULL  ,
	principal_name       varchar(255)  NOT NULL  ,
	is_active            boolean DEFAULT true   ,
	location             varchar(255)    ,
	department_id        uuid    ,
	image                text    ,
	notification_type    "public".notification_type_enum DEFAULT 'email'::notification_type_enum   ,
	CONSTRAINT users_pkey PRIMARY KEY ( id ),
	CONSTRAINT users_principal_name_key UNIQUE ( principal_name ) 
 );

CREATE  TABLE "public".boards ( 
	board_id             uuid  NOT NULL  ,
	description          text    ,
	owner_id             uuid    ,
	created_at           timestamp DEFAULT CURRENT_TIMESTAMP   ,
	name                 varchar(255)  NOT NULL  ,
	is_archived          boolean  NOT NULL  ,
	CONSTRAINT boards_pkey PRIMARY KEY ( board_id ),
	CONSTRAINT unique_board_name UNIQUE ( name ) 
 );

CREATE  TABLE "public".lists ( 
	id                   uuid  NOT NULL  ,
	board_id             uuid  NOT NULL  ,
	task_ids             uuid[]    ,
	name                 text    ,
	is_archived          boolean DEFAULT false NOT NULL  ,
	is_collapsed         boolean DEFAULT false NOT NULL  ,
	"position"           integer DEFAULT 1 NOT NULL  ,
	CONSTRAINT pk_lists PRIMARY KEY ( id )
 );

CREATE  TABLE "public".roles ( 
	id                   uuid  NOT NULL  ,
	name                 varchar(255)    ,
	CONSTRAINT roles_pkey PRIMARY KEY ( id )
 );

CREATE  TABLE "public".templates ( 
	id                   uuid  NOT NULL  ,
	list_id              uuid    ,
	subject              varchar(255)  NOT NULL  ,
	description          text    ,
	author_id            uuid  NOT NULL  ,
	assignee_id          uuid    ,
	man_hours            integer    ,
	is_archived          boolean DEFAULT false NOT NULL  ,
	repeat_type          text  NOT NULL  ,
	start_date_time      timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	"interval"           integer DEFAULT 1 NOT NULL  ,
	end_date             date DEFAULT CURRENT_DATE NOT NULL  ,
	weekdays             text[]    ,
	monthly_repeat_type  text    ,
	monthly_repeat_date  integer    ,
	monthly_ordinal_number text    ,
	monthly_ordinal_day  text    ,
	yearly_repeat_type   text    ,
	yearly_month         text    ,
	yearly_month_repeat_date integer    ,
	yearly_ordinal_number text    ,
	yearly_ordinal_day   text    ,
	yearly_ordinal_month text    ,
	board_id             uuid  NOT NULL  ,
	CONSTRAINT pk_templates PRIMARY KEY ( id )
 );

CREATE  TABLE "public".user_board_access ( 
	id                   uuid  NOT NULL  ,
	board_id             uuid  NOT NULL  ,
	"role"               varchar DEFAULT 'editor'::character varying   ,
	CONSTRAINT user_board_access_pkey PRIMARY KEY ( id, board_id )
 );

CREATE  TABLE "public".tasks ( 
	id                   uuid  NOT NULL  ,
	assignee_id          uuid    ,
	author_id            uuid    ,
	subject              varchar(255)  NOT NULL  ,
	description          text    ,
	time_total           integer    ,
	created_at           timestamptz DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL  ,
	is_active            boolean DEFAULT true NOT NULL  ,
	last_updated_at      timestamptz DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text)   ,
	signature_url        text DEFAULT ''::text   ,
	signature_time       varchar(255)    ,
	board_id             uuid    ,
	signed_by_id         uuid    ,
	is_archived          boolean DEFAULT false NOT NULL  ,
	status_changed_at    timestamptz    ,
	status               "public".ticket_status DEFAULT 'new'::ticket_status NOT NULL  ,
	due_date             timestamptz    ,
	start_date           timestamptz    ,
	man_hours            integer    ,
	list_id              uuid    ,
	template_id          uuid    ,
	CONSTRAINT tickets_pkey PRIMARY KEY ( id )
 );

ALTER TABLE "public".tasks ADD CONSTRAINT tickets_time_total_check CHECK ( (time_total >= 0) );

CREATE INDEX idx_tickets_assignee_id ON "public".tasks USING  btree ( assignee_id );

CREATE INDEX idx_tickets_author_id ON "public".tasks USING  btree ( author_id );

CREATE INDEX idx_tickets_created_at ON "public".tasks USING  btree ( created_at );

CREATE  TABLE "public".checklists ( 
	id                   uuid  NOT NULL  ,
	task_id              uuid  NOT NULL  ,
	title                text  NOT NULL  ,
	created_at           timestamptz DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT checklists_pkey PRIMARY KEY ( id )
 );

CREATE  TABLE "public".comments ( 
	id                   uuid DEFAULT gen_random_uuid() NOT NULL  ,
	user_id              varchar(255)  NOT NULL  ,
	task_id              uuid    ,
	user_image           text    ,
	display_name         varchar(255)    ,
	text                 text  NOT NULL  ,
	post_time            timestamptz DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT comments_pkey PRIMARY KEY ( id )
 );

CREATE  TABLE "public".notifications ( 
	user_id              uuid  NOT NULL  ,
	task_id              uuid  NOT NULL  ,
	reminder_int         varchar(50)  NOT NULL  ,
	notify_comments      boolean DEFAULT false NOT NULL  ,
	notify_status        boolean DEFAULT false NOT NULL  ,
	notify_signature     boolean DEFAULT false NOT NULL  ,
	notify_assignee      boolean DEFAULT false NOT NULL  ,
	board_name           varchar[]    ,
	notify_due_date      boolean DEFAULT false   ,
	CONSTRAINT notifications_pkey PRIMARY KEY ( user_id, task_id )
 );

CREATE  TABLE "public".checklist_items ( 
	id                   uuid  NOT NULL  ,
	checklist_id         uuid  NOT NULL  ,
	item_text            text  NOT NULL  ,
	is_completed         boolean DEFAULT false NOT NULL  ,
	created_at           timestamptz DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT checklist_items_pkey PRIMARY KEY ( id )
 );

ALTER TABLE "public".boards ADD CONSTRAINT boards_owner_id_fkey FOREIGN KEY ( owner_id ) REFERENCES "public".users( id );

ALTER TABLE "public".checklist_items ADD CONSTRAINT fk_checklist FOREIGN KEY ( checklist_id ) REFERENCES "public".checklists( id );

ALTER TABLE "public".checklists ADD CONSTRAINT fk_task FOREIGN KEY ( task_id ) REFERENCES "public".tasks( id );

ALTER TABLE "public".comments ADD CONSTRAINT comments_ticket_id_fkey FOREIGN KEY ( task_id ) REFERENCES "public".tasks( id ) ON DELETE CASCADE;

ALTER TABLE "public".lists ADD CONSTRAINT fk_lists_boards FOREIGN KEY ( board_id ) REFERENCES "public".boards( board_id );

ALTER TABLE "public".notifications ADD CONSTRAINT fk_notifications_user FOREIGN KEY ( user_id ) REFERENCES "public".users( id ) ON DELETE CASCADE;

ALTER TABLE "public".notifications ADD CONSTRAINT fk_notifications_task FOREIGN KEY ( task_id ) REFERENCES "public".tasks( id ) ON DELETE CASCADE;

ALTER TABLE "public".roles ADD CONSTRAINT fk_roles_users FOREIGN KEY ( id ) REFERENCES "public".users( id );

ALTER TABLE "public".tasks ADD CONSTRAINT tickets_assignee_id_fkey FOREIGN KEY ( assignee_id ) REFERENCES "public".users( id ) ON DELETE SET NULL;

ALTER TABLE "public".tasks ADD CONSTRAINT tickets_author_id_fkey FOREIGN KEY ( author_id ) REFERENCES "public".users( id ) ON DELETE SET NULL;

ALTER TABLE "public".tasks ADD CONSTRAINT fk_tasks_templates FOREIGN KEY ( template_id ) REFERENCES "public".templates( id );

ALTER TABLE "public".tasks ADD CONSTRAINT fk_tasks_lists FOREIGN KEY ( list_id ) REFERENCES "public".lists( id );

ALTER TABLE "public".tasks ADD CONSTRAINT fk_board_id FOREIGN KEY ( board_id ) REFERENCES "public".boards( board_id );

ALTER TABLE "public".tasks ADD CONSTRAINT fk_tickets_users FOREIGN KEY ( signed_by_id ) REFERENCES "public".users( id );

ALTER TABLE "public".templates ADD CONSTRAINT fk_templates_lists FOREIGN KEY ( list_id ) REFERENCES "public".lists( id );

ALTER TABLE "public".user_board_access ADD CONSTRAINT user_board_access_id_fkey FOREIGN KEY ( id ) REFERENCES "public".users( id );

ALTER TABLE "public".user_board_access ADD CONSTRAINT user_board_access_board_id_fkey FOREIGN KEY ( board_id ) REFERENCES "public".boards( board_id );

ALTER TABLE "public".users ADD CONSTRAINT fk_users_department FOREIGN KEY ( department_id ) REFERENCES "public".departments( id );

CREATE TRIGGER track_ticket_time BEFORE UPDATE OF status ON public.tasks FOR EACH ROW WHEN ((old.is_archived = false)) EXECUTE FUNCTION update_ticket_time();

CREATE OR REPLACE FUNCTION public.get_current_time_total(ticket_id uuid)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
DECLARE
    ticket_record "public".tickets%ROWTYPE;
BEGIN
    SELECT * INTO ticket_record FROM "public".tickets WHERE id = ticket_id;
    
    IF ticket_record.status = 'in_progress' AND ticket_record.status_changed_at IS NOT NULL THEN
        RETURN COALESCE(ticket_record.time_total, 0) + 
            EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - ticket_record.status_changed_at))::integer;
    ELSE
        RETURN COALESCE(ticket_record.time_total, 0);
    END IF;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_ticket_time()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.status = 'in_progress' AND OLD.status != 'in_progress' THEN
        -- Starting progress
        NEW.status_changed_at = CURRENT_TIMESTAMP;
    ELSIF OLD.status = 'in_progress' AND NEW.status != 'in_progress' THEN
        -- Stopping progress - add elapsed time to time_total
        NEW.time_total = COALESCE(OLD.time_total, 0) + 
            EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - OLD.status_changed_at))::integer;
        NEW.status_changed_at = NULL;
    END IF;
    RETURN NEW;
END;
$function$
;

