nginx:
    user.present:
        - name: www-data
        - fullname: nginx
        - shell: /bin/false
        - home: /var/www
        - groups:
            - www-data
            - server
    pkg:
        - installed
    service.running:
        - enable: True
        - require:
            - pkg: nginx
        - watch:
            - file: /etc/nginx/nginx.conf

{% for dir in '/var/www', '/etc/nginx/sites-enabled/', '/etc/nginx/sites-available/', '/var/lib/nginx', '/var/lib/nginx/tmp/' %}
{{ dir }}:
    file.directory:
        - user: www-data
        - group: www-data
        - mode: 755
        - makedirs: True
{% endfor %}

{% for path in '/etc/nginx/conf.d/', '/etc/nginx/sites-enabled/default' %}
{{ path }}:
    file.absent
{% endfor %}

/etc/nginx/nginx.conf:
    file.managed:
        - source: salt://nginx/nginx.conf
        - require:
            - pkg: nginx

{% for logdir in '/var/log/nginx/', %}
{{ logdir }}:
    file.directory:
        - user: www-data
        - group: www-data
        - mode: 750
        - makedirs: True
{% endfor %}

/etc/nginx/sites-available/devel.conf:
    file.managed:
        - source: salt://nginx/devel.conf
        - require:
            - pkg: nginx
            - file: /etc/nginx/sites-available/
        - watch_in:
            - service: nginx

/etc/nginx/sites-enabled/devel.conf:
    file.symlink:
        - target: /etc/nginx/sites-available/devel.conf
        - require:
            - file: /etc/nginx/sites-enabled/
        - watch_in:
            - service: nginx
