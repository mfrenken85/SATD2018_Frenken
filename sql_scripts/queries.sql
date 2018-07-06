Select b.id, b.commenttext, b.treated_commenttext, a.projectname, a.filename, a.classname, b.description, b.type
from comment_class as a, processed_comment as b
where a.id = b.commentclassid and a.projectname = 'fp2-launcher'

Select COUNT(b.id), a.projectname
from comment_class as a, processed_comment as b
where a.id = b.commentclassid
group by a.projectname

Select COUNT(DISTINCT(classname)), projectname
from comment_class
group by projectname

delete from processed_comment where id > 1000000000
delete from comment_class where id > 1000000000