server:
    group.present:
        - system: False
    user.present:
        - fullname: server
        - shell: /bin/bash
        - home: /home/server
        - groups:
            - server

/home/server/.bashrc:
    file.managed:
        - source: salt://basic/bashrc
        - user: server
        - group: server
        - mode: 700

/home/server/:
    file.directory:
        - user: server
        - group: server
        - mode: 750
        - makedirs: True

# Bunch of useful tools people want on machines
{% for pkg in 'gcc', 'vim', 'nano', 'lsof', 'wget', 'curl', 'strace', 'bzip2' %}
{{ pkg }}:
    pkg.installed
{% endfor %}
