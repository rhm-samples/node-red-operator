FROM quay.io/operator-framework/ansible-operator:v0.16.0
LABEL name="Node-RED Operator"
LABEL vendor="IBM"
LABEL version="v0.0.1"
LABEL release="1"
LABEL summary="Node-RED is a programming tool for wiring together hardware devices, APIs and online services in new and interesting ways."
LABEL description="This operator is for Node-RED v1.0.6"
COPY licenses /licenses

COPY requirements.yml ${HOME}/requirements.yml
RUN ansible-galaxy collection install -r ${HOME}/requirements.yml \
 && chmod -R ug+rwx ${HOME}/.ansible

COPY watches.yaml ${HOME}/watches.yaml

COPY roles/ ${HOME}/roles/