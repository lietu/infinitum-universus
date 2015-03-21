{% for pkg in 'git', 'nodejs', 'npm' %}
{{ pkg }}:
    pkg.installed
{% endfor %}

{% for npm in 'bower', %}
{{ npm }}:
    npm.installed:
        - require:
            - pkg: npm
{% endfor %}

/usr/bin/node:
    file.symlink:
        - target: /usr/bin/nodejs
