{% block title %}{{demands.subject_name}}{% endblock %}

{% block body %}
Dear {{rep.full_name}},

My name is {{name}}, and I'm a member of your district. I am writing to you today to to discuss the important issue of {{demands.subject_name}}.



Signed,

{{name}}
Executive Director, RELIC
http://relic-law.org

Attachment:

{{ rendered_law }}
{% endblock %}